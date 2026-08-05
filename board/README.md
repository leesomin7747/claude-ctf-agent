# board/

대회 실시간 상태. 이 안의 `scope.md`/`challenges.md`/`writeups/`는 런타임에 갱신되며
`.gitignore`로 커밋에서 제외된다(템플릿만 최초 커밋).

- `scope.md` — 인가 타겟(In-Scope) + 플래그 정규식(Flag-Format). 대회 시작 시 채운다.
- `challenges.md` — 문제 상태 표. 상태: todo → solving → solved / stuck / needs-scope / needs-user.
- `writeups/` — 문제별 `<challenge>.md` 산출물.
