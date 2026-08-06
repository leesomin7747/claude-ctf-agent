# ctf-agent

CTF/워게임 자동 풀이 Claude Code 에이전트. 웹 해킹 최대 비중, 풀 카테고리, 대회 실시간 병렬 풀이.

## 빠른 시작

Claude Code에서 이 폴더를 열면 `/ctf` 계열 커맨드와 solver가 자동 로드된다.

**1) 대회 세팅 (1분)** — `board/scope.md` 편집:
```markdown
## Flag-Format
FLAG\{.*?\}                 # 대회 플래그 정규식으로 교체

## In-Scope
https://web1.ctf.io/        # 공격이 인가된 타겟만 나열
10.10.10.5:8080
```
> In-Scope에 없는 호스트는 에이전트가 능동 공격을 거부(`needs-scope`)한다.

**2) 툴 점검**
```
/ctf-setup
```

**3) 문제 풀기** — URL·파일·지문을 붙여넣기만:
```
/ctf https://web1.ctf.io/login?id=1
```
여러 개 동시(2개 이상이면 병렬):
```
/ctf
https://web1.ctf.io/          (웹)
./pwn/challenge.bin           (바이너리)
n=0x1337..., e=3, c=...       (crypto 지문)
```
→ 분류 → 보드 등록 → 카테고리별 solver 병렬 실행 → 플래그 검증 → writeup 생성 → 요약까지 자동.

**4) 현황·산출물**
```
/ctf-board
```
- 플래그·상태: `board/challenges.md`
- 상세 writeup(재현 명령 포함): `board/writeups/<문제>.md`

**막히면**: solver가 `needs-scope`면 타겟을 In-Scope에 추가, `stuck`이면 힌트/대체 기법을 지시. 인증 필요한 문제는 자격증명을 `/ctf` 입력이나 scope.md Notes에 함께 준다.

**새 기법은 스킬로 축적**: `.claude/skills/<cat>/<slug>/SKILL.md` 추가 후 `python3 tools/validate.py && python3 tools/check_indexes.py`로 정합성 확인.

## 구조
- `CLAUDE.md` — 대회 프로토콜·스코프 락·플래그 규칙
- `.claude/commands/` — /ctf, /ctf-board, /ctf-web, /ctf-writeup, /ctf-setup
- `.claude/agents/` — 카테고리별 solver(web/pwn/rev/crypto/forensic/misc)
- `.claude/skills/` — 기법 라이브러리(web 14, 기타 18, meta 4)
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
