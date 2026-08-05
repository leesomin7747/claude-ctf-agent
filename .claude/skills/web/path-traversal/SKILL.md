---
name: path-traversal
description: 경로 순회로 임의 파일 읽기
---
## When
파일명/경로 입력

## Tools
curl

## Procedure
1) 입력점 확인
2) `../` 시퀀스
3) 인코딩 우회
4) 플래그 파일

## PoC
```
?file=....//....//etc/passwd
```

## Pitfalls
null byte·이중 인코딩·절대경로; 화이트리스트 회피
