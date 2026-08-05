---
name: stego
description: 이미지·오디오 은닉 데이터 추출
---
## When
미디어 파일·"보이는게 다가아님"

## Tools
binwalk, steghide, zsteg, exiftool

## Procedure
1) 메타/`binwalk`
2) LSB·팔레트
3) `steghide`(암호)
4) 스펙트로그램

## PoC
```
binwalk -e img.png; zsteg img.png
```

## Pitfalls
암호 필요 시 사전공격; 다중 계층
