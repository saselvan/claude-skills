### Scenario 5: Compliance Audit Trail (Data Lineage for Regulators)

**Audience:** Compliance officers, internal audit, external regulators  
**Intent:** Show how Unity Catalog + Lakeflow Jobs provide audit-ready lineage  
**Canvas Size:** S (1200x700)

**Architecture:** Regulated Data Sources (ERP, claims, patient records) → Data Intelligence Platform (Unity Catalog + Lakeflow Jobs + Audit Logs) → Regulatory Reports. Compliance Officer validates provenance and access; Data Analyst runs approved queries; Auditor reviews lineage and governance.

**Talking Points:**
- Every data transformation logged (source → bronze → silver → gold)
- Column-level masking for PII (automatic redaction for analysts)
- Access control tied to job role, not individuals
- Audit logs exportable for regulators (SOX, HIPAA, GDPR)

```xml
<mxfile>
  <diagram name="Compliance Audit Trail" id="compliance-audit-1">
    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="700">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="platform" value="Data Intelligence Platform" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FF3621;" 
          vertex="1" parent="1">
          <mxGeometry x="350" y="60" width="500" height="480" as="geometry"/>
        </mxCell>
        
        <mxCell id="sources-zone" value="Regulated Data Sources" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=1;" 
          vertex="1" parent="1">
          <mxGeometry x="40" y="160" width="140" height="280" as="geometry"/>
        </mxCell>
        
        <mxCell id="erp" value="ERP&#xa;Financial Records" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;fontColor=#333333;strokeColor=#999999;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="60" y="200" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="claims" value="Claims&#xa;Insurance Data" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;fontColor=#333333;strokeColor=#999999;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="60" y="280" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="patient-records" value="Patient Records&#xa;PHI/PII Data" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;fontColor=#333333;strokeColor=#999999;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="60" y="360" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="auto-loader" value="Auto Loader&#xa;File ingestion" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="platform">
          <mxGeometry x="40" y="80" width="80" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="bronze" value="Bronze&#xa;Raw ingested data&#xa;(provenance tracked)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#CD7F32;fontColor=#FFFFFF;strokeColor=#8B4513;fontSize=10;fontStyle=1;" 
          vertex="1" parent="platform">
          <mxGeometry x="40" y="220" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="silver" value="Silver&#xa;Cleansed &amp; validated&#xa;(PII masked)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C0C0C0;fontColor=#000000;strokeColor=#808080;fontSize=10;fontStyle=1;" 
          vertex="1" parent="platform">
          <mxGeometry x="190" y="220" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="gold" value="Gold&#xa;Curated analytics&#xa;(access controlled)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;fontColor=#000000;strokeColor=#B8860B;fontSize=10;fontStyle=1;" 
          vertex="1" parent="platform">
          <mxGeometry x="340" y="220" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="dbsql" value="SQL Warehouse&#xa;Query execution&#xa;(logged)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="platform">
          <mxGeometry x="160" y="355" width="90" height="55" as="geometry"/>
        </mxCell>
        
        <mxCell id="reports-zone" value="Regulatory Reports" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1020" y="160" width="140" height="280" as="geometry"/>
        </mxCell>
        
        <mxCell id="hipaa-logs" value="HIPAA Audit&#xa;Logs" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;fontColor=#333333;strokeColor=#999999;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1040" y="200" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="lineage-export" value="Lineage&#xa;Export" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;fontColor=#333333;strokeColor=#999999;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1040" y="360" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="compliance-officer" value="Compliance Officer&#xa;(validates provenance &amp; access)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E1F5FE;fontColor=#01579B;strokeColor=#0288D1;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="330" y="10" width="160" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="data-analyst" value="Data Analyst&#xa;(runs approved queries)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E1F5FE;fontColor=#01579B;strokeColor=#0288D1;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="160" y="310" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="auditor" value="Auditor/Regulator&#xa;(reviews lineage &amp; governance)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E1F5FE;fontColor=#01579B;strokeColor=#0288D1;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1000" y="10" width="180" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="governance" value="Governance — Unity Catalog&#xa;Access control · PII masking · Lineage · Audit trail" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="560" width="1200" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="350" y="620" width="500" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-1a" value="Ingest logged" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="erp" target="auto-loader" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-bronze-silver" value="Validation &amp; masking" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="bronze" target="silver" parent="platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-silver-gold" value="Curation &amp; access control" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="silver" target="gold" parent="platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-2" value="Query curated data (recorded in audit log)" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="data-analyst" target="dbsql" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-3a" value="Export audit trail: lineage graph" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="platform" target="lineage-export" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-4" value="Review lineage: who accessed what, when, why" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;dashed=1;" 
          edge="1" source="auditor" target="reports-zone" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="flow-5" value="Validate governance: role-based access, column masking" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;dashed=1;" 
          edge="1" source="auditor" target="platform" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

