## Task 1
- The iterative resolver started at root server `198.41.0.4`; the root returned a delegation to the next NS level rather than a final A record because it was not authoritative for `www.korea.ac.kr`.
- The actual lookup followed `198.41.0.4` → `210.101.61.1` → authoritative server `163.152.11.6` and returned `163.152.6.10` after three DNS-server queries.
- When a referral has no glue A record, the resolver performs a separate root-to-authoritative lookup for the NS hostname, records those real queries in the same path, and then resumes the original lookup with the resolved NS address.

## Task 2
- Query packet 19 and delegation response packet 20 shared transaction ID `0xe5c4`; packet 20 had 0 answer, 6 authority, and 10 additional records, making it the largest response at 383 bytes because it carried six NS records and ten glue/address records.
- Final answer packet 24 contained the A record `163.152.6.10`, showing that a delegation places the next NS records in the authority section while a final answer places the address in the answer section.
- Across `campus-wifi` and `phone-hotspot`, 8 of 11 CDN-hosted sites returned different address sets; the suffix rule wrongly labeled `www.wikipedia.org` → `dyna.wikimedia.org` as third-party even though Wikimedia operates its own CDN.

## Task 3
- The baseline made 325 upstream queries with a 67.5% hit rate and 266 stale answers; the TTL-aware cache reached 275 upstream queries, a 72.5% hit rate, and zero stale answers.
- The baseline's fixed 60-second lifetime caused both correctness errors for records with shorter TTLs and unnecessary refreshes for records with longer TTLs.
- The theoretical floor is 275 because every name's first request and the first request after each TTL expiration must obtain a fresh upstream answer; going lower would require serving an expired or nonexistent cached answer.
