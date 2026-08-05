---
name: ssrf
description: 서버측 요청 위조로 내부 접근
---
## When
서버가 URL을 fetch/미리보기

## Tools
curl

## Procedure
1) URL 파라미터 확인
2) 내부 대역·메타데이터 시도
3) 스킴/리다이렉트 우회

## PoC
```
?url=http://169.254.169.254/latest/meta-data/
```

## Pitfalls
DNS rebinding·`0.0.0.0`·10진 IP 우회; 블랙리스트 회피
