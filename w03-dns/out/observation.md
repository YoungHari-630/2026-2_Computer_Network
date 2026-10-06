## Task 1
- The iterative resolver started at root server `198.41.0.4`; the root returned a delegation to the next NS level rather than a final A record because it was not authoritative for `www.korea.ac.kr`.
- The actual lookup followed `198.41.0.4` → `210.101.61.1` → authoritative server `163.152.11.6` and returned `163.152.6.10` after three DNS-server queries.
- For glue-less referrals, the resolver starts a separate root-to-authoritative lookup for each NS hostname; in the observed `www.stanford.edu` run, seven such lookups took three queries each, adding 21 DNS queries to the shared path.

## Task 2
- Query packet 19 and delegation response packet 20 shared transaction ID `0xe5c4`; packet 20 had 0 answer, 6 authority, and 10 additional records, making it the largest response at 383 bytes because it carried six NS records and ten glue/address records.
- Final answer packet 24 contained the A record `163.152.6.10`, showing that a delegation places the next NS records in the authority section while a final answer places the address in the answer section.
- Across `campus-wifi` and `phone-hotspot`, 8 of 11 CDN-hosted sites returned different address sets; the suffix rule wrongly labeled `www.wikipedia.org` → `dyna.wikimedia.org` as third-party even though Wikimedia operates its own CDN.

## Task 3
- The baseline made 325 upstream queries with a 67.5% hit rate and 266 stale answers; the TTL-aware cache reached 275 upstream queries, a 72.5% hit rate, and zero stale answers.
- The baseline's fixed 60-second lifetime caused stale answers for short-TTL records and unnecessary refreshes for long-TTL records; `www.microsoft.com` was the worst correctness case because its 20-second TTL was extended to 60 seconds, producing 189 stale answers.
- The theoretical floor is 275 because every name's first request and the first request after each TTL expiration must obtain a fresh upstream answer; going lower would require serving an expired or nonexistent cached answer.
