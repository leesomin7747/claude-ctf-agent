---
name: race-condition
description: 경쟁 상태로 제한 우회
---
## When
동시 요청 시 상태 불일치

## Tools
curl, python(threads)

## Procedure
1) 임계 연산 식별
2) 동시 요청 발사
3) 창(window) 활용
4) 효과 확인

## PoC
```
파이썬 스레드로 동일 요청 N개 동시 전송
```

## Pitfalls
단일패킷 공격 필요 시 정밀 타이밍; 멱등성 확인
