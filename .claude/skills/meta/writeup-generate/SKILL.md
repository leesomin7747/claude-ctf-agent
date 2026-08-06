---
name: writeup-generate
description: 증거타입 로그와 플래그로 문제별 writeup 마크다운을 생성한다
---
## When
문제가 solved 되어 재현 가능한 기록을 남길 때. `/ctf` 말미와 `/ctf-writeup`이 호출.

## Tools
없음(로그·플래그 텍스트만 사용).

## Procedure
0. **writeup 본문은 한국어로 작성한다**(제목·섹션명·설명 모두). 명령어·페이로드·코드·플래그 등 기술 토큰은 원문 그대로 두되, 설명 산문은 한국어.
1. solver의 증거타입 로그(`[OBS]/[HYP]/[POC]/[FLAG]`)와 사용 스킬 목록 수집.
2. 다음 구조로 `board/writeups/<challenge>.md` 작성:
   - 제목/카테고리/점수
   - 정찰: `[OBS]` 요약
   - 취약점: `[HYP]`에서 확정된 근본 원인
   - 익스플로잇: `[POC]`의 재현 명령/페이로드(그대로 실행 가능하게)
   - 플래그: `[FLAG]`
   - 회고: 막혔던 지점·대체 기법
3. 파일 경로를 결과 스키마 `writeup_path`에 반환.

## PoC
파일명은 문제명을 슬러그화(`공백→-`, 소문자). 예: `ez sqli` → `board/writeups/ez-sqli.md`.

## Pitfalls
재현 명령에 실제 타겟 호스트가 들어가면 스코프 내 값인지 확인. 비어있는 섹션은 생략하지 말고 "해당 없음" 명시.
