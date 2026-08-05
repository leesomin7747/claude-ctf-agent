---
name: rsa-attacks
description: RSA 파라미터 취약점 공격
---
## When
n,e,c 제공

## Tools
python(sympy,pycryptodome), RsaCtfTool

## Procedure
1) e·n 특성 확인
2) 소인수분해/작은e/공통모듈러스
3) 복호
4) 플래그

## PoC
```
RsaCtfTool --publickey k.pem --uncipher c
```

## Pitfalls
여러 취약 조합 동시 점검
