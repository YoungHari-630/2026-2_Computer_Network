# DNS and CDN Steering Report

## Measurement networks

The same 12 sites were measured on both `campus-wifi` and `phone-hotspot`.
On each network, the script queried the system resolver, Google Public DNS
(`8.8.8.8`), and Quad9 (`9.9.9.9`). All 72 site/network/resolver result objects
(12 sites × 2 networks × 3 resolvers) contain an address set and no recorded
lookup error.

## Classification rule

The provisional rule compares the last two labels of the original site and the
final CNAME target. If they differ, the rule says `third party`; otherwise it
says `not third party`.

This is only a DNS-name heuristic, not an ownership test. For the actual verdict
I combined the measured CNAME chain with operator documentation. Akamai documents
`edgesuite.net` and `edgekey.net` as its CDN edge-hostname domains, with the latter
resolving onward to `akamaiedge.net`; Fastly documents `map.fastly.net` as a Fastly
traffic-routing hostname; and Netlify describes its globally distributed CDN for
custom domains. Netflix, Wikimedia, and GitHub require separate treatment because
they operate their own delivery or edge infrastructure rather than exposing a
third-party CDN suffix.

The `final zone` column is the suffix displayed by the provisional rule. The
`chain length` is the number of CNAME hops. Adobe had two hops in most observations
and one additional `akamaitech.net` hop in the phone-hotspot/system observation,
so it is shown as `2–3`.

| site | chain length | final zone | CDN-hosted? | actual third party? | provisional rule | address sets differed? |
|---|---:|---|---|---|---|---|
| `www.microsoft.com` | 2 | `akamaiedge.net` | yes, Akamai CDN | yes | third party — correct | yes |
| `www.netflix.com` | 1 | `netflix.com` | yes, Netflix Open Connect | no, own CDN | not third party — correct | no |
| `www.adobe.com` | 2–3 | `akamai.net` / `akamaitech.net` | yes, Akamai CDN | yes | third party — correct | yes |
| `www.cnn.com` | 1 | `fastly.net` | yes, Fastly CDN | yes | third party — correct | yes |
| `www.apple.com` | 3 | `akamaiedge.net` | yes, Akamai CDN | yes | third party — correct | yes |
| `www.korea.ac.kr` | 0 | `ac.kr` | no CDN observed | no | not third party — correct | no |
| `www.stanford.edu` | 1 | `netlifyglobalcdn.com` | yes, Netlify CDN | yes | third party — correct | no |
| `www.bbc.co.uk` | 2 | `fastly.net` | yes, Fastly CDN | yes | third party — correct | yes |
| `www.spotify.com` | 1 | `fastly.net` | yes, Fastly CDN | yes | third party — correct | yes |
| `www.github.com` | 1 | `github.com` | yes, GitHub-operated distributed edge delivery | no, own edge/CDN | not third party — correct, but the suffix rule cannot reveal that a CDN is present | yes |
| `www.wikipedia.org` | 1 | `wikimedia.org` | yes, Wikimedia CDN | no, own CDN | third party — **wrong** | no |
| `www.nytimes.com` | 3 | `fastly.net` | yes, Fastly CDN | yes | third party — correct | yes |

### Where the provisional rule fails

`www.wikipedia.org` is the clearest false positive. Its chain ends at
`dyna.wikimedia.org`, so the last-two-label rule sees `wikipedia.org` and
`wikimedia.org` as different and calls the service third-party. However, the
Wikimedia Foundation states that it hosts Wikipedia, and Wikimedia's own technical
documentation states that its SRE Traffic team operates a private global CDN for
Wikipedia and related projects. The domain suffix changed, but the operator did
not; this is an own-CDN case.

The rule also has a different limitation at `www.github.com`: the chain ends at
`github.com`, so the rule correctly says “not third party,” but the suffix alone
does not reveal the distributed delivery system. GitHub describes using GeoDNS to
send requests to the closest region and operating regional network-edge points of
presence. For this lab's broad CDN/replica-steering definition, I classify this as
GitHub's own distributed edge delivery rather than a third-party CDN.

## Resolver and network steering

For each site, I treated its sorted A-record list as one address set and compared
all six observations (three resolvers on two networks). A site counts as different
when at least two distinct address sets appear. Eight of all 12 measured sites
differed: Adobe, Apple, BBC, CNN, GitHub, Microsoft, The New York Times, and Spotify.

`www.korea.ac.kr` is the only site classified as not CDN-hosted, and it did not
vary. Removing it from the denominator leaves 11 CDN-hosted sites; the same eight
sites above showed resolver- or network-dependent address sets.

**8 of 11 CDN-hosted sites answered differently to a different resolver or network.**

The three CDN-hosted sites with no observed address-set difference were Netflix,
Stanford, and Wikipedia. Therefore this measurement supports the existence of DNS
steering for many, but not all, CDN-hosted sites. A non-difference in this short
measurement does not prove that a CDN never steers; the chosen resolvers may have
been mapped to the same replica or address set at the measurement time.

## Wireshark evidence

- Matching query packet: **19**
- Matching response packet: **20**
- Transaction ID in both packets: **`0xe5c4`**
- Delegation response packet: **20**
  - Answer RRs: **0**
  - Authority RRs: **6**
  - Additional RRs: **10**
  - Authority NS names: `c.dns.kr`, `e.dns.kr`, `d.dns.kr`, `g.dns.kr`,
    `f.dns.kr`, and `b.dns.kr`
- Final A-answer response packet: **24**
- Final A address: **`163.152.6.10`**
- Largest DNS response packet: **20**
- Largest response frame length: **383 bytes**

Packet 20 was large because its authority section contained six NS records and its
additional section contained ten glue/address records. A delegation and a final
answer use the same DNS message format, but packet 20 had no answer records and
placed the next nameservers in the authority section, whereas packet 24 placed the
final A record in the answer section.

## Sources used for operator classification

- [Akamai edge-hostname terminology](https://techdocs.akamai.com/edge-hostnames/docs/edge-hn-terminology)
- [Akamai property-hostname example showing `edgekey.net` to `akamaiedge.net`](https://techdocs.akamai.com/property-mgr/reference/modify-property-hostnames)
- [Fastly documentation for `map.fastly.net` routing hostnames](https://www.fastly.com/documentation/guides/concepts/routing-traffic-to-fastly/)
- [Netlify documentation describing its global CDN and custom-domain routing](https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/)
- [Netflix Open Connect overview](https://openconnect.netflix.com/Open-Connect-Overview.pdf)
- [Wikimedia Foundation statement that it hosts Wikipedia](https://wikimediafoundation.org/who-we-are/)
- [Wikimedia SRE Traffic documentation for its private global CDN](https://wikitech.wikimedia.org/wiki/Traffic)
- [GitHub explanation of GeoDNS, closest-region selection, and regional edge sites](https://github.blog/engineering/infrastructure/transit-and-peering-how-your-requests-reach-github/)

## Raw-data note

The complete per-network, per-resolver CNAME hops, timestamps, address sets, and
errors are preserved unchanged in `out/chains.json`.
