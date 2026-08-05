#!/usr/bin/env python3
"""CTF 에이전트 아티팩트 구조 검증기 (표준 라이브러리만 사용)."""
import sys, re, glob, os

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)

def parse_front(text):
    m = FRONTMATTER.match(text)
    if not m:
        return None
    keys = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k = line.split(":", 1)[0].strip()
            keys[k] = line.split(":", 1)[1].strip()
    return keys

def has_anchors(text, anchors):
    return [a for a in anchors if not re.search(r"^%s\s*$" % re.escape(a), text, re.M)]

SKILL_ANCHORS = ["## When", "## Tools", "## Procedure", "## PoC", "## Pitfalls"]
SOLVER_ANCHORS = ["## Budget", "## Skills", "## Protocol", "## Return"]
WEB_SOLVER_EXTRA = ["## Recon Checklist", "## Vuln Tree"]
CLAUDE_ANCHORS = ["## Competition Protocol", "## Scope Lock", "## Flag Rules", "## Workflow"]

def validate_file(path):
    """리스트(에러문자열) 반환. 빈 리스트면 통과."""
    if not os.path.isfile(path):
        return ["missing file"]
    text = open(path, encoding="utf-8").read()
    errs = []
    norm = path.replace("\\", "/")
    if norm.endswith("/SKILL.md") or "/skills/" in norm:
        fm = parse_front(text)
        if fm is None: errs.append("no frontmatter")
        else:
            for k in ("name", "description"):
                if k not in fm: errs.append("frontmatter missing '%s'" % k)
        errs += ["missing anchor '%s'" % a for a in has_anchors(text, SKILL_ANCHORS)]
    elif "/agents/" in norm:
        fm = parse_front(text)
        if fm is None: errs.append("no frontmatter")
        else:
            for k in ("name", "description", "tools"):
                if k not in fm: errs.append("frontmatter missing '%s'" % k)
        anchors = SOLVER_ANCHORS + (WEB_SOLVER_EXTRA if norm.endswith("web-solver.md") else [])
        errs += ["missing anchor '%s'" % a for a in has_anchors(text, anchors)]
    elif "/commands/" in norm:
        fm = parse_front(text)
        if fm is None or "description" not in (fm or {}):
            errs.append("frontmatter missing 'description'")
    elif norm.endswith("CLAUDE.md"):
        errs += ["missing anchor '%s'" % a for a in has_anchors(text, CLAUDE_ANCHORS)]
    return errs

def targets(args):
    if args:
        return args
    found = ["CLAUDE.md"]
    for pat in (".claude/skills/**/SKILL.md", ".claude/agents/*.md", ".claude/commands/*.md"):
        found += glob.glob(pat, recursive=True)
    return found

def main():
    paths = targets(sys.argv[1:])
    failed = False
    for p in paths:
        errs = validate_file(p)
        if errs:
            failed = True
            for e in errs:
                sys.stderr.write("FAIL %s: %s\n" % (p, e))
    if failed:
        sys.exit(1)
    print("OK (%d files)" % len(paths))

if __name__ == "__main__":
    main()
