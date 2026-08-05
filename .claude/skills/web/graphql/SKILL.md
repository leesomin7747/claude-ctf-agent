---
name: graphql
description: GraphQL 남용으로 정보노출·우회
---
## When
`/graphql` 엔드포인트

## Tools
curl, jq

## Procedure
1) introspection 질의
2) 스키마 분석
3) 숨은 필드·뮤테이션
4) IDOR/인젝션 결합

## PoC
```
curl $U/graphql -d '{"query":"{__schema{types{name}}}"}'
```

## Pitfalls
introspection 비활성 시 필드 브루트포싱; batching 남용
