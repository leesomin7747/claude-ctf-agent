#!/usr/bin/env python3
"""solver가 참조하는 스킬 슬러그와 실제 skills/ 디렉토리 일치 검증(양방향)."""
import os, re, sys

CATS = {"web-solver": "web", "pwn-solver": "pwn", "rev-solver": "rev",
        "crypto-solver": "crypto", "forensic-solver": "forensic", "misc-solver": "misc"}

fail = False
for agent, cat in CATS.items():
    ap = ".claude/agents/%s.md" % agent
    text = open(ap, encoding="utf-8").read()

    m = re.search(r"## Skills(.*?)(?:\n## |\Z)", text, re.S)
    skills_text = m.group(1) if m else ""

    # solver가 명시적으로 나열한 스킬 슬러그만 추출한다.
    # "...로드: slug1, slug2, ..., slugN." 형태 문장에서 "로드:" 다음부터
    # 첫 마침표까지만 취해, 뒤이어 나오는 일반 산문 속 소문자 단어들이
    # (예: "각 스킬의 When으로 적용 판단...") 슬러그로 오검출되지 않게 한다.
    list_m = re.search(r"로드:\s*(.*?)\.", skills_text, re.S)
    referenced = set()
    if list_m:
        for tok in list_m.group(1).split(","):
            tok = re.sub(r"\s+", "", tok.strip().strip("`"))
            if tok:
                referenced.add(tok)

    # 실제 스킬 디렉토리만 집계: 디렉토리이면서 SKILL.md를 가진 항목만 인정한다
    # (.DS_Store 같은 잡파일이나 SKILL.md 없는 빈 폴더는 무시).
    skilldir = ".claude/skills/%s" % cat
    actual = set()
    if os.path.isdir(skilldir):
        for entry in os.listdir(skilldir):
            full = os.path.join(skilldir, entry)
            if os.path.isdir(full) and os.path.isfile(os.path.join(full, "SKILL.md")):
                actual.add(entry)

    # 방향 1(기존): 실제 디렉토리가 solver 본문에 언급되는지 확인
    not_referenced = sorted(actual - referenced)
    if not_referenced:
        fail = True
        sys.stderr.write("FAIL %s: skills not referenced by %s: %s\n" % (cat, agent, not_referenced))

    # 방향 2(신규): solver가 언급한 슬러그가 실제 디렉토리로 존재하는지 확인
    # (오타났거나 삭제된 슬러그가 조용히 통과하는 것을 방지)
    dangling = sorted(referenced - actual)
    if dangling:
        fail = True
        sys.stderr.write("FAIL %s: %s references nonexistent skill dir(s): %s\n" % (cat, agent, dangling))

if fail:
    sys.exit(1)
print("indexes OK")
