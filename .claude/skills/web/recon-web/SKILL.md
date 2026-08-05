---
name: recon-web
description: 웹 타겟 정찰: 엔드포인트·기술스택·입력지점 매핑
---
## When
웹 문제 착수 직후

## Tools
curl, ffuf, jq

## Procedure
1) 헤더/쿠키
2) robots·경로 퍼징
3) JS 번들 분석
4) 입력지점 표

## PoC
```
ffuf -u $U/FUZZ -w wordlist -mc 200,301,302
```

## Pitfalls
클라이언트 검증만 믿지 말 것; 숨은 파라미터 존재
