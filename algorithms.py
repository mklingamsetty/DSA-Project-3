from worldSettings import *
from collections import deque
from PIL import Image, ImageDraw
import time

# This file will contain the algorithms used for finding the shortest path between the player and the home

def BFS(image, draw, tile_map):
    
    # Breadth First Search Algorithm
    # This algorithm will find the shortest path between the player and the home
    # The algorithm will return a list of coordinates (x, z) that represent the path from the player to the home
    # The algorithm will return None if no path is found
    # The algorithm will return None if the player is already at the home
    # The algorithm will return None if the home is blocked by obstacles
    # The algorithm will return None if the home is unreachable from the player's position

    # The algorithm will use a queue to keep track of the nodes to visit
    # Implemention of the BFS algorithm here
    rows = len(tile_map)
    cols = len(tile_map[0])

    # Find the player's and home's position
    start = None
    goal = []
    for i in range(rows):
        for j in range(cols):
            if tile_map[i][j] == 'P':  # 'P' represents the player
                start = (i, j)
            elif tile_map[i][j] == 'H':  # 'H' represents the home
                goal.append((i, j))

    if start is None or goal is None:
        return None  # Player or home not found

    if start in goal:
        return None  # Player is already at home

    queue = deque([start])
    visited = set([start])
    parent = {}

    # Possible movements: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()
        if current in goal:
            # Reconstruct the path
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)

            # Reverse the path to get the correct order from start to goal
            path.reverse()
            return path  # List of tuples from start to goal
        
        last_save_time = time.time()
        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                if tile_map[neighbor[0]][neighbor[1]] != 'O' and neighbor not in visited:  # 'O' represents obstacles
                    queue.append(neighbor)
                    visited.add(neighbor)
                    draw.point((world_size - neighbor[0] - 1, neighbor[1]), fill=(128, 0, 128, 255))
                    
                    current_time = time.time()
                    if current_time - last_save_time >= 5:
                        image.save("minimap.png")
                        last_save_time = current_time
                    parent[neighbor] = current
 
    return None  # No path found

def DFS(image, draw, tile_map):
    # Depth First Search Algorithm
    # This algorithm will find the shortest path between the player and the home
    # The algorithm will return a list of coordinates (x, z) that represent the path from the player to the home
    # The algorithm will return None if no path is found
    # The algorithm will return None if the player is already at the home
    # The algorithm will return None if the home is blocked by obstacles
    # The algorithm will return None if the home is unreachable from the player's position

    # The algorithm will use a stack to keep track of the nodes to visit
    # Implemention of the DFS algorithm here
    rows = len(tile_map)
    cols = len(tile_map[0])

    # Find the player's and home's position
    start = None
    goal = []
    for i in range(rows):
        for j in range(cols):
            if tile_map[i][j] == 'P':  # 'P' represents the player
                start = (i, j)
            elif tile_map[i][j] == 'H':  # 'H' represents the home
                goal.append((i, j))

    if start is None or goal is None:
        return None  # Player or home not found

    if start in goal:
        return None  # Player is already at home

    stack = [start]
    visited = set([start])
    parent = {}

    # Possible movements: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()
        if current == goal:
            # Reconstruct the path
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)

            # Reverse the path to get the correct order from start to goal
            path.reverse()
            return path  # List of tuples from start to goal

        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                if tile_map[neighbor[0]][neighbor[1]] != 'O' and neighbor not in visited:  # 'O' represents obstacles
                    stack.append(neighbor)
                    visited.add(neighbor)
                    #fill will be purple
                    draw.point((world_size - neighbor[0] - 1, neighbor[1]), fill=(128, 0, 128, 255))
                    parent[neighbor] = current
                    
    return None  # No path found

