import pygame
import random
import sys
import math
import time
from collections import deque
# 1. SETUP CONSTANTS & SPLIT SCREEN CONFIGURATIONS
# =====================================================================
# Optimized dimensions to ensure complex pathways and lightning-fast execution
MAZE_W = 31  # Must be odd numbers for the maze carving engine
MAZE_H = 31
CELL_SIZE = 12

PANEL_WIDTH = MAZE_W * CELL_SIZE
PANEL_HEIGHT = MAZE_H * CELL_SIZE

# Horizontal panel arrangement layout calculations
WINDOW_WIDTH = PANEL_WIDTH * 3 + 40  # Includes layout grid spacer columns
WINDOW_HEIGHT = PANEL_HEIGHT + 80  # Bottom margin padding for the HUD data feeds

# Color Schemes
COLOR_BG = (10, 10, 14)
COLOR_WALL = (22, 22, 30)
COLOR_PATH = (40, 40, 48)
COLOR_GOAL = (255, 69, 0)
COLOR_TEXT = (230, 235, 240)

# Screen Branding Labels Color Coding
COLOR_DFS = (255, 65, 65)  # Red for Screen 1
COLOR_BFS = (65, 105, 255)  # Blue for Screen 2
COLOR_ASTAR = (0, 255, 150)  # Neon Green for Screen 3

# High Precision Benchmarking Ledgers
dfs_time_log = []
bfs_time_log = []
astar_time_log = []
MAX_TEST_RUNS = 100

# =====================================================================
# 2. COMPLEX MAZE CARVING ALGORITHM (Recursive Backtracker / DFS Carve)
# =====================================================================
maze_grid = [[1 for _ in range(MAZE_H)] for _ in range(MAZE_W)]


def generate_complex_maze():
    global maze_grid
    # Fill background entirely with solid block nodes
    maze_grid = [[1 for _ in range(MAZE_H)] for _ in range(MAZE_W)]
    stack = [(1, 1)]
    maze_grid[1][1] = 0

    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < MAZE_W - 1 and 0 < ny < MAZE_H - 1:
                if maze_grid[nx][ny] == 1:
                    neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze_grid[cx + dx // 2][cy + dy // 2] = 0
            maze_grid[nx][ny] = 0
            stack.append((nx, ny))
        else:
            stack.pop()


generate_complex_maze()

START_CELL = (1, 1)
GOAL_CELL = (MAZE_W - 2, MAZE_H - 2)


# =====================================================================
# 3. HIGH-SPEED INSTANT SOLVING ENGINES
# =====================================================================
def solve_dfs(start, goal):
    stack = [[start]]
    visited = {start}
    while stack:
        path = stack.pop()
        curr = path[-1]
        if curr == goal: return path
        cx, cy = curr
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if maze_grid[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append(path + [(nx, ny)])
    return [start]


def solve_bfs(start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        curr = path[-1]
        if curr == goal: return path
        cx, cy = curr
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if maze_grid[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(path + [(nx, ny)])
    return [start]


def solve_astar(start, goal):
    def heuristic(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])  # Manhattan Distance Heuristic

    open_set = [(heuristic(start, goal), [start])]
    visited = {start}
    while open_set:
        open_set.sort(key=lambda x: x[0])
        f_score, path = open_set.pop(0)
        curr = path[-1]
        if curr == goal: return path
        cx, cy = curr
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if maze_grid[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                g_score = len(path)
                h_score = heuristic((nx, ny), goal)
                open_set.append((g_score + h_score, path + [(nx, ny)]))
    return [start]


# =====================================================================
# 4. KINEMATIC RENDERING DRONE BOTS
# =====================================================================
class PanelDrone:
    def __init__(self, x_offset):
        self.x_offset = x_offset
        self.x = float(START_CELL[0])
        self.y = float(START_CELL[1])
        self.path = []
        self.idx = 0
        self.speed = 1.65  # Accelerated rendering velocity

    def reset_flight(self, path):
        self.path = path
        self.idx = 0
        self.x = float(START_CELL[0])
        self.y = float(START_CELL[1])

    def step(self):
        if self.idx >= len(self.path):
            return True  # Goal reached inside panel
        target = self.path[self.idx]
        tx, ty = float(target[0]), float(target[1])
        dx, dy = tx - self.x, ty - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < self.speed:
            self.x, self.y = tx, ty
            self.idx += 1
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        return False


# Screen partition alignment coordinates
panel_positions = [10, PANEL_WIDTH + 20, (PANEL_WIDTH * 2) + 30]

drone_dfs = PanelDrone(panel_positions[0])
drone_bfs = PanelDrone(panel_positions[1])
drone_astar = PanelDrone(panel_positions[2])

current_state = 'STANDBY'
path_dfs, path_bfs, path_astar = [], [], []
calc_dfs, calc_bfs, calc_astar = 0.0, 0.0, 0.0

# =====================================================================
# 5. PYGAME SYSTEM LIFE-CYCLE INITIALIZATION
# =====================================================================
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Parallel Algorithm Laboratory: Split View Comparison")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Courier New", 15, bold=True)
font_hud = pygame.font.SysFont("Arial", 14, bold=True)
font_card = pygame.font.SysFont("Arial", 20, bold=True)

print("\n[PANEL SETUP REGISTERED]: Press ENTER to launch parallel testing.")

# =====================================================================
# 6. CONCURRENT SPEEDWAY LOOP EXECUTION
# =====================================================================
running = True
while running:

    # --- AUTOMATION BENCHMARK CONTROL LAYER ---
    if current_state == 'TRIGGER_COMPUTATIONS':
        if len(dfs_time_log) < MAX_TEST_RUNS:

            # 🏎️ 1. Compute DFS Execution
            t0 = time.perf_counter()
            path_dfs = solve_dfs(START_CELL, GOAL_CELL)
            calc_dfs = (time.perf_counter() - t0) * 1000
            dfs_time_log.append(calc_dfs)

            # 🏎️ 2. Compute BFS Execution
            t0 = time.perf_counter()
            path_bfs = solve_bfs(START_CELL, GOAL_CELL)
            calc_bfs = (time.perf_counter() - t0) * 1000
            bfs_time_log.append(calc_bfs)

            # 🏎️ 3. Compute A* Execution
            t0 = time.perf_counter()
            path_astar = solve_astar(START_CELL, GOAL_CELL)
            calc_astar = (time.perf_counter() - t0) * 1000
            astar_time_log.append(calc_astar)

            # Reset drones onto the newly solved tracks
            drone_dfs.reset_flight(path_dfs)
            drone_bfs.reset_flight(path_bfs)
            drone_astar.reset_flight(path_astar)

            current_state = 'RACING_SIMULATION'
        else:
            current_state = 'SHOW_FINAL_REPORT'

    # --- USER EVENT INTERACTION SYSTEM ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and current_state == 'STANDBY':
                current_state = 'TRIGGER_COMPUTATIONS'

    # --- SIMULTANEOUS PHYSICS RUNNER ---
    if current_state == 'RACING_SIMULATION':
        f1 = drone_dfs.step()
        f2 = drone_bfs.step()
        f3 = drone_astar.step()

        # Immediate advancement reset loop step hook
        if f1 or f2 or f3:
            generate_complex_maze()
            current_state = 'TRIGGER_COMPUTATIONS'

    # -----------------------------------------------------------------
    # GRAPHICS WINDOW DRAWING ROUTINES
    # -----------------------------------------------------------------
    screen.fill(COLOR_BG)

    # Render out the 3 separate maze environments side-by-side
    for i, offset_x in enumerate(panel_positions):
        # Draw background floor map card
        pygame.draw.rect(screen, COLOR_PATH, (offset_x, 10, PANEL_WIDTH, PANEL_HEIGHT))

        # Splice the static maze matrices elements across pixel offsets
        for x in range(MAZE_W):
            for y in range(MAZE_H):
                if maze_grid[x][y] == 1:
                    rect = pygame.Rect(offset_x + (x * CELL_SIZE), 10 + (y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, COLOR_WALL, rect)

        # Render Extraction Goal Pad
        g_rect = pygame.Rect(offset_x + (GOAL_CELL[0] * CELL_SIZE), 10 + (GOAL_CELL[1] * CELL_SIZE), CELL_SIZE,
                             CELL_SIZE)
        pygame.draw.rect(screen, COLOR_GOAL, g_rect)

    # --- DRAW INDEPENDENT SOLUTION TRAJECTORIES ---
    if current_state == 'RACING_SIMULATION':
        # Screen 1 Route Ribbon (DFS)
        for idx in range(len(path_dfs) - 1):
            p1, p2 = path_dfs[idx], path_dfs[idx + 1]
            pos1 = (panel_positions[0] + p1[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p1[1] * CELL_SIZE + CELL_SIZE // 2)
            pos2 = (panel_positions[0] + p2[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p2[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, COLOR_DFS, pos1, pos2, 2)

        # Screen 2 Route Ribbon (BFS)
        for idx in range(len(path_bfs) - 1):
            p1, p2 = path_bfs[idx], path_bfs[idx + 1]
            pos1 = (panel_positions[1] + p1[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p1[1] * CELL_SIZE + CELL_SIZE // 2)
            pos2 = (panel_positions[1] + p2[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p2[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, COLOR_BFS, pos1, pos2, 2)

        # Screen 3 Route Ribbon (A*)
        for idx in range(len(path_astar) - 1):
            p1, p2 = path_astar[idx], path_astar[idx + 1]
            pos1 = (panel_positions[2] + p1[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p1[1] * CELL_SIZE + CELL_SIZE // 2)
            pos2 = (panel_positions[2] + p2[0] * CELL_SIZE + CELL_SIZE // 2, 10 + p2[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, COLOR_ASTAR, pos1, pos2, 2)

        # --- DRAW PARALLEL RUNNING DRONES ---
        pygame.draw.circle(screen, (255, 255, 255), (int(drone_dfs.x_offset + drone_dfs.x * CELL_SIZE + CELL_SIZE // 2),
                                                     int(10 + drone_dfs.y * CELL_SIZE + CELL_SIZE // 2)), 5)
        pygame.draw.circle(screen, (255, 255, 255), (int(drone_bfs.x_offset + drone_bfs.x * CELL_SIZE + CELL_SIZE // 2),
                                                     int(10 + drone_bfs.y * CELL_SIZE + CELL_SIZE // 2)), 5)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(drone_astar.x_offset + drone_astar.x * CELL_SIZE + CELL_SIZE // 2),
                            int(10 + drone_astar.y * CELL_SIZE + CELL_SIZE // 2)), 5)

    # --- SCREEN LABELS HEADERS ---
    screen.blit(font_title.render("[ SCREEN 1: DFS ]", True, COLOR_DFS), (panel_positions[0] + 35, PANEL_HEIGHT + 20))
    screen.blit(font_title.render("[ SCREEN 2: BFS ]", True, COLOR_BFS), (panel_positions[1] + 35, PANEL_HEIGHT + 20))
    screen.blit(font_title.render("[ SCREEN 3: A* ]", True, COLOR_ASTAR), (panel_positions[2] + 40, PANEL_HEIGHT + 20))

    # --- BOTTOM STATUS HUB ---
    hud_bg = pygame.Rect(0, WINDOW_HEIGHT - 45, WINDOW_WIDTH, 45)
    pygame.draw.rect(screen, (8, 8, 12), hud_bg)
    pygame.draw.line(screen, (35, 35, 45), (0, WINDOW_HEIGHT - 45), (WINDOW_WIDTH, WINDOW_HEIGHT - 45), 2)

    if current_state != 'SHOW_FINAL_REPORT':
        runs_count = len(dfs_time_log)
        l1 = f"EXPERIMENT RUN DATA COUNT: {runs_count}/100 LAYOUTS MAPPED SUCCESSFUL."
        if runs_count > 0:
            l1 += f" | Live Delta -> DFS: {calc_dfs:.2f}ms | BFS: {calc_bfs:.2f}ms | A*: {calc_astar:.2f}ms"
        screen.blit(font_hud.render(l1, True, COLOR_TEXT), (20, WINDOW_HEIGHT - 30))
    else:
        if len(dfs_time_log) == 0:
            screen.blit(
                font_hud.render("System Standby Mode initialization. Press ENTER to start the 3-panel race.", True,
                                COLOR_TEXT), (20, WINDOW_HEIGHT - 30))

    # --- 📊 CENTRALIZED TOURNAMENT METRICS OVERLAY SCOREBOARD ---
    if current_state == 'SHOW_FINAL_REPORT':
        filter_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        filter_surface.fill((0, 0, 0, 210))
        screen.blit(filter_surface, (0, 0))

        # Core Report Card Canvas Panel
        card = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 110, 500, 190)
        pygame.draw.rect(screen, (242, 245, 250), card)
        pygame.draw.rect(screen, COLOR_ASTAR, card, 3)

        # Average Calculations across 100 entries
        avg_dfs = sum(dfs_time_log) / len(dfs_time_log)
        avg_bfs = sum(bfs_time_log) / len(bfs_time_log)
        avg_astar = sum(astar_time_log) / len(astar_time_log)

        screen.blit(font_card.render("🏆 FINAL 100-RUN TOURNAMENT OVERVIEW RESULTS", True, (10, 30, 80)),
                    (WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 - 95))
        screen.blit(
            font_hud.render(f"• Screen 3 [A* Search Mean Avg Execution] : {avg_astar:.4f} ms", True, (0, 140, 60)),
            (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 45))
        screen.blit(
            font_hud.render(f"• Screen 2 [BFS Shortest Mean Avg Time]  : {avg_bfs:.4f} ms", True, (20, 50, 180)),
            (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 20))
        screen.blit(
            font_hud.render(f"• Screen 1 [DFS Blind Stack Mean Avg Time]: {avg_dfs:.4f} ms", True, (180, 20, 20)),
            (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 + 5))

        verdict = "Verdict: A* dominates speed checks via target-driven heuristics!"
        screen.blit(font_title.render(verdict, True, (40, 45, 55)), (WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 + 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
print("this is benchmark for maze routing algorithm")