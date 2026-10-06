#!/usr/bin/env python3
"""Week 3 · Task 2 — Does DNS actually steer you? Measure it.

Textbook §2.4.3 (records) and §2.5 (CDNs).

The lecture claims two things:

    (a) most large sites are served by a CDN, reached through a CNAME chain
    (b) DNS steers each user to a *nearby* replica

Both are testable from your laptop, and one of them is harder to prove than
the slide makes it look. Your job is to produce the evidence and a number.

    python3 task2_steering.py --collect        # gather the raw data
    python3 task2_steering.py --report         # your analysis

What you have to build
----------------------
1.  For each hostname in SITES, follow the CNAME chain to its end and record
    every hop. `--collect` should leave the raw data in out/chains.json.

2.  Decide, for each site, whether it is served by a **third party**.
    This is the hard part and there is no single right answer:

      - `www.microsoft.com` ends at `akamaiedge.net`     - clearly third party
      - `www.netflix.com`   stops inside `netflix.com`   - own CDN, not third party
      - some sites have no CNAME at all and still sit behind a CDN (anycast)
      - `foo.cloudfront.net` and `foo.s3.amazonaws.com` are both Amazon,
        but they are not the same service

    Write down the rule you used and **defend it in observation.md**. A rule
    that just compares the last two labels will be wrong on at least one of
    the sites below; find which, and say so.

3.  Ask **two different resolvers** for the same name and compare the
    addresses you get back. If DNS really steers by location, a CDN-hosted
    name should answer differently to resolvers sitting in different places.

        RESOLVERS below has your system resolver and two public ones.

    Report: of N CDN-hosted sites, how many returned a different address set
    from a different resolver? Claim (b) predicts most of them. Check it.

Pass condition
--------------
There is no fixed answer. You pass by producing, in out/report.md:

  - the table: site | chain length | final zone | third party? | your rule's verdict
  - the steering number: "X of N sites answered differently to a different resolver"
  - at least one site where your classification rule was wrong, and why
"""
import argparse, datetime, ipaddress, json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

SITES = [
    "www.microsoft.com",     # Akamai, multi-hop
    "www.netflix.com",       # own CDN
    "www.adobe.com",
    "www.cnn.com",
    "www.apple.com",
    "www.korea.ac.kr",       # no CDN at all
    "www.stanford.edu",
    "www.bbc.co.uk",
    "www.spotify.com",
    "www.github.com",
    "www.wikipedia.org",
    "www.nytimes.com",
]

RESOLVERS = {
    "system": None,          # whatever is in your resolv.conf
    "google": "8.8.8.8",
    "quad9":  "9.9.9.9",
}

MAX_CNAME_HOPS = 20


def dig(name, rtype="A", server=None):
    """Raw lookup. Transport only - the thinking is yours."""
    args = ["dig", "+short", "+time=3", "+tries=1", name, rtype]
    if server:
        args.insert(1, f"@{server}")
    result = subprocess.run(
        args, capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        detail = result.stderr.strip() or f"dig exited with {result.returncode}"
        raise RuntimeError(detail)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def normalise_name(name):
    return name.strip().rstrip(".").lower()


def ipv4_addresses(lines):
    """Keep only IPv4 results; `dig +short A` may also print CNAMEs."""
    addresses = set()
    for line in lines:
        try:
            address = ipaddress.ip_address(line)
        except ValueError:
            continue
        if address.version == 4:
            addresses.add(str(address))
    return sorted(addresses)


def measure_site(site, server):
    """Follow one resolver's CNAME chain and collect its final A record set."""
    current = normalise_name(site)
    chain = [current]
    seen = {current}

    for _ in range(MAX_CNAME_HOPS):
        targets = [normalise_name(value)
                   for value in dig(current, "CNAME", server)]
        targets = [value for value in targets if value]
        if not targets:
            break

        # A DNS owner normally has only one CNAME.  Keeping the first response
        # is deterministic; recording all hops still exposes what was seen.
        target = targets[0]
        if target in seen:
            raise RuntimeError(f"CNAME loop detected at {target}")
        chain.append(target)
        seen.add(target)
        current = target
    else:
        raise RuntimeError(
            f"CNAME chain exceeded {MAX_CNAME_HOPS} hops for {site}")

    addresses = ipv4_addresses(dig(current, "A", server))
    if not addresses:
        raise RuntimeError(f"no IPv4 address returned for {current}")

    return {
        "chain": chain,
        "cname_hops": [
            {"from": chain[index], "to": chain[index + 1]}
            for index in range(len(chain) - 1)
        ],
        "final_name": current,
        "addresses": addresses,
    }


def collect(network_label):
    """Gather raw chains and per-resolver answers into out/chains.json.

    Reusing a label refreshes only that network.  A different label adds a
    second vantage point without overwriting the first measurement.
    """
    if not shutil.which("dig"):
        raise RuntimeError(
            "dig is not installed; install dnsutils/BIND tools before collecting")

    network_label = network_label.strip()
    if not network_label:
        raise ValueError("network label must not be empty")

    os.makedirs(OUT, exist_ok=True)
    output_path = os.path.join(OUT, "chains.json")
    if os.path.exists(output_path):
        with open(output_path, encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("out/chains.json must contain a JSON object")
    else:
        data = {}

    collected_at = datetime.datetime.now().astimezone().isoformat(
        timespec="seconds")
    for site in SITES:
        site_data = data.setdefault(site, {"networks": {}})
        networks = site_data.setdefault("networks", {})
        measurement = {
            "collected_at": collected_at,
            "resolvers": {},
        }

        for resolver_name, server in RESOLVERS.items():
            try:
                result = measure_site(site, server)
                result["error"] = None
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                # An unreachable public resolver is itself real measurement
                # information.  Preserve it rather than inventing an answer.
                result = {
                    "chain": [normalise_name(site)],
                    "cname_hops": [],
                    "final_name": normalise_name(site),
                    "addresses": [],
                    "error": str(exc),
                }
            measurement["resolvers"][resolver_name] = result

        networks[network_label] = measurement
        print(f"  collected {site} on {network_label}")

    temporary_path = output_path + ".tmp"
    with open(temporary_path, "w", encoding="utf-8", newline="\n") as output:
        json.dump(data, output, indent=2, ensure_ascii=False, sort_keys=True)
        output.write("\n")
    os.replace(temporary_path, output_path)
    print(f"\n  wrote {output_path}")


def final_zone(name):
    """A deliberately simple zone approximation used by the report table."""
    labels = normalise_name(name).split(".")
    return ".".join(labels[-2:]) if len(labels) >= 2 else labels[0]


def measured_networks(data):
    labels = set()
    for site_data in data.values():
        labels.update(site_data.get("networks", {}))
    return sorted(labels)


def address_observations(site_data):
    """Return every non-empty resolver/network address set for one site."""
    observations = []
    for measurement in site_data.get("networks", {}).values():
        for result in measurement.get("resolvers", {}).values():
            addresses = result.get("addresses", [])
            if addresses:
                observations.append(tuple(sorted(addresses)))
    return observations


def addresses_differ(site_data):
    """Compare every non-empty resolver/network address set for one site."""
    return len(set(address_observations(site_data))) > 1


def report():
    """Read out/chains.json and produce out/report.md.

    Measurements are rendered automatically.  Wireshark observations and the
    human CDN/third-party judgement remain explicit TODOs until the student
    has inspected their own traffic and researched the ambiguous cases.
    """
    input_path = os.path.join(OUT, "chains.json")
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            "out/chains.json does not exist; run --collect --network LABEL first")
    with open(input_path, encoding="utf-8") as source:
        data = json.load(source)

    networks = measured_networks(data)
    lines = [
        "# DNS and CDN Steering Report",
        "",
        "## Measurement networks",
        "",
        ", ".join(f"`{name}`" for name in networks)
        if networks else "TODO: collect measurements on two networks.",
        "",
        "## CNAME and third-party review",
        "",
        "The provisional rule below compares the last two labels of the original "
        "site and the final CNAME target. Different suffixes produce a "
        "`third party` verdict. This is only a deliberately simple rule to test; "
        "it cannot detect an own-CDN or a CDN reached without CNAME, and public "
        "suffixes such as `co.uk` make a last-two-label rule especially fragile.",
        "",
        "| site | chain length | final zone | third party? | rule verdict |",
        "|---|---:|---|---|---|",
    ]

    first_network = networks[0] if networks else None
    for site in SITES:
        site_data = data.get(site, {})
        measurement = site_data.get("networks", {}).get(first_network, {})
        resolver_result = measurement.get("resolvers", {}).get("system", {})
        if resolver_result.get("error"):
            resolver_result = next(
                (result for result in measurement.get("resolvers", {}).values()
                 if not result.get("error")),
                resolver_result)
        chain = resolver_result.get("chain", [site])
        final_name = resolver_result.get("final_name", site)
        chain_length = max(0, len(chain) - 1)
        verdict = ("third party" if final_zone(site) != final_zone(final_name)
                   else "not third party")
        lines.append(
            f"| `{site}` | {chain_length} | `{final_zone(final_name)}` | "
            f"TODO: manual review | {verdict} |")

    comparable = [
        site for site in SITES
        if site in data and len(address_observations(data[site])) >= 2
    ]
    changed = sum(addresses_differ(data[site]) for site in comparable)
    lines.extend([
        "",
        "### Classification review still required",
        "",
        "TODO: decide which sites are CDN-hosted and which are third-party. "
        "Identify at least one site where the provisional rule is wrong and explain why.",
        "",
        "## Resolver and network steering",
        "",
    ])
    if len(networks) >= 2:
        lines.append(
            f"Across all measured sites, {changed} of {len(comparable)} had more "
            "than one address set across the resolvers or networks.")
    else:
        lines.append(
            "TODO: collect the second network before comparing resolver/network answers.")
    lines.extend([
        "",
        "Required CDN-only steering number: **TODO: X of N CDN-hosted sites "
        "answered differently to a different resolver or network.**",
        "",
        "## Wireshark evidence",
        "",
        "- Matching query packet number: TODO",
        "- Matching response packet number: TODO",
        "- Transaction ID shown in both packets: TODO",
        "- Delegation response packet number: TODO",
        "- Final A-answer response packet number: TODO",
        "- Largest DNS response size in bytes: TODO",
        "- Why that response was large: TODO",
        "",
        "## Raw-data notes",
        "",
        "Full per-resolver CNAME hops, address sets, timestamps, and lookup "
        "errors are preserved in `out/chains.json`.",
        "",
    ])

    output_path = os.path.join(OUT, "report.md")
    with open(output_path, "w", encoding="utf-8", newline="\n") as output:
        output.write("\n".join(lines))
    print(f"  wrote {output_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    action = p.add_mutually_exclusive_group()
    action.add_argument("--collect", action="store_true")
    action.add_argument("--report", action="store_true")
    p.add_argument(
        "--network", metavar="LABEL",
        help="network label used to preserve separate measurements")
    a = p.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.collect:
        if not a.network:
            p.error("--collect requires --network LABEL")
        collect(a.network)
    elif a.report:
        report()
    else:
        p.print_help()
