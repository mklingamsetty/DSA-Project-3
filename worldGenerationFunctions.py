from ursina import *
import random
from worldSettings import *
from textures import *
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image, ImageDraw
from collections import deque

class GameScreen:
    def __init__(self):
        self.settings = worldSettings()
        self.player_spawn_x = self.settings.get_player_spawn_x()
        self.player_spawn_z = self.settings.get_player_spawn_z()
        self.player_speed = self.settings.get_player_speed()
       
        # Store all block positions in a set (unique blocks with unique positions)
        self.block_positions = {}
        
        # 2D map of obstacle positions and free spaces
        self.tile_map = []
        
        # Generate the Home
        self.home_tile_positions = homeGeneration(self)
        
        # Sets and lists to store unique obstacle positions
        self.obstacle_positions = set()
        self.cluster_locations = []
        self.single_locations = []
        
        # Generate Cluster Obstacles
        clusterGeneration(self.home_tile_positions, self.obstacle_positions, self.cluster_locations, self.settings)
        
        # Generate Single Obstacles
        singlesGeneration(self.obstacle_positions, self.home_tile_positions, self.single_locations, self.settings)
          
        # Generate the map
        generateMap(self.tile_map, self.block_positions, self.obstacle_positions, self.home_tile_positions, self.settings)

        while (self.player_spawn_x, self.player_spawn_z) in self.obstacle_positions:
            self.player_spawn_x += 1  # Adjust as necessary

        # initialize the player controller
        self.player=FirstPersonController(
        mouse_sensitivity=Vec2(100, 100), # Mouse sensitivity
        position=(self.player_spawn_x, 7, self.player_spawn_z), # Player spawn position
        speed=self.player_speed # Player movement speed
        )

        self.current_position = (int(self.player_spawn_x), int(self.player_spawn_z))
        
        self.MiniMap = Entity(
            parent=camera.ui,
            model='quad',
            position=(0.6, 0.35),
            scale=(0.3, 0.3)
        )
        # Now starting at the bottomLeft corner of the MiniMap, we will use the tile_map 2D List to draw on the MiniMap
        # The MiniMap will be a 2D representation of the tile_map so the beginning of the tile_map will start on the 
        # bottom left, moving towards the right and once it reaches the end 
        # of 1 row in tile_map, it will move up to the next row in tile_map
        self.image = Image.new('RGB', (self.settings.get_world_size(), self.settings.get_world_size()), color=(0, 0, 0, 0))
        self.colorMap = []
        draw_minimap(self.image, self.tile_map, self.colorMap, self.settings)
        self.MiniMap.texture = "minimap.png"
        self.draw = ImageDraw.Draw(self.image)
        self.map = None
        self.texture_counter = 0

        self.mini_block = Entity(
            parent=camera,
            model="minecraft_starter/assets/models/Torch",
            texture=block_textures.get("torch"),
            scale= 0.2,
            position=(0.35, -0.25, 0.5),
            rotation=(-15, -30, -5)
        )


    def setMap(self, map_entity):
        self.map = map_entity
   
    def BFS(self):
        print("algorithm started")
        tile_map = self.tile_map
        image = self.image
        draw = self.draw
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
            print(f"Current: {current}")
            if current in goal:
                # Reconstruct the path
                self.image.save("minimapAlgorithmVisitedBFS.png")

                path = []
                while current != start:
                    path.append(current)
                    current = parent[current]
                path.append(start)

                # Reverse the path to get the correct order from start to goal
                path.reverse()
                print("algorithm complete")
                
                for x, z in path:
                    draw.point((self.settings.get_world_size() - x - 1, z), fill=(0, 0, 255, 255))
                self.image.save("minimapAlgorithmPathBFS.png")

                return path  # List of tuples from start to goal

            for d in directions:
                neighbor = (current[0] + d[0], current[1] + d[1])
                print(f"Neighbor: {neighbor}")
                if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                    if tile_map[neighbor[0]][neighbor[1]] != 'O' and neighbor not in visited:  # 'O' represents obstacles
                        queue.append(neighbor)
                        visited.add(neighbor)
                        parent[neighbor] = current
                        draw.point((self.settings.get_world_size() - neighbor[0] - 1, neighbor[1]), fill=(128, 0, 128, 255))
        print("No path found")
        return None  # No path found

    def DFS(self):
        print("DFS algorithm started")
        tile_map = self.tile_map
        image = self.image
        draw = self.draw
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
            print(f"Current: {current}")
            if current in goal:
                self.image.save("minimapAlgorithmVisitedDFS.png")
                # Reconstruct the path
                path = []
                while current != start:
                    path.append(current)
                    current = parent[current]
                path.append(start)

                # Reverse the path to get the correct order from start to goal
                path.reverse()
                print("DFS algorithm complete")
                
                for x, z in path:
                    draw.point((self.settings.get_world_size() - x - 1, z), fill=(0, 0, 255, 255))
                self.image.save("minimapAlgorithmPathDFS.png")
                print("DFS algorithm complete")
                return path  # List of tuples from start to goal

            for d in directions:
                neighbor = (current[0] + d[0], current[1] + d[1])
                if (0 <= neighbor[0] < rows) and (0 <= neighbor[1] < cols):
                    if tile_map[neighbor[0]][neighbor[1]] != 'O' and neighbor not in visited:  # 'O' represents obstacles
                        stack.append(neighbor)
                        visited.add(neighbor)
                        #fill will be purple
                        draw.point((self.settings.get_world_size() - neighbor[0] - 1, neighbor[1]), fill=(128, 0, 128, 255))
                        parent[neighbor] = current
                        
        return None  # No path found
            
# Block class
class Block(Entity):
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1), block_type="grass", **kwargs):
        if block_type == "zombie":
            model = "minecraft_starter/assets/models/AnyConv.com__zombie.obj"
            texture = mob_textures.get("zombie")
        elif block_type == "enderman":
            model = "minecraft_starter/assets/models/AnyConv.com__enderman.obj"
            texture = mob_textures.get("enderman")
        elif block_type == "creeper":
            model = "minecraft_starter/assets/models/AnyConv.com__creeper.obj"
            texture = mob_textures.get("creeper")
        elif block_type == "skeleton":
            model = "minecraft_starter/assets/models/AnyConv.com__skeleton.obj"
            texture = mob_textures.get("skeleton")
        else:
            model = "minecraft_starter/assets/models/block_model"
            texture = block_textures.get(block_type)

        super().__init__(
            position=position,
            scale=scale,
            origin_y=0.5,
            model=model,
            texture=texture,
            collider='box',
            **kwargs  # Allow additional parameters to be passed
        )
        self.block_type = block_type

# Draw the texture for the MiniMap
def draw_minimap(image, tile_map, colorMap, settings):
    
    colorChar = ''
    draw = ImageDraw.Draw(image)
    for x in range(settings.get_world_size()):
        row = []
        for z in range(settings.get_world_size()):
            if tile_map[x][z] == "O":
                color = (255, 0, 0, 255)  # Red
                colorChar = 'R'
            elif tile_map[x][z] == "H":
                color = (139, 69, 19, 255)  # Brown
                colorChar = 'B'
            elif tile_map[x][z] == "P":
                color = (255, 192, 203, 255)  # Pink
                colorChar = 'P'
            else:
                color = (0, 255, 0, 255)  # Green
                colorChar = 'G'
            #draw.point((world_size - x - 1, world_size - z - 1), fill=color)
            draw.point((settings.get_world_size() - x - 1, z), fill=color)
            row.append(colorChar)
        colorMap.append(row)
    #image = image.transpose(Image.ROTATE_90)
    
    image.save("minimap.png")
    print("MiniMap Created")

# Generate Home Structure
def homeGeneration(self):
    home_tile_positions = []
    x = random.randint(self.settings.get_home_min_z(), self.settings.get_home_max_z())
    z = random.randint(0, self.settings.get_world_size() - self.settings.get_home_size() - 10)
    for dx in range(self.settings.get_home_size()):
        for dz in range(self.settings.get_home_size()):
            home_tile_positions.append((x + dx, z + dz))
    return home_tile_positions

# Generate Cluster Obstacles
def clusterGeneration(home_tile_positions, obstacle_positions, cluster_locations, settings):
    # Place 3x3 clusters of obstacles
    for i in range(settings.get_num_clusters()):
        placed = False
        while not placed:
            # Declaring the cluster position to be inside of the world and not outside of it
            x = random.randint(0, settings.get_world_size() - 3) # x pos
            z = random.randint(0, settings.get_world_size() - 3) # z pos
            obstacleType = random.randint(1, 3) # Randomly select the obstacle type
            
            # create a vector<pair<int, int>> equivalent to mark the cluster obstacle positions
            cluster_positions = [(x + dx, z + dz) for dx in range(3) for dz in range(3)]
            # print(cluster_positions)
            # Creates a 3x3 cluster starting at the randomly generated x and z positions
            # Now using a nested for loop, we marks the clustered position 3 in the x from the start and 3 in the z from the start
            
            # cluster_positions in C++: vector<pair<int, int>> cluster_positions = {{x, z}, {x + 1, z}, {x + 2, z}, 
            #                                                                       {x, z + 1}, {x + 1, z + 1}, {x + 2, z + 1}, 
            #                                                                       {x, z + 2}, {x + 1, z + 2}, {x + 2, z + 2}};
            # Now we need to check if any of the coordinates in cluster_positions are already occupied by an obstacle
            if all((cx, cz) not in obstacle_positions and home_tile_positions for (cx, cz) in cluster_positions):
                # if all the coordinates in cluster_positions are not in obstacle_positions
                # meaning now the obstacle cluster CAN be placed
                
                # Then I should Add the cluster positions to the obstacle set
                obstacle_positions.update(cluster_positions)
                cluster_locations.append((cluster_positions, obstacleType))
                placed = True

# Generate Single Obstacles
def singlesGeneration(obstacle_positions, home_tile_positions, single_locations, settings):
    # Place single tile obstacles
    while len(obstacle_positions) < settings.get_total_obstacles(): # Remaining obstacles will be single tiled
        # Declare world bounds for the obstacles
        x = random.randint(0, settings.get_world_size() - 1)
        z = random.randint(0, settings.get_world_size() - 1)
        obstacleType = random.randint(1, 5) # Randomly select the obstacle type
        
        # If the position is not already taken by an obstacle, add it to the obstacle set
        if (x, z) not in obstacle_positions and (x, z) not in home_tile_positions:
            obstacle_positions.add((x, z))
            single_locations.append(((x, z), obstacleType))

# Generate the Map
def generateMap(tile_map, block_positions, obstacle_positions, home_tile_positions, settings):
        # Initialize the tile map
    for x in range(settings.get_world_size()):
        row = [] #declare a row to store the tile status (Free Space or Obstacle) (True or False)
        for z in range(settings.get_world_size()):
            position = (x, -5, z)
            is_free_space = (x, z) not in obstacle_positions
            block_positions[position] = is_free_space
            if x == settings.get_player_spawn_x() and z == settings.get_player_spawn_z():
                row.append("P") # P for Player
            elif is_free_space:
                row.append("F") # F for Free Space
            elif (x, z) in home_tile_positions:
                row.append("H") # H for Home
            else:
                row.append("O") # O for Obstacle
        tile_map.append(row)

def colorMap(algorithm, colorMap, path):
    if algorithm == "BFS":
        color = (0, 0, 255, 255) # Blue
    elif algorithm == "DFS":
        color = (0, 255, 0, 255) # Green
    for x, z in path:
        colorMap[x][z] = color
    return colorMap