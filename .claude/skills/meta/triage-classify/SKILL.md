---
name: triage-classify
description: CTF 문제 입력을 카테고리(web/pwn/rev/crypto/forensic/misc)로 분류하고 신뢰도를 매긴다
---
## When
새 문제가 들어와 어느 solver로 보낼지 정해야 할 때. `/ctf`가 최초로 호출한다.

## Tools
`file`, `binwalk`, `strings`, `curl -I`(스코프 내). 입력이 URL/파일/텍스트인지에 따라 선택.

## Procedure
1. 입력 형태 판별: URL → 웹 우선. 파일 → `file`로 타입 확인. 텍스트 → 키워드/패턴.
2. 신호 매핑:
   - web: http(s) URL, HTML/JS, 쿠키/JWT, 로그인 폼, GraphQL 엔드포인트.
   - pwn: ELF/PE 실행파일, `nc host port`, libc 첨부.
   - rev: 실행파일인데 네트워크 없음, 난독화 스크립트, .apk/.class.
   - crypto: RSA/AES 언급, 키·암호문·nonce, 인코딩 덩어리.
   - forensic: .pcap, 메모리 덤프, 이미지/오디오(stego), 디스크 이미지.
   - misc: 그 외(인코딩 퍼즐, jail, esolang).
3. 각 문제에 `category` + `confidence(high/med/low)` 부여.
4. `board/challenges.md`에 행 추가(상태 todo). 애매하면 상위 2개 후보를 기록.

## PoC
`file ./chal` → `ELF 64-bit` ⇒ pwn/rev 후보. `curl -sI $URL | grep -i server` ⇒ web 스택 단서.

## Pitfalls
겉보기 web이 실제로 crypto(JWT 약한 서명)일 수 있음 → confidence low면 solver에 대체 후보를 함께 전달.
