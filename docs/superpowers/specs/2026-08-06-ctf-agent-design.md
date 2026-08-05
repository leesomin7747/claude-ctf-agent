# CTF/워게임 자동 풀이 에이전트 — 설계서

- **작성일**: 2026-08-06
- **폼팩터**: Claude Code 네이티브 (CLAUDE.md + commands + agents + skills)
- **성격**: 자동 풀이형 · 대회 실시간(다중 문제 병렬) · 풀 카테고리(웹 최대 비중)
- **아키텍처**: 오케스트레이터 + 병렬 서브에이전트 + 공유 스킬 라이브러리 (접근 B)

---

## 1. 목표와 비목표

### 목표
- CTF 대회 중 여러 문제를 **동시에** 받아, 카테고리 분류 → 자동 풀이 → 플래그 회수 → writeup 생성까지 최소 개입으로 수행.
- 웹 해킹을 가장 깊게 다루고(전용 스킬 12개 내외), pwn/rev/crypto/forensic/misc도 핵심 기법으로 커버.
- 문제별 컨텍스트를 격리해 상호 간섭을 없애고 병렬성을 확보.
- 대회 진행 상황(문제 상태·플래그·점수)을 실시간 보드로 추적.

### 비목표
- 학습 코칭(단계별 힌트 유도)은 이 에이전트의 기본 모드가 아니다. (자동 풀이 우선)
- 논문 수준의 완전 자율 knowledge-graph 멀티에이전트는 만들지 않는다. 유지보수 가능한 실용 패턴만 흡수.
- 대회 범위 밖 실제 서비스에 대한 공격은 지원하지 않는다(스코프 락).

---

## 2. 근거가 된 레퍼런스 분석

| 소스 | 배운 점 | 우리 설계 반영 |
|---|---|---|
| `ljagiello/ctf-skills` | 카테고리별 폴더 + `SKILL.md`(전제조건+방법론) + `/solve-challenge` 오케스트레이터 위임 | `.claude/skills/<cat>/` 구조, meta 오케스트레이션 스킬 |
| `0xSteph/pentest-ai-agents`, `H-mmer/pentest-agents` | 역할별 서브에이전트 + 슬래시 커맨드 진입점 | `.claude/agents/*-solver.md`, `/ctf*` 커맨드 |
| CTFExplorer (arXiv 2602.08023) | 정찰→병렬 실행자, 예산 제한 에이전트 체인, 자기비평(50/80%), critic 개입, 증거 타입 분류 | 서브에이전트 예산·자기비평·critic·증거타입 로그 |

**핵심 판단**: 완전 자동 풀이를 원하므로 CTFExplorer식 오케스트레이션이 적합하나, knowledge-graph/공유메모리 전체를 수작업 구현하는 것은 ROI가 낮다. 예산 제한·자기비평·증거 타입만 부분 흡수한다.

---

## 3. 파일 구조

```
ctf-agent/
├── CLAUDE.md                  # 에이전트 헌법: 대회 프로토콜, 스코프 락, 워크플로, 플래그 규칙
├── .claude/
│   ├── commands/
│   │   ├── ctf.md             # /ctf  — 메인: 트리아지 + 풀이 디스패치
│   │   ├── ctf-board.md       # /ctf-board — 현황판 출력
│   │   ├── ctf-web.md         # /ctf-web — 웹 솔버 직접 호출
│   │   ├── ctf-writeup.md     # /ctf-writeup — writeup 재생성
│   │   └── ctf-setup.md       # /ctf-setup — 툴 설치/점검
│   ├── agents/
│   │   ├── web-solver.md      # ★ 최대 깊이
│   │   ├── pwn-solver.md
│   │   ├── rev-solver.md
│   │   ├── crypto-solver.md
│   │   ├── forensic-solver.md
│   │   └── misc-solver.md
│   └── skills/
│       ├── web/               # ★ (아래 §5)
│       ├── pwn/  rev/  crypto/  forensic/  misc/
│       └── meta/              # triage-classify, flag-hunt, writeup-generate, tool-check
└── board/
    ├── scope.md               # 인가된 타겟/도메인 (스코프 락)
    ├── challenges.md          # 문제 보드
    └── writeups/              # 문제별 산출물
```

---

## 4. 컴포넌트 명세

### 4.1 오케스트레이터 (`/ctf` + CLAUDE.md)
- **입력**: URL / 로컬 파일 경로 / 문제 지문 텍스트 / 붙여넣기(여러 문제 가능).
- **동작**:
  1. `meta/triage-classify` 스킬로 각 문제 카테고리 분류(web/pwn/rev/crypto/forensic/misc) + 신뢰도.
  2. `board/challenges.md`에 등록(상태 `todo`).
  3. 문제가 여럿이면 **문제당 서브에이전트를 병렬 spawn**(Agent 도구, `run_in_background`). 단일 문제면 동기 실행.
  4. 각 서브에이전트 결과(플래그 + 증거타입 로그 + writeup 노트) 수집.
  5. `meta/flag-hunt`로 플래그 검증 → 보드 갱신 → `meta/writeup-generate`로 writeup 산출.
- **critic 역할**: 한 서브에이전트가 N회(기본 3) 연속 실패 보고 시, 재분류하거나 대체 기법을 지시해 재디스패치.

### 4.2 카테고리 서브에이전트 (`.claude/agents/*-solver.md`)
- 각 파일은 Claude Code 서브에이전트 정의(frontmatter: `name`, `description`, `tools`, `model`).
- **공통 프로토콜**(각 solver 본문에 명시):
  - **예산**: 시도 라운드 상한(기본 web=12, 기타=8). 50%/80% 지점에서 자기비평 체크포인트(무엇을 시도했나 / 무엇이 유효했나 / 다음 가설).
  - **증거 타입 로그**: 모든 관찰을 `[OBS] / [HYP] / [POC] / [FLAG]` 태그로 기록 → writeup 원재료.
  - **스킬 로드**: 해당 카테고리 스킬 목록을 읽고 탐지 신호에 맞는 것을 선택 적용.
  - **반환 형식**: 아래 §7 표준 결과 스키마.
  - **에스컬레이션**: 예산 소진·범위밖 타겟 필요·수동 확인 필요 시 오케스트레이터로 반환(사용자에게 보고).
- **web-solver**가 가장 상세(정찰 체크리스트 + 취약점 분류 트리 + 스킬 인덱스 포함).

### 4.3 스킬 라이브러리 (`.claude/skills/**/SKILL.md`)
- 각 스킬 표준 섹션:
  1. `frontmatter`: `name`, `description`(트리거 판단용 한 줄).
  2. **탐지 신호(When)**: 이 기법을 언제 의심하나(요청/응답/소스 단서).
  3. **전제조건/툴**: 필요한 CLI(설치 확인은 `meta/tool-check` 위임).
  4. **공격 절차**: 단계별. 재현 가능한 명령/페이로드.
  5. **PoC 템플릿**: 붙여 쓸 수 있는 스크립트/요청 골격.
  6. **함정/우회**: WAF·필터 우회, 흔한 실패 원인.

### 4.4 플래그 매니저 (`meta/flag-hunt`)
- 대회별 플래그 정규식을 `board/scope.md` 상단 설정에서 읽음(기본 다중: `FLAG\{.*?\}`, `DH\{.*?\}`, `[a-z0-9_]+\{.*?\}`).
- 서브에이전트 출력·툴 로그를 스캔해 후보 추출 → 형식 검증 → 보드의 해당 문제에 기록 + 타임스탬프.

### 4.5 writeup 생성기 (`meta/writeup-generate`)
- 입력: 증거타입 로그 + 최종 플래그.
- 출력: `board/writeups/<challenge>.md` — 정찰 → 취약점 → 익스플로잇(재현 명령) → 플래그 → 회고.

### 4.6 스코프/안전 레이어
- `board/scope.md`에 인가된 타겟(호스트/도메인/포트/파일 경로) 명시.
- **자유 실행**: 스코프 내 타겟에는 공격 툴(sqlmap/ffuf/nmap/pwntools 등)을 **매 명령 확인 없이** 실행.
- **스코프 락**: 스코프에 없는 호스트로의 능동 공격 요청은 서브에이전트가 거부하고 오케스트레이터에 보고(오발·법적 사고 방지). 사용자가 `board/scope.md`에 추가하면 즉시 허용.

---

## 5. 스킬 인벤토리 (초기 구축 대상 — 전체 골대)

### web/ (12 + 정찰)
`recon-web`, `sqli`, `xss`, `ssrf`, `jwt`, `file-upload-rce`, `xxe`, `deserialization`, `ssti`, `idor-authbypass`, `path-traversal`, `race-condition`, `graphql`.

### pwn/ (4)
`recon-binary`, `rop-stack-overflow`, `format-string`, `heap-exploit`.

### rev/ (3)
`static-triage`, `dynamic-analysis`, `deobfuscation`.

### crypto/ (4)
`rsa-attacks`, `aes-mode-attacks`, `hash-length-ext`, `classical-encoding`.

### forensic/ (4)
`pcap-analysis`, `memory-forensics`, `stego`, `disk-file-carving`.

### misc/ (2)
`encoding-decoding`, `jail-escape`.

### meta/ (4)
`triage-classify`, `flag-hunt`, `writeup-generate`, `tool-check`.

> 개수는 초기 기준선. 대회에서 부딪히는 기법을 스킬로 추가해 성장시킨다.

---

## 6. 슬래시 커맨드 명세

| 커맨드 | 인자 | 동작 |
|---|---|---|
| `/ctf` | URL/파일/지문(복수 가능) | 트리아지 → 보드 등록 → 병렬 풀이 → 플래그·writeup |
| `/ctf-board` | 없음 | 현재 보드 상태 표(문제/카테고리/상태/점수/플래그) |
| `/ctf-web` | 타겟 | 트리아지 생략, web-solver 직접 호출 |
| `/ctf-writeup` | 문제명 | 해당 문제 writeup 재생성 |
| `/ctf-setup` | 없음 | `tool-check` 실행, 누락 툴 설치 안내/실행 |

---

## 7. 표준 결과 스키마 (서브에이전트 → 오케스트레이터)

```
challenge: <이름/식별자>
category: web|pwn|rev|crypto|forensic|misc
status: solved | stuck | needs-scope | needs-user
flag: <문자열 또는 null>
techniques: [사용한 스킬 목록]
evidence:            # 증거타입 로그 요약
  - [OBS] ...
  - [HYP] ...
  - [POC] ...
  - [FLAG] ...
next_steps: <stuck일 때 다음 가설/필요한 것>
writeup_path: board/writeups/<challenge>.md
```

---

## 8. board/challenges.md 포맷

마크다운 표(사람이 바로 읽기 쉬움, git diff 친화적).

```
| # | 문제 | 카테고리 | 점수 | 상태 | 플래그 | 갱신 |
|---|------|---------|------|------|--------|------|
| 1 | ez-sqli | web | 100 | solved | FLAG{...} | 2026-08-06T12:00 |
```

상태 값: `todo` → `solving` → `solved` / `stuck` / `needs-scope` / `needs-user`.

---

## 9. 전형적 실행 흐름

```
사용자: /ctf  (문제 3개 붙여넣기: 웹URL, 바이너리 첨부, crypto 지문)
  → triage-classify: [web, pwn, crypto]
  → challenges.md에 3행 등록 (todo)
  → 병렬 spawn: web-solver, pwn-solver, crypto-solver
       web-solver: recon-web → sqli 신호 감지 → sqli 스킬 → flag
       pwn-solver: recon-binary → rop → 예산 60%에서 자기비평 → heap로 전환 → flag
       crypto-solver: rsa-attacks → 3회 실패 보고 → critic이 hash-length-ext 지시 → flag
  → flag-hunt: 3개 플래그 검증·기록
  → writeup-generate: writeups/ 3개 생성
  → /ctf-board: 3 solved 표시
```

---

## 10. 구현 순서 (writing-plans 단계에서 상세화)

1. 골격: 디렉토리 + `CLAUDE.md`(프로토콜·스코프 락·플래그 규칙) + `board/` 초기 파일.
2. meta 스킬 4종(triage/flag-hunt/writeup/tool-check) — 오케스트레이션의 뼈대.
3. 커맨드 5종.
4. 서브에이전트 6종(공통 프로토콜 + web-solver 상세).
5. web/ 스킬 12+1 (최우선, 깊게).
6. 나머지 카테고리 스킬(pwn/rev/crypto/forensic/misc).
7. 통합 리허설: 카테고리별 샘플 문제로 end-to-end 검증(단일·병렬).

---

## 11. 미해결/추후 결정
- 대회별 플래그 정규식·스코프는 대회 시작 시 `board/scope.md`에서 세팅(런타임 설정).
- 병렬 서브에이전트 동시 실행 상한(리소스 고려) — 구현 시 기본값 정하고 튜닝.
- writeup 다국어(한/영) 여부 — 기본 한국어, 필요 시 옵션.
