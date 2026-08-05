---
name: format-string
description: 포맷스트링으로 누출·임의쓰기
---
## When
`printf(user)` 형태

## Tools
pwntools

## Procedure
1) 오프셋 탐색 `%p`
2) 누출
3) `%n` 임의쓰기
4) GOT 덮어쓰기

## PoC
```
%7$p
```
류로 스택 누출

## Pitfalls
짧은 버퍼·정확한 쓰기 폭 계산
