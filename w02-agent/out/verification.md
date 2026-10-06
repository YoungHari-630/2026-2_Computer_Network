# Task 2 Manual Verification

Each claim in the six rows of `analysis.md` was compared with the corresponding file in `materials/`. Lecture slides were not available in the repository, so slide comparisons remain manual checks.

| Row | Claim checked | Correct? | Where confirmed |
|---|---|---|---|
| 1a — RFC 9112 / HTTP/1.1 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9112`; title `HTTP/1.1`. |
| 1b — RFC 9112 / HTTP/1.1 | Year | Correct | Document header: `June 2022`. |
| 1c — RFC 9112 / HTTP/1.1 | Key mechanism claim | Correct | Sections 2.1 (message format), 6.1–6.3 (message framing), 7.1 (chunked transfer coding), and 9.3 (persistent connections). |
| 1d — RFC 9112 / HTTP/1.1 | “What it gave up” claim | Correct | Section 9.3.2 requires pipelined responses to be sent in request order and says a client should not pipeline after a non-idempotent method until its final response arrives. |
| 1e — RFC 9112 / HTTP/1.1 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/1.1 slides manually. |
| 2a — RFC 9113 / HTTP/2 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9113`; title `HTTP/2`. |
| 2b — RFC 9113 / HTTP/2 | Year | Correct | Document header: `June 2022`. |
| 2c — RFC 9113 / HTTP/2 | Key mechanism claim | Correct | Sections 1 and 2 describe binary framing, one stream per exchange, multiplexing, flow control, prioritization, and compressed fields; Sections 4.3 and 8.2 identify HPACK field compression. |
| 2d — RFC 9113 / HTTP/2 | “What it gave up” claim | Correct | Section 1 explicitly says TCP head-of-line blocking is not addressed. Section 2 explicitly describes server push as trading network usage for a potential latency gain. |
| 2e — RFC 9113 / HTTP/2 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/2 slides manually. |
| 3a — RFC 9114 / HTTP/3 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9114`; title `HTTP/3`. |
| 3b — RFC 9114 / HTTP/3 | Year | Correct | Document header: `June 2022`. |
| 3c — RFC 9114 / HTTP/3 | Key mechanism claim | Correct | Sections 1.2 and 2 describe QUIC stream multiplexing, per-stream reliability and flow control, connection-wide congestion control, one stream per request/response, and QPACK replacing HPACK. |
| 3d — RFC 9114 / HTTP/3 | “What it gave up” claim | Correct | Section 3.1 states that blocking UDP can prevent a QUIC connection and that clients should attempt a TCP-based HTTP version. |
| 3e — RFC 9114 / HTTP/3 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/3 slides manually. |
| 4a — RFC 9000 / QUIC | RFC number or document identifier | Correct | Document header: `Request for Comments: 9000`; title `QUIC: A UDP-Based Multiplexed and Secure Transport`. |
| 4b — RFC 9000 / QUIC | Year | Correct | Document header: `May 2021`. |
| 4c — RFC 9000 / QUIC | Key mechanism claim | Correct | Section 1 describes the integrated TLS/transport handshake, optional 0-RTT, protected QUIC packets in UDP datagrams, flow-controlled streams, and connection-ID-based migration. |
| 4d — RFC 9000 / QUIC | “What it gave up” claim | Correct | Section 1 says only clients can migrate in QUIC v1. Section 21.5 says the spoofed-migration attack lacks adequate countermeasures and that QUIC v1 does not allow server migration. |
| 4e — RFC 9000 / QUIC | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the QUIC slides manually. |
| 5a — Langley et al. SIGCOMM paper | Document identifier/title | Correct | PDF page 1 gives the exact title, author list, SIGCOMM ’17 citation, and DOI `10.1145/3098822.3098842`. |
| 5b — Langley et al. SIGCOMM paper | Year | Correct | PDF page 1 states `2017` in the ACM reference and `SIGCOMM ’17, August 21–25, 2017`. |
| 5c — Langley et al. SIGCOMM paper | Key mechanism claim | Correct | Sections 1 and 3, PDF pages 1 and 3: user-space UDP transport, encrypted packets, combined handshakes, independent streams, and connection IDs are described directly. |
| 5d — Langley et al. SIGCOMM paper | “What it gave up” claim | Correct | Section 6.7, PDF page 10 reports optimized server CPU cost at approximately twice TLS/TCP. Section 7.2, PDF page 11 reports 4.4% unable to use QUIC because QUIC/UDP was blocked or the path MTU was too small. |
| 5e — Langley et al. SIGCOMM paper | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare the paper’s motivation, mechanisms, and measured limitations with the QUIC slides manually. |
| 6a — Chromium QUIC overview | Document identifier/title | Correct | YAML document header: `title: QUIC, a multiplexed transport over UDP`. |
| 6b — Chromium QUIC overview | Year | Incorrect (unsupported) | The document header and body contain no author or publication date. Dates in “Abridged QUIC Version History” date protocol events, not this document. `analysis.md` correctly warned that the year was unverified, but it does not supply the required verified year. |
| 6c — Chromium QUIC overview | Key mechanism claim | Correct | Opening paragraphs and “Key features of QUIC and HTTP/3 over TCP+TLS and HTTP/2” list UDP transport, encrypted transport functionality, reduced setup time, multiplexing without cross-stream head-of-line blocking, migration, extensibility, and optional unreliable delivery. |
| 6d — Chromium QUIC overview | “What it gave up” claim | Incorrect (unsupported) | No explicit implementation cost or design trade-off appears in the saved document. The analysis cell is an `(unverified)` absence note rather than a source-supported “what it gave up” claim. |
| 6e — Chromium QUIC overview | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare the overview’s benefit claims with the QUIC slides manually. |

## Per-row result

| Analysis row | At least one error? | Worst error found | How it was found |
|---|---|---|---|
| 1 — RFC 9112 / HTTP/1.1 | No | None found in the checked claims. | Header and Sections 2.1, 6.1–6.3, 7.1, 9.3, and 9.3.2. |
| 2 — RFC 9113 / HTTP/2 | No | None found in the checked claims. | Header and Sections 1, 2, 4.3, and 8.2. |
| 3 — RFC 9114 / HTTP/3 | No | None found in the checked claims. | Header and Sections 1.2, 2, and 3.1. |
| 4 — RFC 9000 / QUIC | No | None found in the checked claims. | Header and Sections 1 and 21.5. |
| 5 — Langley et al. SIGCOMM paper | No | None found in the checked claims. | PDF title page and Sections 1, 3, 6.7, and 7.2. |
| 6 — Chromium QUIC overview | Yes | The required year and “what it gave up” fields are unsupported by this source. | The complete 121-line document has no publication metadata or explicit trade-off statement. |

**1 of 6 rows contained at least one error.**

## 한국어 설명

위 영어 표와 판정은 원문 그대로 유지했습니다. 아래 내용은 표의 의미를 이해하기 위한 보충 설명이며, 판정이나 근거를 새로 변경하지 않습니다.

### 판정 용어

- `Correct`: 해당 주장을 지정된 원문 위치에서 확인할 수 있다는 뜻입니다.
- `Incorrect (unsupported)`: 주장을 뒷받침하는 직접적인 근거를 해당 원문에서 확인할 수 없다는 뜻입니다. 반드시 사실 자체가 거짓이라는 의미는 아닙니다.
- `Manual check required`: 저장소에 강의 슬라이드가 없어 원문과 강의자료의 모순 여부를 판정하지 못했다는 뜻입니다. 이 상태는 모든 lecture slide 항목에서 그대로 유지됩니다.
- `At least one error?`: 한 행의 여러 검사항목 중 하나라도 오류가 있으면 `Yes`로 표시합니다.

### 행별 해설

1. **RFC 9112 / HTTP/1.1** — 문서 번호와 2022년 발행일, 메시지 형식·프레이밍·청크 전송·지속 연결에 관한 설명이 원문에서 확인되었습니다. 파이프라이닝 응답이 요청 순서를 따라야 하는 제약도 직접 확인되어 모든 source claim이 `Correct`입니다.
2. **RFC 9113 / HTTP/2** — 이진 프레이밍, 스트림 다중화, 흐름 제어, 우선순위 및 HPACK 압축 설명이 원문과 일치합니다. TCP 수준의 head-of-line blocking을 해결하지 못한다는 점과 서버 푸시가 네트워크 사용량과 지연 시간 사이의 교환관계를 만든다는 점도 직접 근거가 있어 `Correct`입니다.
3. **RFC 9114 / HTTP/3** — QUIC 스트림 다중화, 스트림별 신뢰성과 흐름 제어, 연결 전체 혼잡 제어 및 QPACK 설명이 확인되었습니다. UDP가 차단되면 QUIC 연결이 실패할 수 있고 TCP 기반 HTTP를 시도해야 한다는 제한도 원문에 있어 `Correct`입니다.
4. **RFC 9000 / QUIC** — TLS와 전송 계층의 통합 핸드셰이크, 선택적 0-RTT, UDP 기반 보호 패킷, 스트림 및 연결 ID 기반 이동 기능이 확인되었습니다. QUIC v1에서 서버 이동을 허용하지 않는 제한과 그 보안 배경도 확인되어 `Correct`입니다.
5. **Langley et al. SIGCOMM 논문** — 제목, 저자, 2017년 학회 정보와 DOI가 논문 첫 페이지에 있습니다. QUIC의 핵심 구조뿐 아니라 최적화된 서버 CPU 비용이 TLS/TCP의 약 두 배였다는 결과와 4.4%가 UDP 차단 또는 작은 path MTU로 QUIC을 사용하지 못했다는 측정 결과도 확인되어 `Correct`입니다.
6. **Chromium QUIC overview** — 제목과 핵심 기능 설명은 원문에서 확인되어 `Correct`입니다. 그러나 문서 자체의 발행연도와 명시적인 구현 비용·설계 trade-off는 원문에서 찾을 수 없어 각각 `Incorrect (unsupported)`로 판정되었습니다. 버전 연혁의 날짜는 프로토콜 사건의 날짜이지 문서 발행일이 아니므로 발행연도 근거로 사용할 수 없습니다.

### 최종 결과 해설

첫 번째 검증에서는 6개 분석 행 가운데 Chromium QUIC overview 행에 발행연도와 trade-off 관련 미지원 주장이 포함되어 있었습니다. 따라서 영어 결론인 **`1 of 6 rows contained at least one error.`**는 **6개 행 중 1개 행에 하나 이상의 오류가 있었다**는 뜻입니다. 강의 슬라이드 비교는 자료 부재로 이 오류 수에 확정 판정으로 반영되지 않았으며, 계속 `Manual check required`로 남습니다.
