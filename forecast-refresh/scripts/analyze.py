#!/usr/bin/env python3
"""Recompute the forecast model in pure Python (no LibreOffice) and surface WoW/MoM deltas,
accuracy, pace, and ANOMALIES that need SA classification.
Usage: analyze.py --xlsx WB [--json] [--wow-drop 0.08] [--divergence 0.05] [--pace 0.05]
Reads: Event Ledger (params + events), Actuals (real net), Math!D (standing projection DBU baseline)."""
import argparse, json
from datetime import date, datetime, timedelta
import openpyxl

def asdate(v):
    if isinstance(v,datetime): return v.date()
    if isinstance(v,date): return v
    if isinstance(v,str):
        for f in ("%Y-%m-%d","%m/%d/%Y"):
            try: return datetime.strptime(v.strip(),f).date()
            except ValueError: pass
    return None

def label_cell(ws, key):
    for r in range(1,20):
        for c in range(1,8):
            if key in str(ws.cell(r,c).value or "").lower():
                return ws.cell(r,c+2).value
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--xlsx",required=True); ap.add_argument("--json",action="store_true")
    ap.add_argument("--wow-drop",type=float,default=0.08); ap.add_argument("--divergence",type=float,default=0.05)
    ap.add_argument("--pace",type=float,default=0.05)
    a=ap.parse_args()
    wb=openpyxl.load_workbook(a.xlsx, data_only=True)
    L=wb["Event Ledger"]
    list_rate=float(label_cell(L,"list_rate") or 0.52)
    as_of=asdate(label_cell(L,"as_of")); net_commit=float(label_cell(L,"commit (") or label_cell(L,"net_commit") or 0)

    # ledger events
    contracts=[]; workloads=[]
    hr=None
    for r in range(1,30):
        if str(L.cell(r,2).value or "").strip().lower()=="event_id": hr=r; break
    r=hr+1
    while L.cell(r,2).value:
        dt=asdate(L.cell(r,3).value); typ=str(L.cell(r,4).value or "").lower()
        param=L.cell(r,7).value; inl=str(L.cell(r,9).value or "").upper()
        if typ=="contract" and dt is not None: contracts.append((dt,float(param)))
        if typ=="workload" and dt is not None: workloads.append((dt,float(param),inl))
        r+=1
    contracts.sort()
    def disc(dt):
        d=contracts[0][1] if contracts else 0.0
        for cd,cp in contracts:
            if cd<=dt: d=cp
        return d
    def wload(dt):
        return sum(p for wd,p,inl in workloads if inl=="Y" and wd<=dt)

    # actuals
    A=wb["Actuals"]; ahr=None
    for r in range(1,20):
        if str(A.cell(r,2).value or "").strip().lower()=="date": ahr=r; break
    act={}
    r=ahr+1
    while A.cell(r,2).value:
        dt=asdate(A.cell(r,2).value)
        if dt is not None:
            act[dt]=(float(A.cell(r,3).value or 0), float(A.cell(r,4).value or 0))  # dbu, net
        r+=1

    # Math: daily actuals + weekly forecast. baseline DBU/day = col E(5); days = col D(4)
    M=wb["Math"]; mhr=None
    for r in range(1,20):
        if str(M.cell(r,2).value or "").strip().lower()=="date": mhr=r; break
    baseline={}; daysmap={}; timeline=[]
    r=mhr+1
    while M.cell(r,2).value:
        dt=asdate(M.cell(r,2).value)
        if dt is not None:
            timeline.append(dt); baseline[dt]=float(M.cell(r,5).value or 0); daysmap[dt]=float(M.cell(r,4).value or 1)
        r+=1
    timeline.sort()

    def predicted_net(dt):
        return (baseline.get(dt,0)+wload(dt))*list_rate*(1-disc(dt))
    def actual_net(dt):
        return act.get(dt,(None,None))[1]

    # ---- metrics ----
    def rng(a,b): return [d for d in timeline if a<=d<=b]
    def sum_net(dates, kind):
        s=0.0
        for d in dates:
            v=actual_net(d) if kind=="actual" else predicted_net(d)
            if v is not None: s+=v
        return s
    cur=actual_net(as_of)
    # WoW / MoM on actual net + dbu
    def actual_dbu(dt): return act.get(dt,(None,None))[0]
    def wow(fn):
        cur7=[fn(as_of-timedelta(days=i)) for i in range(0,7)]
        prev7=[fn(as_of-timedelta(days=i)) for i in range(7,14)]
        cur7=[x for x in cur7 if x]; prev7=[x for x in prev7 if x]
        if not cur7 or not prev7: return None
        c=sum(cur7); p=sum(prev7); return (c-p)/p if p else None
    def mom(fn):
        cur30=[fn(as_of-timedelta(days=i)) for i in range(0,30)]
        prev30=[fn(as_of-timedelta(days=i)) for i in range(30,60)]
        cur30=[x for x in cur30 if x]; prev30=[x for x in prev30 if x]
        if not cur30 or not prev30: return None
        return (sum(cur30)-sum(prev30))/sum(prev30)
    # accuracy to date
    past=[d for d in timeline if d<=as_of and actual_net(d) is not None]
    err=sum(abs(actual_net(d)-predicted_net(d)) for d in past)
    denom=sum(actual_net(d) for d in past)
    accuracy=1-err/denom if denom else None
    # committed next 365 (predicted, days-weighted: forecast rows are weekly)
    fut=[d for d in timeline if as_of<d<=as_of+timedelta(days=365)]
    committed=sum(predicted_net(d)*daysmap.get(d,1) for d in fut)
    # cumulative to date + position vs commit
    cum=sum(actual_net(d) for d in past)
    # pace: trailing-14d actual daily avg vs committed-line daily avg (next 14d predicted)
    t14=[d for d in past if d>as_of-timedelta(days=14)]
    pace_actual=sum(actual_net(d) for d in t14)/len(t14) if t14 else None
    n14=[d for d in timeline if as_of<d<=as_of+timedelta(days=14)]
    pace_line=sum(predicted_net(d) for d in n14)/len(n14) if n14 else None
    pace_gap=(pace_actual-pace_line)/pace_line if (pace_actual and pace_line) else None

    # ---- anomalies ----
    an=[]
    w_net=wow(actual_net); w_dbu=wow(actual_dbu)
    if w_net is not None and w_net<=-a.wow_drop:
        an.append({"kind":"wow_drop_net","value":round(w_net,3),
                   "ask":f"Net $ dropped {w_net:.0%} WoW to {as_of}. Optimization / workload offboarded / discount change / noise? Add a contract|workload event, or ignore?"})
    if w_dbu is not None and w_dbu<=-a.wow_drop:
        an.append({"kind":"wow_drop_dbu","value":round(w_dbu,3),
                   "ask":f"DBU dropped {w_dbu:.0%} WoW — real consumption drop (workload), not a pricing artifact. Classify it."})
    # divergence over trailing 7d (tightened from 14d — flag in a week, not two)
    t7=[d for d in past if d>as_of-timedelta(days=7)]
    if t7:
        da=sum(actual_net(d) for d in t7); dp=sum(predicted_net(d) for d in t7)
        div=(da-dp)/dp if dp else None
        if div is not None and abs(div)>=a.divergence:
            downside = div<0
            an.append({"kind":"model_divergence","value":round(div,3),
                       "ask":f"Actual is {div:+.0%} vs model over trailing 7d. "
                             + ("DOWNSIDE — actual under model; you will miss low unless the baseline comes down. Re-baseline now."
                                if downside else "Running hot — actual over model; is an unlogged workload live? Re-baseline up.")})
    if pace_gap is not None and pace_gap<=-a.pace:
        an.append({"kind":"pace_slip","value":round(pace_gap,3),
                   "ask":f"Pace is {pace_gap:.0%} below the committed line — you will miss unless it recovers. What's the plan / what changed?"})
    # cumulative vs commit
    if net_commit:
        if cum>=net_commit:
            an.append({"kind":"over_commit","value":round(cum/net_commit,2),
                       "ask":f"Cumulative net is {cum/net_commit:.1f}x the commit — renegotiation (contract event) coming? Up. Confirm date/discount."})
        elif cum>=0.85*net_commit:
            an.append({"kind":"near_commit","value":round(cum/net_commit,2),
                       "ask":f"At {cum/net_commit:.0%} of commit — burst is near. Add the projected recommit contract event?"})

    out={"as_of":str(as_of),"current_daily_run_rate":round(cur,0) if cur else None,
         "committed_next_365":round(committed,0),"commit_target":net_commit,
         "committed_vs_commit_x":round(committed/net_commit,2) if net_commit else None,
         "accuracy_to_date":round(accuracy,3) if accuracy is not None else None,
         "wow_net":round(w_net,3) if w_net is not None else None,
         "wow_dbu":round(w_dbu,3) if w_dbu is not None else None,
         "mom_net":round(mom(actual_net),3) if mom(actual_net) is not None else None,
         "cumulative_net":round(cum,0),"cumulative_vs_commit_x":round(cum/net_commit,2) if net_commit else None,
         "pace_gap":round(pace_gap,3) if pace_gap is not None else None,
         "status":"GREEN" if (pace_gap is None or pace_gap>-a.pace) else "YELLOW",
         "anomalies":an}
    if a.json: print(json.dumps(out,indent=2))
    else:
        print(f"as_of {out['as_of']}  run-rate ${out['current_daily_run_rate']:,.0f}/day  committed ${out['committed_next_365']:,.0f} ({out['committed_vs_commit_x']}x)  accuracy {out['accuracy_to_date']:.1%}  status {out['status']}")
        print(f"WoW net {out['wow_net']}  WoW dbu {out['wow_dbu']}  MoM net {out['mom_net']}  cum {out['cumulative_vs_commit_x']}x commit")
        if an:
            print("ANOMALIES (classify before the call):")
            for x in an: print(f"  [{x['kind']}] {x['ask']}")
        else: print("No anomalies — on pace.")

if __name__=="__main__": main()
