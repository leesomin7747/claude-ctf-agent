---
name: hash-length-ext
description: 해시 길이확장 공격
---
## When
`H(secret‖msg)` MAC

## Tools
hashpump, python

## Procedure
1) 취약 구성 확인
2) 길이확장으로 위조
3) 서명 우회

## PoC
```
hashpumpy
```
로 확장 서명 생성

## Pitfalls
시크릿 길이 브루트포싱 필요
