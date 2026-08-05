---
name: rop-stack-overflow
description: 스택 오버플로+ROP로 제어흐름 탈취
---
## When
오프바이·긴입력 크래시

## Tools
pwntools, ropper

## Procedure
1) 오프셋 산출
2) 가젯 수집
3) ROP 체인
4) 셸/플래그

## PoC
```
cyclic 200
ropper --file bin
```
`cyclic 200`으로 오프셋, `ropper --file bin`

## Pitfalls
ASLR 시 libc 누출 필요; 정렬 이슈
