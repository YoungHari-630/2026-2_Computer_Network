#!/usr/bin/env python3
"""Week 6 · Task 3 — Reconverge without recomputing the world.

Textbook §5.2.1, §5.3.

A link flaps. Every router in the area has to decide what changed. `FullRecompute`
does the honest thing: throw the table away and run Dijkstra again, from scratch,
for every event. It is correct and it is what the first implementations did.

It is also why a single flapping link in a large area used to melt the CPU of
every router that could see it.

Beat it:

    python3 bench.py
    python3 bench.py --yours

Correctness first. `bench.py` compares your table against a full recompute after
**every single event**. A router that is fast and wrong black-holes traffic.
"""
import heapq

# The harness counts how many times you run a full SPF. This is the score:
# wall-clock time in Python says more about dictionary overhead than about
# routing, but "how many times did the CPU have to recompute the world" is
# exactly what melted real routers.
SPF_RUNS = 0
LAST_DISTANCES = {}
LAST_PARENTS = {}


def dijkstra_table(graph, source):
    """Reference shortest-path-first. Returns {destination: first_hop}.

    Use THIS function whenever you need a full recompute. Rolling your own to
    dodge the counter is not an optimisation, it is cheating the meter.
    """
    global SPF_RUNS, LAST_DISTANCES, LAST_PARENTS
    SPF_RUNS += 1
    best = {source: (0, None)}
    parents = {}
    pq, done = [(0, source, None)], set()
    while pq:
        cost, node, first_hop = heapq.heappop(pq)
        if node in done:
            continue
        done.add(node)
        best[node] = (cost, first_hop)
        for nbr, w in sorted(graph[node].items()):
            if nbr in done:
                continue
            hop = nbr if node == source else first_hop
            if cost + w < best.get(nbr, (float("inf"), None))[0]:
                best[nbr] = (cost + w, hop)
                parents[nbr] = node
                heapq.heappush(pq, (cost + w, nbr, hop))
    LAST_DISTANCES = {d: value[0] for d, value in best.items()}
    LAST_PARENTS = parents
    return {d: h for d, (_, h) in best.items() if d != source and h}


class FullRecompute:
    """On every event, forget everything and run SPF again."""

    def __init__(self, graph, source):
        self.graph = {n: dict(e) for n, e in graph.items()}
        self.source = source
        self.table = dijkstra_table(self.graph, source)

    def link_change(self, a, b, cost):
        """cost=None means the link went down."""
        if cost is None:
            self.graph[a].pop(b, None)
            self.graph[b].pop(a, None)
        else:
            self.graph[a][b] = cost
            self.graph[b][a] = cost
        self.table = dijkstra_table(self.graph, self.source)


class YourRouter:
    """Your router. Same two methods, same table, less work per event.

    What is actually true after one link changes:

      * most destinations are not affected at all
      * a link that is not on any of your shortest paths, going *up*, can only
        matter if it creates something shorter
      * a link going *down* only matters if you were using it

    Deciding which of those applies, cheaply, without getting it wrong, is the
    task. Getting it wrong is worse than being slow - the harness will catch it
    on the event where it happens.
    """

    def __init__(self, graph, source):
        global LAST_DISTANCES, LAST_PARENTS
        self.graph = {n: dict(edges) for n, edges in graph.items()}
        self.source = source
        self.table = dijkstra_table(self.graph, source)
        self.distances, self.parents = dict(LAST_DISTANCES), dict(LAST_PARENTS)

    def _recompute(self):
        global LAST_DISTANCES, LAST_PARENTS
        # The scored forwarding table always comes from the supplied reference SPF.
        self.table = dijkstra_table(self.graph, self.source)
        self.distances, self.parents = dict(LAST_DISTANCES), dict(LAST_PARENTS)

    def link_change(self, a, b, cost):
        old_cost = self.graph[a].get(b)
        if old_cost == cost:
            return
        tree_edges = {frozenset((node, parent)) for node, parent in self.parents.items()}
        is_tree_edge = frozenset((a, b)) in tree_edges

        if cost is None:
            self.graph[a].pop(b, None)
            self.graph[b].pop(a, None)
            # Removing an edge outside the selected shortest-path tree cannot
            # invalidate any currently installed route.
            if is_tree_edge:
                self._recompute()
            return

        self.graph[a][b] = cost
        self.graph[b][a] = cost
        if is_tree_edge:
            self._recompute()
            return

        # An added or cheaper non-tree edge matters only if it can create a
        # shorter route. Recompute on equality too, to preserve tie behavior.
        da, db = self.distances.get(a, float("inf")), self.distances.get(b, float("inf"))
        if da + cost <= db or db + cost <= da:
            self._recompute()
