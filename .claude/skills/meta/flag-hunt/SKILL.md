---
name: flag-hunt
description: 툴 출력과 solver 로그에서 플래그를 추출·형식검증하고 보드에 기록한다
---
## When
solver가 결과를 반환했을 때, 또는 임의 툴 출력에서 플래그를 확인해야 할 때.

## Tools
`grep -Eo`, ripgrep. 정규식은 `board/scope.md`의 Flag-Format에서 읽음.

## Procedure
1. `board/scope.md`의 `## Flag-Format` 아래 각 줄을 정규식으로 로드(없으면 기본값 3종).
2. 대상 텍스트에 각 정규식 매칭 → 후보 수집(중복 제거).
3. 후보가 여러 개면 문제 문맥(형식·길이)로 가장 그럴듯한 것 선택, 나머지는 로그에 남김.
4. `board/challenges.md`의 해당 문제 행에 플래그 + ISO8601 타임스탬프 기록, 상태 solved.

## PoC
`grep -Eo 'FLAG\{.*?\}|DH\{.*?\}' output.txt | sort -u`

## Pitfalls
디코이 플래그·플래그 형식의 예시 문자열 주의. 확정 전 `[FLAG]` 태그로 근거(어디서 나왔는지) 남길 것.
