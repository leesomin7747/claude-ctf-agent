---
name: encoding-decoding
description: 다중 인코딩·인코더 체인 해제
---
## When
base/hex/rot 덩어리

## Tools
python, CyberChef식

## Procedure
1) 인코딩 식별
2) 계층 순차 해제
3) 압축·직렬화 처리
4) 플래그

## PoC
```
echo $S | base64 -d | xxd
```

## Pitfalls
magic으로 포맷 추정; 순서 중요
