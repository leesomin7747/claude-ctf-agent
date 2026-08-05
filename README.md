# ctf-agent

CTF/워게임 자동 풀이 Claude Code 에이전트. 웹 해킹 최대 비중, 풀 카테고리, 대회 실시간 병렬 풀이.

## 구조
- `CLAUDE.md` — 대회 프로토콜·스코프 락·플래그 규칙
- `.claude/commands/` — /ctf, /ctf-board, /ctf-web, /ctf-writeup, /ctf-setup
- `.claude/agents/` — 카테고리별 solver(web/pwn/rev/crypto/forensic/misc)
- `.claude/skills/` — 기법 라이브러리(web 13, 기타 17, meta 4)
- `board/` — 런타임 상태(scope/challenges/writeups)

## 대회 시작 절차
1. `board/scope.md`의 In-Scope에 인가 타겟, Flag-Format에 대회 플래그 정규식 설정.
2. `/ctf-setup`으로 툴 점검.
3. `/ctf <문제 URL/파일/지문>`으로 풀이 시작(여러 개 동시 가능).
4. `/ctf-board`로 현황 확인.

## 커맨드
| 커맨드 | 용도 |
|---|---|
| /ctf | 트리아지+병렬 풀이+플래그+writeup |
| /ctf-board | 보드 현황 |
| /ctf-web | web-solver 직접 호출 |
| /ctf-writeup | writeup 재생성 |
| /ctf-setup | 툴 설치 점검 |

## 검증
`python3 tools/validate.py && python3 tools/check_indexes.py`

## 스코프 정책
스코프 내 타겟은 확인 없이 자유 실행, 스코프 밖 능동 공격은 거부. 인가된 CTF 대상에만 사용.
