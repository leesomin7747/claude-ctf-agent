#!/usr/bin/env python3
"""solver가 참조하는 스킬 슬러그와 실제 skills/ 디렉토리 일치 검증."""
import os, re, sys

CATS = {"web-solver": "web", "pwn-solver": "pwn", "rev-solver": "rev",
        "crypto-solver": "crypto", "forensic-solver": "forensic", "misc-solver": "misc"}
fail = False
for agent, cat in CATS.items():
    ap = ".claude/agents/%s.md" % agent
    text = open(ap, encoding="utf-8").read()
    m = re.search(r"## Skills(.*?)(?:\n## |\Z)", text, re.S)
    referenced = set(re.findall(r"[a-z][a-z0-9-]+", m.group(1))) if m else set()
    skilldir = ".claude/skills/%s" % cat
    actual = set(os.listdir(skilldir)) if os.path.isdir(skilldir) else set()
    missing = [s for s in actual if s not in referenced]
    ghost = [s for s in actual if not os.path.isfile("%s/%s/SKILL.md" % (skilldir, s))]
    # 실제 디렉토리의 각 스킬이 solver 본문에 언급되는지 확인
    not_referenced = [s for s in actual if s not in referenced]
    if not_referenced:
        fail = True
        sys.stderr.write("FAIL %s: skills not referenced by %s: %s\n" % (cat, agent, not_referenced))
if fail:
    sys.exit(1)
print("indexes OK")
