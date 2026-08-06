---
name: tool-check
description: CTF 풀이에 필요한 CLI 툴 설치 여부를 점검하고 누락분 설치를 안내·실행한다
---
## When
`/ctf-setup` 실행 시, 또는 solver가 특정 툴을 쓰기 직전 존재를 확인할 때.

## Tools
`command -v`, `brew`(darwin), `pipx`(파이썬 CLI), `pip`/`python3 -m pip`(라이브러리), `go install`(go 툴).

## Procedure
1. 카테고리별 툴을 점검한다(★=핵심, 나머지는 상황용). 없으면 우측 명령으로 설치.

   **web** (최우선)
   - ★`curl`, ★`jq` — 기본 HTTP/JSON (`brew install curl jq`)
   - ★`ffuf` 디렉토리/파라미터 퍼징 (`brew install ffuf`), `gobuster`/`feroxbuster` 대체
   - ★`sqlmap` SQLi (`brew install sqlmap` 또는 `pipx install sqlmap`)
   - ★`nuclei` 템플릿 스캐너 (`brew install nuclei`)
   - `dalfox` XSS (`brew install dalfox`), `commix` 커맨드 인젝션 (`pipx install commix`)
   - `jwt_tool` JWT 공격 (`pipx install jwt-tool`), `arjun` 숨은 파라미터 (`pipx install arjun`)
   - `httpx` 프로빙 (`brew install httpx`), `gau`/`waybackurls` URL 수집, `hakrawler` 크롤
   - `wpscan` 워드프레스 (`brew install wpscan`), `nikto` 서버 스캔 (`brew install nikto`)

   **pwn**
   - ★`python3`+`pwntools` (`python3 -m pip install --user pwntools`)
   - ★`gdb` + 강화(`pwndbg` 또는 `gef`) — `brew install gdb`; pwndbg: `git clone https://github.com/pwndbg/pwndbg && ./pwndbg/setup.sh`
   - ★`checksec` (`brew install checksec`), `ropper`/`ROPgadget` (`pipx install ropper`)
   - `one_gadget` (`gem install one_gadget`), `seccomp-tools` (`gem install seccomp-tools`), `patchelf` (`brew install patchelf`)

   **rev**
   - ★`radare2` 또는 `rizin` (`brew install radare2`), `strings`(내장), `binwalk` (`brew install binwalk`)
   - `ghidra` GUI(선택, `brew install --cask ghidra`), `upx` (`brew install upx`), `apktool`(android, `brew install apktool`)

   **crypto**
   - ★`python3` 라이브러리: `pycryptodome sympy gmpy2` (`python3 -m pip install --user pycryptodome sympy gmpy2`)
   - `openssl`(내장), `RsaCtfTool`(git clone), `hashcat`/`john` 해시크랙 (`brew install hashcat john-jumbo`)

   **forensic**
   - ★`tshark`/`wireshark` (`brew install wireshark`), `exiftool` (`brew install exiftool`)
   - `volatility3` (`pipx install volatility3`), `steghide`/`zsteg`(stego), `foremost`/`binwalk`/`testdisk`(카빙)

   **network/infra** (샌드박스 실습 환경용 — `docs/sandbox.md` 참고)
   - ★`nmap` 포트/서비스 스캔 (`brew install nmap`), `masscan` 고속 (`brew install masscan`)
   - ★`nuclei` 웹/네트워크 취약점 템플릿 스캔
   - `trivy` 컨테이너/IaC 취약점 스캔 (`brew install trivy`) — cloud/devops 문제용
   - `metasploit`(`msfconsole`) 익스 프레임워크 (`brew install --cask metasploit`) — **인가된 격리 랩에서만**

   **공통**: `git`, `python3`, `pipx`(`brew install pipx && pipx ensurepath`), `go`.

2. 점검은 `command -v <tool>` (파이썬 라이브러리는 `python3 -c "import <mod>"`)로 하고, 없으면 위 명령으로 설치.
3. 자유 실행 정책에 따라 sudo 불필요한 설치(brew/pipx/pip --user)는 바로 수행. **큰 변경**(cask GUI: ghidra·metasploit, 시스템 패키지)은 시간·용량이 크니 사용자에게 알리고 진행.

## PoC
```
# 웹 핵심 툴 한 번에 점검
for t in curl jq ffuf sqlmap nuclei dalfox jwt_tool nmap nuclei trivy gdb; do
  command -v "$t" >/dev/null && echo "ok $t" || echo "MISSING $t"
done
# 파이썬 라이브러리 점검
for m in pwn Crypto sympy requests; do python3 -c "import $m" 2>/dev/null && echo "ok $m" || echo "MISSING $m"; done
# darwin 일괄 설치 예
brew install ffuf sqlmap nuclei nmap jq checksec binwalk exiftool
python3 -m pip install --user pwntools pycryptodome sympy requests
```

## Pitfalls
pwntools/volatility3/sqlmap 등 파이썬 CLI는 `pipx`(격리)로, 라이브러리는 `pip --user`로 설치해 전역 오염을 피한다. GUI 툴(ghidra·wireshark·metasploit-cask)은 용량이 크고 필수가 아니므로 필요 시에만. `metasploit`·`nmap`·`masscan` 등 능동 네트워크 툴은 **반드시 `board/scope.md` In-Scope(인가된 격리 랩)** 안에서만 실행(Scope Lock). macOS는 pip PEP668로 `--user` 또는 venv 필요.
