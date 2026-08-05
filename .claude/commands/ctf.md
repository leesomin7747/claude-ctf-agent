---
description: CTF 문제를 트리아지→분류→병렬 풀이하고 플래그와 writeup을 산출한다
argument-hint: <URL | 파일경로 | 문제 지문 (복수 가능)>
---
입력: $ARGUMENTS

CLAUDE.md의 Competition Protocol을 따른다:
1. `triage-classify` 스킬로 각 문제를 카테고리 분류하고 `board/challenges.md`에 등록(todo).
2. 문제가 2개 이상이면 문제당 해당 카테고리 서브에이전트(web-solver 등)를 병렬 spawn(백그라운드),
   1개면 동기 실행. 각 서브에이전트에 문제 식별자·입력·스코프를 전달.
3. 각 서브에이전트의 표준 결과 스키마를 수집한다.
4. `flag-hunt`로 플래그 검증·기록, `writeup-generate`로 writeup 생성, 보드 상태 갱신.
5. 최종 요약(문제별 상태·플래그·writeup 경로)을 표로 출력.

스코프: `board/scope.md`의 In-Scope에 없는 능동 공격은 실행하지 말고 needs-scope로 보고.
