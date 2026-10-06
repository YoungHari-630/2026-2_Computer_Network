# 2026-2 컴퓨터 네트워크 실습

고려대학교 세종캠퍼스 컴퓨터 네트워크 과목의 실습 및 과제 제출을 위한 개인 저장소입니다.

원본 실습 저장소:
`codingchild2424/2026-lecture-network-practice`

교수님이 제공한 실습 코드를 기반으로 각 주차의 과제를 수행하고,
직접 작성한 코드와 측정 결과를 기록합니다.

---

## Week 3 · DNS Hierarchy and CDNs

폴더:

`w03-dns/`

이번 주차에서는 DNS 계층 구조와 CDN의 동작을 실습했습니다.

### Task 1 · Iterative DNS Resolver

Root DNS 서버에서 시작하여 TLD 및 authoritative DNS 서버를 직접 따라가는
iterative DNS resolver를 구현했습니다.

일반 recursive resolver에 전체 질의를 맡기지 않고,
delegation, NS record, glue record, CNAME 등을 직접 처리하도록 구현했습니다.

### Task 2 · DNS / CDN Measurement

Wireshark를 이용하여 실제 DNS query와 response를 캡처하고 분석했습니다.

또한 서로 다른 두 네트워크 환경에서 여러 DNS resolver를 사용하여
CDN의 DNS steering 여부를 측정했습니다.

측정 환경:

- Campus Wi-Fi
- Phone Hotspot

결과 파일은 `w03-dns/out/`에 저장되어 있습니다.

### Task 3 · DNS Cache Improvement

제공된 `BaselineCache`의 문제점을 분석하고,
실제 DNS TTL을 따르는 `YourCache`를 구현했습니다.

Benchmark 결과:

| Cache | Upstream Queries | Hit Rate | Stale |
|---|---:|---:|---:|
| Baseline | 325 | 67.5% | 266 |
| YourCache | 275 | 72.5% | 0 |

TTL을 정확히 적용하여 stale response를 제거하고,
upstream query를 줄였습니다.

---

## Week 3 결과물

`w03-dns/out/`

- `dns.pcapng` — 실제 DNS 패킷 캡처
- `chains.json` — CDN / DNS resolver 측정 데이터
- `report.md` — DNS 및 CDN steering 분석
- `bench.txt` — DNS cache benchmark 결과
- `observation.md` — 각 Task에서 관찰하고 이해한 내용

---

## 제출 전 검사

```bash
cd w03-dns

python3 test_tasks.py
python3 ../check.py w03
