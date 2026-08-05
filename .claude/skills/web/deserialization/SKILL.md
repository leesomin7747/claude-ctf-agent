---
name: deserialization
description: 역직렬화 취약점으로 RCE
---
## When
직렬화 객체 문자열(base64 등)

## Tools
python, ysoserial

## Procedure
1) 포맷 식별(pickle/PHP/Java)
2) 가젯 체인
3) 페이로드 생성
4) 주입

## PoC
```
python -c "import pickle,os,base64;..."  # 가젯 클래스 __reduce__
```

## Pitfalls
언어별 가젯 상이; 화이트리스트 우회 필요할 수 있음
