---
name: aes-mode-attacks
description: 블록암호 운용모드 취약점
---
## When
ECB/CBC/nonce 재사용

## Tools
python(pycryptodome)

## Procedure
1) 모드 식별(ECB 반복블록)
2) 바이트플립/오라클
3) 패딩오라클
4) 복호·위조

## PoC
```
ECB cut-and-paste 스크립트
```

## Pitfalls
IV/nonce 재사용·패딩 오라클 구분
