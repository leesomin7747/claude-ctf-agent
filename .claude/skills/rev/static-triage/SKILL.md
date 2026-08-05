---
name: static-triage
description: 정적 분석으로 로직·플래그검증 파악
---
## When
실행파일·네트워크無

## Tools
r2/rizin, strings, ghidra

## Procedure
1) strings·심볼
2) 디컴파일
3) 플래그 검증 루틴
4) 역산

## PoC
```
rizin -A ./chal
pdf @ main
```

## Pitfalls
안티디스어셈블·가짜 심볼 주의
