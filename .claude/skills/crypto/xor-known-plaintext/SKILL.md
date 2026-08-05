---
name: xor-known-plaintext
description: XOR 암호를 알려진 평문으로 키 복구·위조
---
## When
XOR로 암호화된 데이터인데 평문 전부/일부를 알거나 추측 가능할 때. 반복키 XOR, 단일바이트 XOR, `base64(XOR(json, key))` 형태의 쿠키/토큰(기본값 JSON을 아는 경우), 고정 포맷 헤더/매직바이트가 있는 경우.

## Tools
python3, `pwntools`의 `xor()`, `xortool`, `openssl`/`base64`/`xxd`(인코딩 계층 벗기기).

## Procedure
1) 인코딩 계층 먼저 제거: URL 디코드 → base64 디코드 등으로 원시 암호문 바이트 확보.
2) 알려진/추측 평문 확보: 기본 설정 JSON, 파일 매직바이트, 프로토콜 헤더 등.
3) 키 복구: `key = ciphertext XOR knownplaintext`. 반복키면 키 길이 주기로 같은 바이트가 반복되어 드러남(주기 짧게 정렬해 키 확정).
4) 목적에 따라: (복호) 복구한 키로 전체 XOR → 평문. (위조) 원하는 평문을 같은 키로 재암호화 후 다시 인코딩해 제출.

## PoC
```
python3 - <<'PY'
import base64
ct = base64.b64decode("<url-decoded base64 cookie>")
known = b'{"showpassword":"no","bgcolor":"#ffffff"}'   # 알려진 기본 평문
key = bytes(c ^ known[i % len(known)] for i, c in enumerate(ct))
print("key(repeat):", key)                              # 반복 구간 관찰 → 실제 키
k = key[:4]                                             # 확정한 키 길이만큼
forge = b'{"showpassword":"yes","bgcolor":"#ffffff"}'
out = bytes(b ^ k[i % len(k)] for i, b in enumerate(forge))
print("forged cookie:", base64.b64encode(out).decode())
PY
```

## Pitfalls
키가 평문보다 짧으면 주기적으로 반복 — 키 길이를 먼저 확정(xortool/육안). 단일바이트 키는 256개 전수. base64/URL/hex 인코딩을 반드시 먼저 벗길 것. 평문 길이 ≥ 키 길이여야 키 전체가 드러남.
