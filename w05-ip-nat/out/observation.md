# Observations

## Task 1
`/31` returns both addresses as usable under RFC 3021; `/32` returns its single address as both first and last. The four 10.x matches for `10.20.30.70` were `/8`, `/16`, `/24`, and `/26`; the default `/0` also matched but lost.
Same-length duplicate routes replace the prior next hop (latest add wins); malformed CIDRs with host bits or prefix lengths outside 0–32 raise `ValueError`.

## Task 2
The two private addresses changed from `192.168.0.39/24` (gateway `.1`) to `10.30.108.202/24` (gateway `.237`), while both checks showed public `39.127.67.13`; shared public egress is consistent with upstream NAT, but does not reveal the number of NAT layers.
The capture confirms DORA: Discover was `0.0.0.0:68 → 255.255.255.255:67`; the Offer from `10.30.108.237` offered a 3,600-second lease for `10.30.108.202`. ACK was broadcast in this trace, though it can be unicast once the server knows the client's address and link-layer destination and the client's broadcast flag allows it.

## Task 3
`YourTable` groups routes into hash maps by prefix length, using O(R) route storage plus at most 33 maps; it checks only distinct installed lengths in descending order, so lookup is O(L), with L ≤ 33.
The 20,000-query benchmark matched every linear answer and ran 1,183.3× faster; a bit trie bounds lookup to 32 steps and suits fixed hardware datapaths, while Python hash maps have lower interpreter overhead here.
