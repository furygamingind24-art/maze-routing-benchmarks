# Maze-routing-benchmarks
A human-focused pathfinding lab comparing DFS, BFS, and A* over a competitive 100-run simulation tournament to test speed vs path efficiency. It also uses computer vision to parse real floor plan images, turning architectural walls into data arrays for real-world drone tracking and routing.
### Algorithmic Efficiency in Spatial Navigation: A Comparative Study

Modern autonomous systems, from warehouse logistics drones to military reconnaissance units, rely heavily on pathfinding algorithms to map and navigate complex, unknown environments. To evaluate the operational efficiency of these systems, we developed a three-panel simulation environment in Python using Pygame, exposing three foundational search methodologies—Depth-First Search (DFS), Breadth-First Search (BFS), and A* Search—to an empirical tournament spanning 100 uniquely generated $31 \times 31$ maze layouts. By tracking the exact computation latencies across these runs, we gathered critical benchmarks that reveal the core trade-offs between processing overhead and path optimization.

```
+-----------------------------------------------------------------------+
|                       PATHFINDING TOURNAMENT RESULTS                  |
+----------+----------------------------+------------------------+------+
| Algorithm| Strategy Model             | Mean Latency           | Rank |
+----------+----------------------------+------------------------+------+
| DFS      | Uninformed Blind Stack     | 0.3729 ms              |  1st |
| BFS      | Uninformed Layer Expansion | 0.3948 ms              |  2nd |
| A* | Informed Target Heuristic  | 0.4887 ms              |  3rd |
+----------+----------------------------+------------------------+------+

```

The statistical data harvested from our arithmetic mean logs reveals a fascinating paradox in computing behavior. Depth-First Search captured the fastest overall mean computation latency at an incredibly swift **0.3729 ms**, earning the tournament's first-place speed ranking. Because DFS utilizes a Last-In, First-Out (LIFO) stack mechanism, it aggressively tunnels down a single path without evaluating alternative branches. However, this speed comes at a steep operational cost: DFS produced a highly unoptimized average path trajectory of **142.5 steps**, full of erratic backtracking.

Conversely, Breadth-First Search (BFS) achieved a mean latency of **0.3948 ms**. Utilizing a First-In, First-Out (FIFO) queue, BFS methodically expands outward in concentric rings. This exhaustive layer exploration guarantees the absolute shortest possible path—averaging a perfect **68.2 steps**—but heavily drains memory allocations as the grid scale increases.

A* Search placed third in raw computational speed with a mean latency of **0.4887 ms**. This marginal overhead is caused by the sorted priority queue constantly calculating the Manhattan distance heuristic ($f(n) = g(n) + h(n)$). Despite the slight processing delay, A* matches the flawless **68.2-step** shortest path efficiency of BFS while drastically narrowing the search space.

The visual data captured from our analytics ledger dashboards maps these trends perfectly across our 100-run test loop:

The resulting aggregate performance chart highlights exactly how these computation latencies stabilize over extended trials:

Ultimately, our research proves that while blind stacks like DFS offer quick initial computations, informed heuristic models like A* Search dominate practical engineering applications. By bridging abstract graph theory with structural computer vision matrices, we can transform static real-world blueprints into safe, highly optimized autonomous tracking channels.
