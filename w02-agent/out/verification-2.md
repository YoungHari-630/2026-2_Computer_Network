# Task 3 Second Verification

Each claim in the six rows of `analysis-2.md` was checked again against the corresponding file in `materials/`. Lecture slides were not available in the repository, so slide comparisons remain manual checks.

| Row | Claim checked | Correct? | Where confirmed |
|---|---|---|---|
| 1a — RFC 9112 / HTTP/1.1 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9112`; title `HTTP/1.1`. |
| 1b — RFC 9112 / HTTP/1.1 | Year | Correct | Document header: `June 2022`. |
| 1c — RFC 9112 / HTTP/1.1 | Key mechanism claim | Correct | Sections 2.1, 6.1–6.3, 7.1, and 9.3 describe the textual format, framing precedence, chunked coding, and persistent connections cited in the analysis. |
| 1d — RFC 9112 / HTTP/1.1 | “What it gave up” claim | Correct | Section 9.3.2 requires pipelined responses in request order and restricts pipelining after a non-idempotent method until its final response. |
| 1e — RFC 9112 / HTTP/1.1 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/1.1 slides manually. |
| 2a — RFC 9113 / HTTP/2 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9113`; title `HTTP/2`. |
| 2b — RFC 9113 / HTTP/2 | Year | Correct | Document header: `June 2022`. |
| 2c — RFC 9113 / HTTP/2 | Key mechanism claim | Correct | Sections 1, 2, 4.1, 4.3, 5, 5.2, and 8.2 support binary framing, multiplexed streams, flow control, and HPACK field compression. |
| 2d — RFC 9113 / HTTP/2 | “What it gave up” claim | Correct | Section 1 states that TCP head-of-line blocking is not addressed. Section 2 states that server push trades network usage for a possible latency gain. |
| 2e — RFC 9113 / HTTP/2 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/2 slides manually. |
| 3a — RFC 9114 / HTTP/3 | RFC number or document identifier | Correct | Document header: `Request for Comments: 9114`; title `HTTP/3`. |
| 3b — RFC 9114 / HTTP/3 | Year | Correct | Document header: `June 2022`. |
| 3c — RFC 9114 / HTTP/3 | Key mechanism claim | Correct | Sections 1.2 and 2 support the QUIC mapping, stream multiplexing, per-stream reliability and flow control, connection-wide congestion control, integrated TLS, and QPACK. |
| 3d — RFC 9114 / HTTP/3 | “What it gave up” claim | Correct | Section 3.1 states that UDP blocking can prevent a QUIC connection and recommends attempting a TCP-based HTTP version. |
| 3e — RFC 9114 / HTTP/3 | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the HTTP/3 slides manually. |
| 4a — RFC 9000 / QUIC | RFC number or document identifier | Correct | Document header: `Request for Comments: 9000`; title `QUIC: A UDP-Based Multiplexed and Secure Transport`. |
| 4b — RFC 9000 / QUIC | Year | Correct | Document header: `May 2021`. |
| 4c — RFC 9000 / QUIC | Key mechanism claim | Correct | Section 1 supports integrated TLS and transport negotiation, optional 0-RTT, protected packets over UDP, flow-controlled streams, and connection-ID-based migration. |
| 4d — RFC 9000 / QUIC | “What it gave up” claim | Correct | Section 1 limits migration to clients in QUIC v1. Section 21.5 connects the exclusion of server migration to spoofed-migration request forgery and inadequate countermeasures. |
| 4e — RFC 9000 / QUIC | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare with the QUIC slides manually. |
| 5a — Langley et al. SIGCOMM paper | Document identifier/title | Correct | PDF page 1 contains the exact title, authors, SIGCOMM ’17 reference, and DOI `10.1145/3098822.3098842`. |
| 5b — Langley et al. SIGCOMM paper | Year | Correct | PDF page 1 identifies the paper as 2017 and dates SIGCOMM ’17 to August 21–25, 2017. |
| 5c — Langley et al. SIGCOMM paper | Key mechanism claim | Correct | Sections 1 and 3 on PDF pages 1–3 support user-space UDP, encrypted transport, combined setup, independent streams, and connection IDs. |
| 5d — Langley et al. SIGCOMM paper | “What it gave up” claim | Correct | Section 6.7 on PDF page 10 reports optimized server CPU cost at about twice TLS/TCP; Section 7.2 on PDF page 11 reports that 4.4% could not use QUIC because of blocking or insufficient path MTU. |
| 5e — Langley et al. SIGCOMM paper | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare the paper’s motivation, mechanisms, and measurements with the QUIC slides manually. |
| 6a — Chromium QUIC overview | Document identifier/title | Correct | YAML header: `title: QUIC, a multiplexed transport over UDP`. |
| 6b — Chromium QUIC overview | Year recorded as `not stated (unverified)` | Correct | The complete document has no author or publication-date metadata. Dates under “Abridged QUIC Version History” describe protocol events rather than this document’s publication, so the analysis correctly avoids inferring a year. |
| 6c — Chromium QUIC overview | Key mechanism claim | Correct | The opening paragraphs and “Key features of QUIC and HTTP/3 over TCP+TLS and HTTP/2” directly list UDP, encrypted transport functionality, reduced setup time, improved congestion feedback, cross-stream multiplexing, migration, extensibility, and optional unreliable delivery. |
| 6d — Chromium QUIC overview | Trade-off recorded as `unsupported` | Correct | The complete document states benefits and links to other material but gives no explicit implementation cost, restriction, trade-off, or fallback. The phrase “no such limitations” describes a claimed benefit, not a cost; `unsupported` is therefore the appropriate entry. |
| 6e — Chromium QUIC overview | Contradicts a lecture slide? | Manual check required | Lecture slides were not available; compare the overview’s claims with the QUIC slides manually. |

## Per-row result

| Analysis row | At least one error? | Verification result | Evidence checked |
|---|---|---|---|
| 1 — RFC 9112 / HTTP/1.1 | No | All checked source claims are supported. | Header and Sections 2.1, 6.1–6.3, 7.1, 9.3, and 9.3.2. |
| 2 — RFC 9113 / HTTP/2 | No | All checked source claims are supported. | Header and Sections 1, 2, 4.1, 4.3, 5, 5.2, and 8.2. |
| 3 — RFC 9114 / HTTP/3 | No | All checked source claims are supported. | Header and Sections 1.2, 2, and 3.1. |
| 4 — RFC 9000 / QUIC | No | All checked source claims are supported. | Header and Sections 1 and 21.5. |
| 5 — Langley et al. SIGCOMM paper | No | All checked source claims are supported. | PDF page 1 and Sections 1, 3, 6.7, and 7.2 on pages 1–3, 10, and 11. |
| 6 — Chromium QUIC overview | No | The supported claims are accurate, and absent year/trade-off evidence is explicitly marked rather than inferred. | YAML header, opening paragraphs, key-features list, version history, and complete-document absence check. |

**0 of 6 rows contained at least one error.**

## 한국어 설명

위 영어 표와 판정은 원문 그대로 유지했습니다. 아래 내용은 두 번째 검증 결과를 이해하기 위한 보충 설명이며, 판정이나 근거를 새로 변경하지 않습니다.

### 판정 용어

- `Correct`: 해당 주장 또는 미확인 표기가 원문의 실제 내용과 일치한다는 뜻입니다.
- `not stated (unverified)`: 문서에 발행연도가 명시되어 있지 않아 추측하지 않고 “명시되지 않음(검증 불가)”으로 기록했다는 뜻입니다.
- `unsupported`: 원문에서 직접적인 근거를 찾지 못했으므로 내용을 만들어 채우지 않고 “근거 없음”으로 표시했다는 뜻입니다.
- `Manual check required`: 저장소에 강의 슬라이드가 없어 원문과 강의자료의 모순 여부를 판정하지 못했다는 뜻입니다. 이 상태는 모든 lecture slide 항목에서 그대로 유지됩니다.
- `At least one error?`: 한 행의 여러 검사항목 중 하나라도 오류가 있는지를 나타냅니다. 두 번째 검증에서는 모든 행이 `No`입니다.

### 행별 해설

1. **RFC 9112 / HTTP/1.1** — 문서 번호, 2022년 발행일, 텍스트 기반 형식, 프레이밍 우선순위, 청크 전송 및 지속 연결 설명이 확인되었습니다. 요청 순서대로 응답해야 하는 파이프라이닝 제약도 원문과 일치하므로 모든 source claim이 `Correct`입니다.
2. **RFC 9113 / HTTP/2** — 이진 프레이밍, 다중화 스트림, 흐름 제어 및 HPACK 압축이 지정된 절에서 확인되었습니다. TCP head-of-line blocking이 남는다는 점과 서버 푸시의 네트워크 사용량·지연 시간 trade-off도 직접 확인되어 `Correct`입니다.
3. **RFC 9114 / HTTP/3** — QUIC 매핑, 스트림 다중화, 스트림별 신뢰성과 흐름 제어, 연결 전체 혼잡 제어, 통합 TLS 및 QPACK 설명이 원문과 일치합니다. UDP 차단 시 TCP 기반 HTTP 버전을 시도해야 한다는 제한도 확인되어 `Correct`입니다.
4. **RFC 9000 / QUIC** — TLS와 전송 협상의 통합, 선택적 0-RTT, UDP 위의 보호 패킷, 흐름 제어 스트림 및 연결 ID 기반 이동 설명이 확인되었습니다. QUIC v1에서 서버 이동을 제외한 이유도 보안상 spoofed-migration 문제와 함께 확인되어 `Correct`입니다.
5. **Langley et al. SIGCOMM 논문** — 제목·저자·2017년 학회 정보·DOI 및 핵심 QUIC 구조가 확인되었습니다. 최적화된 서버 CPU 비용이 TLS/TCP의 약 두 배였다는 측정과 4.4%가 차단 또는 불충분한 path MTU 때문에 QUIC을 사용할 수 없었다는 결과도 원문과 일치하여 `Correct`입니다.
6. **Chromium QUIC overview** — 제목과 핵심 기능은 원문에서 확인되었습니다. 문서에 발행일이 없으므로 `not stated (unverified)`라고 기록한 것이 올바르며, 명시적인 구현 비용·제약·trade-off·fallback이 없으므로 `unsupported`라고 기록한 것도 올바릅니다. 즉, 첫 번째 분석에서 근거 없이 채워졌던 두 필드를 두 번째 분석에서는 추측하지 않고 명확히 표시했기 때문에 이 행도 오류가 없는 것으로 판정되었습니다.

### 첫 번째 검증과의 차이

첫 번째 `verification.md`에서는 Chromium 행의 발행연도와 trade-off가 원문으로 뒷받침되지 않아 그 행이 오류로 판정되었습니다. `analysis-2.md`에서는 발행연도를 `not stated (unverified)`, trade-off를 `unsupported`로 명시해 원문에 없는 내용을 추론하지 않았습니다. 그 결과 두 번째 검증의 영어 결론인 **`0 of 6 rows contained at least one error.`**는 **6개 행 모두 확인된 source claim 범위에서 오류가 없었다**는 뜻입니다.

강의 슬라이드 비교는 두 번째 검증에서도 수행되지 않았습니다. 따라서 source claim의 오류 수가 0이더라도 모든 lecture slide 항목은 계속 `Manual check required`이며, 강의자료와의 최종 비교는 별도로 사람이 확인해야 합니다.
