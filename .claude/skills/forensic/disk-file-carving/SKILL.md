---
name: disk-file-carving
description: 디스크·파일에서 삭제/은닉 복원
---
## When
디스크 이미지·손상 파일

## Tools
foremost, binwalk, testdisk

## Procedure
1) 파일시스템 확인
2) 카빙
3) 삭제파일 복원
4) 슬랙 검사

## PoC
```
foremost -i disk.img -o out/
```

## Pitfalls
시그니처 겹침·조각 파일
