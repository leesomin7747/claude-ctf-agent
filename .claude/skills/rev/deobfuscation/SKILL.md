---
name: deobfuscation
description: 난독·패킹 해제
---
## When
UPX/VM/난독 스크립트

## Tools
upx, python

## Procedure
1) 패커 식별
2) 언팩
3) VM/난독 패턴 복원
4) 로직 추출

## PoC
```
upx -d ./chal
```

## Pitfalls
커스텀 패커는 덤프 후 재구성
