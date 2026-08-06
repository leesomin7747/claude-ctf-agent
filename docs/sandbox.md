# 샌드박스 · 격리 실습 환경에서 사용하기

능동 공격 도구(nmap·sqlmap·metasploit·nuclei 등)는 **인가된 격리 타겟에만** 실행해야 한다.
이 문서는 (1) Claude Code 샌드박스로 네트워크 egress를 제한하는 법, (2) 로컬 격리 랩을
띄우는 법, (3) 각 도구의 역할, (4) Scope Lock과의 정합을 정리한다.

## 왜 샌드박스인가
- 에이전트가 실수로 **범위 밖 실제 서비스**를 스캔·공격하는 사고 방지(오발·법적 리스크).
- 익스플로잇 프레임워크(metasploit)·스캐너(nmap/nuclei/trivy)는 파급이 크므로 egress를
  대회/랩 도메인으로 **하드 제한**한 채 돌리는 게 안전하다.
- 이 에이전트의 `board/scope.md` **Scope Lock**과 샌드박스 **network allowlist**를 일치시키면
  이중 방어가 된다(에이전트 레벨 거부 + 런타임 레벨 차단).

## 1) Claude Code 샌드박스 설정

`.claude/settings.local.json`(개인·gitignore) 또는 `.claude/settings.json`(팀 공유)에 `sandbox`
블록을 둔다. 예시는 `.claude/settings.sandbox.example.json`에 있다. 핵심:

```json
{
  "permissions": { "defaultMode": "acceptEdits" },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "network": {
      "allowedDomains": [
        "*.ctf.example",           // 대회 도메인
        "chal.example.ctf",
        "localhost", "127.0.0.1"   // 로컬 랩
      ],
      "strictAllowlist": true       // 목록 밖 호스트는 프롬프트 없이 차단
    }
  }
}
```

- `strictAllowlist: true` → allowedDomains에 없는 호스트로의 네트워크는 샌드박스 런타임이
  **결정적으로 차단**한다(에이전트가 실수해도 나가지 못함).
- `autoAllowBashIfSandboxed: true` → 샌드박스 안에서 도는 Bash는 매번 확인 없이 실행(자유 실행).
- 대회가 바뀌면 allowedDomains와 `board/scope.md` In-Scope를 **함께** 갱신한다.
- 주의: `sandbox.network.strictAllowlist`·`tlsTerminate` 등 일부 키는 프로젝트 settings에서
  무시되고 user/managed/CLI(`--settings`)에서만 적용된다. 강한 격리가 필요하면 user 설정이나
  `claude --settings sandbox.json`으로 띄운다.

## 2) 로컬 격리 랩

소스가 주어지는 웹/인프라 문제는 로컬에서 격리해 띄우고, 스코프를 로컬로 한정한다.

```bash
# 예: docker-compose로 취약 타겟을 격리 네트워크에 기동
docker compose up -d            # 타겟이 127.0.0.1:PORT 또는 172.x 내부망에 노출
# board/scope.md In-Scope에 http://127.0.0.1:PORT/ 추가
# 샌드박스 allowedDomains에 127.0.0.1, localhost 추가
```

격리 랩에서만 능동 스캐너를 자유롭게 돌린다:
```bash
nmap -sV -p- 127.0.0.1                    # 서비스/포트 매핑
nuclei -u http://127.0.0.1:PORT           # 웹 취약점 템플릿 스캔
trivy image <lab-image>                    # 컨테이너 이미지 CVE (cloud/devops 문제)
```

## 3) 도구 역할

| 도구 | 용도 | 언제 |
|---|---|---|
| `nmap` | 포트·서비스·버전 매핑 | 인프라/네트워크 문제, 랩 정찰 |
| `nuclei` | 템플릿 기반 웹/네트워크 취약점 스캔 | 웹 정찰 보강(빠른 저부하 스캔) |
| `trivy` | 컨테이너 이미지·IaC·시크릿 스캔 | cloud/devops/컨테이너 카테고리 |
| `metasploit`(`msfconsole`) | 알려진 CVE 익스 | **인가된 격리 랩 한정**, 자동화 익스 |
| `sqlmap`/`dalfox`/`commix` | SQLi/XSS/커맨드인젝션 자동화 | web-solver가 수동 확인 후 자동화 |

> 능동 스캐너·익스는 소음·파괴 가능성이 있으니 **격리 랩 또는 대회가 명시 허용한 타겟**에만.
> 대회 규정에 자동 스캐너 금지가 있으면 사용하지 않는다.

## 4) Scope Lock 정합 체크리스트

대회/실습 시작 시:
1. `board/scope.md` `## In-Scope`에 인가 타겟만 기입.
2. 샌드박스 `network.allowedDomains`를 **같은 목록**으로 맞춤(+`strictAllowlist: true`).
3. `/ctf-setup`으로 필요한 도구 설치 점검.
4. 능동 스캐너/익스는 랩·인가 타겟에서만. 범위 밖이 필요하면 `needs-scope`로 보고 후 사용자 승인.

이 4단계를 지키면 에이전트 레벨(Scope Lock)과 런타임 레벨(sandbox allowlist)이 함께 막아
오발·범위 이탈을 이중으로 방지한다.
