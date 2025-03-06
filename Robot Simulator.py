import pygame
import random
from heapq import heappush, heappop

# Kích thước lưới
GRID_SIZE = 6
CELL_SIZE = 100
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Màu sắc
WHITE = (255, 255, 255)  # Chưa lau
GREEN = (0, 255, 0)      # Đã lau
BLACK = (0, 0, 0)        # Chướng ngại vật
BLUE = (0, 0, 255)       # Robot

# Khởi tạo màn hình Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mô phỏng Robot Lau Nhà")

# Thuật toán heuristic Manhattan cho A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* tìm đường đi ngắn nhất từ start đến goal
def a_star(start, goal, obstacles):
    open_set = []
    heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    came_from = {}
    closed_set = set()

    while open_set:
        _, g, current = heappop(open_set)
        if current in closed_set:
            continue
        closed_set.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        r, c = current
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            neighbor = (nr, nc)
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and neighbor not in obstacles:
                tentative_g = g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heappush(open_set, (f_score, tentative_g, neighbor))
    return None

# Tạo chướng ngại vật ngẫu nhiên
obstacle_count = 5
obstacles = set()
while len(obstacles) < obstacle_count:
    r = random.randint(0, GRID_SIZE - 1)
    c = random.randint(0, GRID_SIZE - 1)
    if (r, c) != (0, 0):
        obstacles.add((r, c))

# Robot bắt đầu tại góc trên trái
robot_pos = (0, 0)

# Lưu danh sách các ô đã lau
cleaned = {robot_pos}

# Tìm tất cả ô cần lau
all_cleanable_cells = {(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if (r, c) not in obstacles}

# Hàm tìm ô chưa lau gần nhất
def find_nearest_dirty_cell(current_pos):
    dirty_cells = all_cleanable_cells - cleaned
    if not dirty_cells:
        return None
    return min(dirty_cells, key=lambda cell: heuristic(current_pos, cell))

# Lặp đến khi mọi ô sạch
path = []
running = True
while running:
    if cleaned == all_cleanable_cells:
        running = False
        continue

    if not path:
        next_target = find_nearest_dirty_cell(robot_pos)
        if next_target:
            path = a_star(robot_pos, next_target, obstacles)
        else:
            running = False
            continue

    if path:
        robot_pos = path.pop(0)
        cleaned.add(robot_pos)

    screen.fill(WHITE)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (r, c) in obstacles:
                pygame.draw.rect(screen, BLACK, rect)
            elif (r, c) in cleaned:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    robot_x = robot_pos[1] * CELL_SIZE + CELL_SIZE // 2
    robot_y = robot_pos[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, BLUE, (robot_x, robot_y), CELL_SIZE // 2 - 5)

    pygame.display.flip()
    pygame.time.delay(300)

pygame.quit()