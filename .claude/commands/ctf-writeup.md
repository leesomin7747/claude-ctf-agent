---
description: 지정한 문제의 writeup을 재생성한다
argument-hint: <문제명>
---
대상 문제: $ARGUMENTS

`board/challenges.md`에서 해당 문제의 상태·플래그를 찾고, 남아있는 증거타입 로그를 근거로
`writeup-generate` 스킬을 호출해 `board/writeups/<slug>.md`를 다시 만든다.
로그가 없으면 사용 가능한 정보로 최선의 writeup을 작성하고 부족한 부분을 명시한다.
