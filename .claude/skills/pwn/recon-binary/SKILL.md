---
name: recon-binary
description: 바이너리 정찰: 보호기법·함수·입력 파악
---
## When
pwn 착수 직후

## Tools
checksec, strings, r2

## Procedure
1) `checksec`
2) 함수·문자열
3) 입력·오버플로 지점
4) libc 확인

## PoC
```
checksec --file=./chal
```

## Pitfalls
PIE/카나리 여부로 전략 결정
