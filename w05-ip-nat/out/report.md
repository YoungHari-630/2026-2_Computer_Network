# Week 05 · Address study

## A · Current network

On the first network Windows reported Wi-Fi IPv4 `192.168.0.39`, subnet mask
`255.255.255.0` (`/24`), default gateway and DHCP server `192.168.0.1`, and a
two-hour lease window (16:16:18–18:16:18 on Oct 20, 2026). The subnet is
`192.168.0.0/24`: network `.0`, usable range `.1`–`.254`, broadcast `.255`.
The gateway `.1` is in that subnet, so the host can reach it directly on the
local link. Task 1's `network_range` uses the same network and usable range.

`192.168.0.39` is RFC 1918 private space. The user checked the public address
from both networks and reported `39.127.67.13` each time. Both private
addresses therefore share the same observed public egress address, which is
consistent with translation at one or more upstream NAT gateways. Equal
public addresses alone do not identify how many NAT layers there are; a VPN or
proxy, or a shared upstream gateway, could also explain the same egress.

## B · Second network

On the second network Windows reported `10.30.108.202/24`, gateway and DHCP
server `10.30.108.237`, and a one-hour lease window (16:35:11–17:35:10). Its
subnet is `10.30.108.0/24`, usable range `.1`–`.254`, broadcast `.255`; the
gateway is on-link. Compared with the first network, the private address and
gateway changed while the mask stayed `/24`. The reported public address stayed
`39.127.67.13`, so both networks presented the same egress IP during the checks.
To distinguish a single NAT from carrier-grade or nested NAT, compare the
router or phone's WAN address with `39.127.67.13`; a WAN address in
`100.64.0.0/10` indicates carrier-grade NAT upstream.

## C · DHCP

The capture contains Discover, Offer, Request and ACK with transaction ID
`0xc55b42da`, confirming DORA. Discover is
`0.0.0.0:68 → 255.255.255.255:67`: the client has no configured address and
does not yet know the server, so it broadcasts. The Offer comes from
`10.30.108.237:67` to `255.255.255.255:68` and offers `10.30.108.202`; its
DHCP lease-time option is 3,600 seconds (one hour). The ACK in this capture is
also broadcast (its lease option is 3,599 seconds). An ACK can be unicast when
the server knows the offered address and the client's link-layer address, and
the client can accept unicast before configuring its address; the client’s
broadcast flag affects this choice.
