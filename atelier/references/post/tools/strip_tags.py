"""Make the publish copy of a draft: drop [Cnn] claim tags and evidence citations like (runs/...), tidy spaces.
Citation folders come from post.config.json "citation_dirs" (default: transcripts, runs, evidence, results).
Usage: python3 tools/strip_tags.py drafts/post1.md  -> drafts/post1.publish.md"""
import json, re, sys
from pathlib import Path

cfg_file = Path("post.config.json")
cfg = json.loads(cfg_file.read_text()) if cfg_file.exists() else {}
dirs = "|".join(map(re.escape, cfg.get("citation_dirs", ["transcripts", "runs", "evidence", "results"])))
cite = rf"\((?:{dirs})/[^)]*\)"
bad = 0
for p in sys.argv[1:]:
    s = open(p).read()
    s = re.sub(r"(\s*\[C\d+\])+", "", s)
    s = re.sub(rf"^[ \t]*{cite}[ \t]*\n", "", s, flags=re.M)   # a citation alone on a line
    s = re.sub(rf"\s*{cite}", "", s)                            # a citation inside a line
    s = re.sub(r"\n{3,}", "\n\n", s)
    out = p.replace(".md", ".publish.md"); open(out, "w").write(s)
    left = re.findall(rf"\[C\d+\]|\((?:{dirs})/", s)
    bad += len(left)
    print(out, "leftover tags:", len(left), "chars:", len(s), "words:", len(s.split()))
sys.exit(1 if bad else 0)
