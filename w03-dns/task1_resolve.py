#!/usr/bin/env python3
"""Week 3 · Task 1 — Build your own iterative resolver.

Textbook §2.4.2 - §2.4.3.

`dig +trace` walks root -> TLD -> authoritative for you. In this task you do
that walk yourself: start at a root server, read the delegation it returns,
ask the next server, and keep going until somebody answers authoritatively.

You may shell out to `dig` for the transport, or use a DNS library
(`dnspython` is in the container). Either is fine - what matters is that
*you* follow the delegations rather than letting a tool do it.

    python3 task1_resolve.py www.korea.ac.kr
    python3 task1_resolve.py --verify        # check yourself against dig

Pass condition
--------------
`--verify` resolves five names with your resolver and with `dig`, and the
addresses must agree. A name behind a CDN may legitimately return a different
address each time; the harness compares the *set of authoritative nameservers*
you ended at for those, not the address.
"""
import argparse, random, socket, struct, subprocess, sys

# Root servers. Everything starts here; there is no earlier step.
ROOT_SERVERS = [
    "198.41.0.4",       # a.root-servers.net
    "199.9.14.201",     # b.root-servers.net
    "192.33.4.12",      # c.root-servers.net
]

# (name, kind).  "stable" names must match dig exactly.  "cdn" names are served
# from many replicas and may legitimately give you a different address than dig
# got a second earlier - for those we only require that you reached an answer.
VERIFY_NAMES = [
    ("www.korea.ac.kr", "stable"),
    ("dns.google", "stable"),
    ("en.wikipedia.org", "stable"),
    ("www.stanford.edu", "stable"),
    ("www.microsoft.com", "cdn"),
]


class Resolver:
    """Your iterative resolver.

    The whole point is that you never ask a server to recurse for you.
    You ask one server, it says "not mine, ask over there", and you go there.

    Suggested shape - but it is yours to design:

        resolve(name) -> (address, path)
            address : the A record you ended up with, as a string
            path    : the servers you asked, in order, so you can show your work

    Things you will hit, in roughly this order:

    1.  A delegation gives you NS *names*, sometimes with glue A records and
        sometimes without. No glue means you have to resolve that nameserver's
        name first - which is another walk. Decide what you do there.
    2.  A server may not answer. Try the next one rather than giving up.
    3.  CNAMEs. The answer you get back may be a different name than the one
        you asked for, and you have to start again with that name.
    4.  Loops. Cap your depth.

    If you shell out to dig, the flag you want is `+norecurse`, so that the
    server you ask replies with a delegation instead of doing the work:

        dig @198.41.0.4 www.korea.ac.kr +norecurse
    """

    TIMEOUT = 2.0
    MAX_DEPTH = 20
    MAX_QUERIES = 100

    def resolve(self, name):
        """Resolve an IPv4 address by following DNS referrals ourselves."""
        name = self._normalise_name(name)
        path = []
        address = self._resolve_name(name, path, depth=0, active_names=set())
        return address, path

    def _resolve_name(self, name, path, depth, active_names):
        """Walk root -> delegation -> authoritative for one DNS name.

        This method is also used to resolve an NS hostname when a referral has
        no glue.  Each such call starts at a root server, just like a normal
        iterative resolver would.
        """
        if depth > self.MAX_DEPTH:
            raise RuntimeError("maximum DNS resolution depth exceeded")
        if name in active_names:
            raise RuntimeError(f"DNS name loop detected at {name}")

        active_names = active_names | {name}
        servers = list(ROOT_SERVERS)
        seen_referrals = set()

        while servers:
            if len(path) >= self.MAX_QUERIES:
                raise RuntimeError("maximum number of DNS queries exceeded")

            next_servers = None
            last_error = None

            # A delegation normally supplies several equivalent servers.  A
            # timeout, SERVFAIL, or malformed reply from one must not stop the
            # walk, so try every candidate before giving up.
            for server in servers:
                if len(path) >= self.MAX_QUERIES:
                    raise RuntimeError("maximum number of DNS queries exceeded")
                path.append(server)
                try:
                    response = self._query(server, name)
                except (OSError, ValueError) as exc:
                    last_error = exc
                    continue

                rcode = response["flags"] & 0x000f
                if rcode == 3:  # NXDOMAIN
                    raise LookupError(f"{name} does not exist")
                if rcode != 0:  # SERVFAIL, REFUSED, and other retryable replies
                    last_error = RuntimeError(
                        f"server {server} returned DNS rcode {rcode}")
                    continue

                answer = self._answer_from(response["answers"], name)
                if answer is not None:
                    kind, value = answer
                    if kind == "A":
                        return value
                    # A CNAME changes the question.  Begin a fresh iterative
                    # walk at a root server for the canonical name.
                    return self._resolve_name(
                        value, path, depth + 1, active_names)

                ns_names = [
                    rr[4] for rr in response["authority"] if rr[1] == 2
                ]
                if not ns_names:
                    last_error = RuntimeError(
                        f"server {server} returned neither an answer nor a referral")
                    continue

                # Glue is useful only when it belongs to one of the NS names
                # in this referral.  Ignore unrelated additional A records.
                glue = {ns: [] for ns in ns_names}
                for owner, rtype, _rclass, _ttl, value in response["additional"]:
                    if rtype == 1 and owner in glue:
                        glue[owner].append(value)

                candidates = []
                for ns_name in ns_names:
                    if glue[ns_name]:
                        candidates.extend(glue[ns_name])
                        continue

                    # No glue: resolve the nameserver hostname through its own
                    # root-to-authoritative walk, recording those queries in
                    # the same path because they really went over the wire.
                    try:
                        ns_address = self._resolve_name(
                            ns_name, path, depth + 1, active_names)
                    except (LookupError, OSError, RuntimeError, ValueError) as exc:
                        last_error = exc
                        continue
                    candidates.append(ns_address)

                # Preserve DNS order while removing duplicate addresses.
                candidates = list(dict.fromkeys(candidates))
                if not candidates:
                    continue

                referral = (name, tuple(candidates))
                if referral in seen_referrals:
                    raise RuntimeError(f"delegation loop detected for {name}")
                seen_referrals.add(referral)
                next_servers = candidates
                break

            if next_servers is not None:
                servers = next_servers
                continue

            detail = f": {last_error}" if last_error else ""
            raise RuntimeError(f"all DNS server candidates failed for {name}{detail}")

        raise RuntimeError(f"no DNS servers available for {name}")

    @staticmethod
    def _normalise_name(name):
        name = name.strip().rstrip(".").lower()
        if not name or len(name.encode("idna")) > 253:
            raise ValueError("invalid DNS name")
        return name

    @staticmethod
    def _answer_from(records, question):
        """Return ("A", address) or ("CNAME", target) from an answer section."""
        current = question
        seen = set()
        followed_cname = False
        while current not in seen:
            seen.add(current)
            for owner, rtype, _rclass, _ttl, value in records:
                if owner == current and rtype == 1:
                    return "A", value
            for owner, rtype, _rclass, _ttl, value in records:
                if owner == current and rtype == 5:
                    current = value
                    followed_cname = True
                    break
            else:
                if followed_cname:
                    return "CNAME", current
                return None

        raise RuntimeError(f"CNAME loop detected at {current}")

    def _query(self, server, name):
        """Send one non-recursive A query, using TCP if UDP is truncated."""
        query_id = random.SystemRandom().randrange(0x10000)
        packet = self._make_query(query_id, name)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(self.TIMEOUT)
            sock.sendto(packet, (server, 53))
            data, source = sock.recvfrom(65535)
        if source[0] != server:
            raise ValueError("DNS response came from an unexpected server")

        response = self._parse_response(data, query_id)
        if response["flags"] & 0x0200:  # TC: retry the same query over TCP
            data = self._query_tcp(server, packet)
            response = self._parse_response(data, query_id)
        return response

    def _query_tcp(self, server, packet):
        with socket.create_connection((server, 53), self.TIMEOUT) as sock:
            sock.settimeout(self.TIMEOUT)
            sock.sendall(struct.pack("!H", len(packet)) + packet)
            size = struct.unpack("!H", self._recv_exact(sock, 2))[0]
            return self._recv_exact(sock, size)

    @staticmethod
    def _recv_exact(sock, size):
        chunks = []
        remaining = size
        while remaining:
            chunk = sock.recv(remaining)
            if not chunk:
                raise OSError("DNS TCP connection closed early")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    @classmethod
    def _make_query(cls, query_id, name):
        # flags=0 means RD (recursion desired) is deliberately not set.
        header = struct.pack("!HHHHHH", query_id, 0, 1, 0, 0, 0)
        question = cls._encode_name(name) + struct.pack("!HH", 1, 1)
        return header + question

    @staticmethod
    def _encode_name(name):
        wire = bytearray()
        for label in name.split("."):
            encoded = label.encode("idna")
            if not encoded or len(encoded) > 63:
                raise ValueError("invalid DNS label")
            wire.append(len(encoded))
            wire.extend(encoded)
        wire.append(0)
        return bytes(wire)

    @classmethod
    def _read_name(cls, packet, offset):
        labels = []
        end = None
        jumps = 0

        while True:
            if offset >= len(packet):
                raise ValueError("truncated DNS name")
            length = packet[offset]
            if length & 0xc0 == 0xc0:
                if offset + 1 >= len(packet):
                    raise ValueError("truncated DNS compression pointer")
                pointer = ((length & 0x3f) << 8) | packet[offset + 1]
                if pointer >= len(packet):
                    raise ValueError("invalid DNS compression pointer")
                if end is None:
                    end = offset + 2
                offset = pointer
                jumps += 1
                if jumps > 30:
                    raise ValueError("DNS compression pointer loop")
                continue
            if length & 0xc0:
                raise ValueError("invalid DNS label length")

            offset += 1
            if length == 0:
                break
            if offset + length > len(packet):
                raise ValueError("truncated DNS label")
            labels.append(packet[offset:offset + length].decode("ascii").lower())
            offset += length

        return ".".join(labels), end if end is not None else offset

    @classmethod
    def _parse_response(cls, packet, expected_id):
        if len(packet) < 12:
            raise ValueError("truncated DNS header")
        query_id, flags, qd, an, ns, ar = struct.unpack("!HHHHHH", packet[:12])
        if query_id != expected_id or not (flags & 0x8000):
            raise ValueError("invalid DNS response")

        offset = 12
        for _ in range(qd):
            _name, offset = cls._read_name(packet, offset)
            if offset + 4 > len(packet):
                raise ValueError("truncated DNS question")
            offset += 4

        sections = []
        for count in (an, ns, ar):
            records = []
            for _ in range(count):
                owner, offset = cls._read_name(packet, offset)
                if offset + 10 > len(packet):
                    raise ValueError("truncated DNS resource record")
                rtype, rclass, ttl, rdlength = struct.unpack(
                    "!HHIH", packet[offset:offset + 10])
                offset += 10
                rdata_offset = offset
                offset += rdlength
                if offset > len(packet):
                    raise ValueError("truncated DNS record data")

                value = packet[rdata_offset:offset]
                if rtype == 1 and rclass == 1 and rdlength == 4:
                    value = socket.inet_ntoa(value)
                elif rtype in (2, 5):  # NS or CNAME
                    value, _unused = cls._read_name(packet, rdata_offset)
                records.append((owner, rtype, rclass, ttl, value))
            sections.append(records)

        return {
            "flags": flags,
            "answers": sections[0],
            "authority": sections[1],
            "additional": sections[2],
        }


# ------------------------------------------------------------------- harness
def dig_answer(name):
    """What the system resolver says, for comparison."""
    out = subprocess.run(["dig", "+short", name, "A"],
                         capture_output=True, text=True).stdout
    return [l for l in out.split() if l and l[0].isdigit()]


def verify():
    r, failures = Resolver(), 0
    for name, kind in VERIFY_NAMES:
        try:
            addr, path = r.resolve(name)
        except NotImplementedError:
            print("Nothing implemented yet - write Resolver.resolve first.")
            return 1
        except Exception as e:
            print(f"  FAIL  {name:<22} your resolver raised {e!r}")
            failures += 1
            continue
        expected = dig_answer(name)
        if addr in expected:
            note = ""
        elif kind == "cdn":
            note = "  <- differs, but this name is CDN-hosted. Explain it."
        else:
            note = "  <- should have matched"
            failures += 1
        print(f"  {'FAIL' if note.endswith('matched') else 'ok  '}  {name:<22} "
              f"you={addr:<16} dig={','.join(expected) or '-'}   "
              f"hops={len(path)}{note}")
    print(f"\n  {len(VERIFY_NAMES) - failures}/{len(VERIFY_NAMES)} ok")
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", nargs="?", default="www.korea.ac.kr")
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()

    if a.verify:
        sys.exit(verify())

    addr, path = Resolver().resolve(a.name)
    for i, server in enumerate(path, 1):
        print(f"  {i}. asked {server}")
    print(f"\n  {a.name} -> {addr}")


if __name__ == "__main__":
    main()
