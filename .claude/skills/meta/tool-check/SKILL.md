---
name: tool-check
description: CTF 풀이에 필요한 CLI 툴 설치 여부를 점검하고 누락분 설치를 안내·실행한다
---
## When
`/ctf-setup` 실행 시, 또는 solver가 특정 툴을 쓰기 직전 존재를 확인할 때.

## Tools
`command -v`, `brew`(darwin), `pipx`/`pip`.

## Procedure
1. 카테고리별 핵심 툴 목록을 점검:
   - web: `curl`, `ffuf`, `sqlmap`, `nmap`, `jq`, `nikto`
   - pwn: `python3`(pwntools), `gdb`, `checksec`, `ropper`, `one_gadget`
   - rev: `radare2`/`rizin`, `ghidra`(선택), `strings`, `binwalk`
   - crypto: `python3`(pycryptodome, sympy), `openssl`
   - forensic: `wireshark`/`tshark`, `volatility3`, `exiftool`, `steghide`, `foremost`
2. `command -v <tool>`로 존재 확인 → 없으면 설치 명령 제시(darwin: `brew install`, python: `pipx install`).
3. 자유 실행 정책에 따라 설치를 바로 수행하되, 시스템 변경이 큰 항목은 사용자에게 알림.

## PoC
`for t in ffuf sqlmap nmap jq; do command -v $t >/dev/null && echo "ok $t" || echo "MISSING $t"; done`

## Pitfalls
pwntools/volatility는 venv/pipx 권장(전역 오염 방지). GUI 툴(ghidra/wireshark)은 필수 아님으로 표시.
