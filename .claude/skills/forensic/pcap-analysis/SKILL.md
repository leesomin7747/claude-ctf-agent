---
name: pcap-analysis
description: 패킷 캡처에서 아티팩트 추출
---
## When
.pcap(ng) 제공

## Tools
tshark, wireshark

## Procedure
1) 프로토콜 통계
2) 스트림 팔로우
3) 파일/자격증명 추출
4) 플래그

## PoC
```
tshark -r f.pcap -Y http --export-objects http,out/
```

## Pitfalls
TLS는 키 필요; 조각난 페이로드 재조립
