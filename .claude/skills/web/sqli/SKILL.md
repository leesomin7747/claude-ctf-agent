---
name: sqli
description: SQL 인젝션으로 데이터 추출·인증우회
---
## When
DB 오류/불린 차이/정렬 변화

## Tools
sqlmap, curl

## Procedure
1) 주입점 확인(`'`,`"`)
2) 불린/시간/UNION 판별
3) 컬럼수·DBMS
4) 데이터/플래그 추출

## PoC
```
sqlmap -u "$U?id=1" --batch --dump
```

## Pitfalls
WAF 필터 시 인코딩/주석 우회; 블라인드는 시간기반
