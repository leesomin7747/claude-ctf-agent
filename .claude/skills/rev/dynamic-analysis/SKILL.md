---
name: dynamic-analysis
description: 동적 분석으로 런타임 동작 관찰
---
## When
정적으로 불충분·패킹

## Tools
gdb, ltrace, strace

## Procedure
1) 브레이크포인트
2) 비교 지점 관찰
3) 메모리·레지스터
4) 입력 역산

## PoC
```
gdb -q ./chal
b *cmp addr
```

## Pitfalls
안티디버깅(ptrace) 우회 필요
