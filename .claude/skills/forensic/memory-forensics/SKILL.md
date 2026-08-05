---
name: memory-forensics
description: 메모리 덤프 분석
---
## When
.raw/.vmem/.dmp

## Tools
volatility3

## Procedure
1) 프로세스/네트워크
2) 덤프·파일 추출
3) 레지스트리·크리덴셜
4) 플래그

## PoC
```
vol -f mem.raw windows.pslist
```

## Pitfalls
프로파일/심볼 일치 필요
