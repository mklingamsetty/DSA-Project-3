from ursina import *
import random
from worldSettings import *
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image, ImageDraw
from collections import deque
import heapq
from ursina.prefabs.health_bar import HealthBar

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
        self.tile_coordinates = []
        
        # Generate the Home
        self.home_tile_positions = homeGeneration(self.settings)
        
        # Sets and lists to store unique obstacle positions
        self.obstacle_positions = set()
        self.cluster_locations = []
        self.single_locations = []
        
        # Generate Cluster Obstacles
        clusterGeneration(self.home_tile_positions, self.obstacle_positions, self.cluster_locations, self.settings)
        
        # Generate Single Obstacles
        singlesGeneration(self.obstacle_positions, self.home_tile_positions, self.single_locations, self.settings)
          
        # Generate the map
        generateMap(self.tile_map, self.tile_coordinates, self.block_positions, self.obstacle_positions, self.home_tile_positions, self.settings)
        
        self.dijkstraDictionary = calculateDijkstraDictionary(self.settings, self.tile_map, self.tile_coordinates, self.single_locations, self.cluster_locations)

        while (self.player_spawn_x, self.player_spawn_z) in self.obstacle_positions:
            self.player_spawn_x += 1  # Adjust as necessary

        # initialize the player controller
        self.player=FirstPersonController(
        mouse_sensitivity=Vec2(100, 100), # Mouse sensitivity
        position=(self.player_spawn_x, -5, self.player_spawn_z), # Player spawn position
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

        self.mini_block = Entity(
            parent=camera,
            model="minecraft_starter/assets/models/Torch",
            texture=self.settings.block_textures.get("torch"),
            scale= 0.2,
            position=(0.35, -0.25, 0.5),
            rotation=(-15, -30, -5)
        )

    def setMap(self, map_entity):
        self.map = map_entity
   
    def BFS(self):
        print("algorithm started")
        tile_map = self.tile_map
        self.bfsMap = Image.new('RGB', (self.settings.get_world_size(), self.settings.get_world_size()), color=(0, 0, 0, 0))
        self.colorMap = []
        draw_minimap(self.bfsMap, self.tile_map, self.colorMap, self.settings)
        self.drawBFS = ImageDraw.Draw(self.bfsMap)
        draw = self.drawBFS
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
        player_x = int(self.player.x)
        player_z = int(self.player.z)
        start = (player_x, player_z)
        goal = []
        for i in range(rows):
            for j in range(cols):
                if tile_map[i][j] == 'H':  # 'H' represents the home
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
                self.bfsMap.save("minimapAlgorithmVisitedBFS.png")

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
                self.bfsMap.save("minimapAlgorithmPathBFS.png")
                self.MiniMap.texture = "minimapAlgorithmpathBFS.png"

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
        player_x = int(self.player.x)
        player_z = int(self.player.z)
        start = (player_x, player_z)
        goal = []
        for i in range(rows):
            for j in range(cols):
                if tile_map[i][j] == 'H':  # 'H' represents the home
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
                self.MiniMap.texture = "minimapAlgorithmpathDFS.png"
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
    
    def dijkstra(self):
        print("algorithm started")
        tile_map = self.tile_map
        rows = len(tile_map)
        cols = len(tile_map[0])
        self.dijkstraMap = Image.new('RGB', (self.settings.get_world_size(), self.settings.get_world_size()), color=(0, 0, 0, 0))
        self.colorMap = []
        draw_minimap(self.dijkstraMap, self.tile_map, self.colorMap, self.settings)
        self.drawDijkstra = ImageDraw.Draw(self.dijkstraMap)
        draw = self.drawDijkstra

        player_x = int(self.player.x)
        player_z = int(self.player.z)
        start = (player_x, player_z)
        goal = []
        for i in range(rows):
            for j in range(cols):
                if tile_map[i][j] == 'H':  # 'H' represents the home
                    goal.append((i, j))
                    break
        print(f"Start: {start}")
        print(f"Goal: {goal}")

        # Priority queue to store (distance, node)
        queue = [(0, start)]
        # Dictionary to store the shortest distance to each node
        distances = {start: 0}
        # Dictionary to store the path
        predecessors = {start: None}
        nearestNode = None
        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_node in goal:
                nearestNode = current_node
                break

            for neighbor, weight in self.dijkstraDictionary.get(current_node, []):
                print(neighbor)
                distance = current_distance + weight

                if neighbor not in distances or distance < distances[neighbor]:
                    print("current_distance: " + str(current_distance) + " current_node: " + str(current_node))
                    draw.point((self.settings.get_world_size() - neighbor[0] - 1, neighbor[1]), fill=(128, 0, 128, 255))
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))
        self.dijkstraMap.save("minimapAlgorithmVisitedDijkstra.png")
        self.MiniMap.texture = "minimapAlgorithmpathDijkstra.png"
        # Reconstruct the shortest path
        path = []
        node = nearestNode
        while node is not None:
            path.append(node)
            node = predecessors[node]
            if node is not None:
                draw.point((self.settings.get_world_size() - node[0] - 1, node[1]), fill=(0, 0, 255, 255))
        self.dijkstraMap.save("minimapAlgorithmPathDijkstra.png")
        path.reverse()
        return path
# Block class
class Block(Entity):
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1), block_type="grass", **kwargs):
        self.settings = worldSettings()
        if block_type == "zombie":
            model = "minecraft_starter/assets/models/AnyConv.com__zombie.obj"
            texture = self.settings.mob_textures.get("zombie")
        elif block_type == "enderman":
            model = "minecraft_starter/assets/models/AnyConv.com__enderman.obj"
            texture = self.settings.mob_textures.get("enderman")
        elif block_type == "creeper":
            model = "minecraft_starter/assets/models/AnyConv.com__creeper.obj"
            texture = self.settings.mob_textures.get("creeper")
        elif block_type == "skeleton":
            model = "minecraft_starter/assets/models/AnyConv.com__skeleton.obj"
            texture = self.settings.mob_textures.get("skeleton")
        else:
            model = "minecraft_starter/assets/models/block_model"
            texture = self.settings.block_textures.get(block_type)

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
def calculateDijkstraDictionary(settings, tile_map, tile_coordinates, single_locations, cluster_locations):
    obstacle_cluster_types = ["stone", "lava", "water"]  # Cluster obstacle types
    obstacle_single_types = ["wood", "bedrock", "mud", "darkstone", "trimmedGrass"]  # Single obstacle types

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    dijkstraDictionary = {}

    single_locations_dict = {tuple(pos): obstacleType for pos, obstacleType in single_locations}
    cluster_locations_dict = {tuple(pos): obstacleType for pos, obstacleType in cluster_locations}

    world_size = settings.get_world_size()

    for row in tile_coordinates:
        for (x, z) in row:
            list = []
            if tile_map[x][z] != "O":
                for (dx, dz) in directions:
                    new_x, new_z = x + dx, z + dz
                    if 0 <= new_x <= world_size and 0 <= new_z <= world_size:
                        if (new_x, new_z) in single_locations_dict:
                            obstacleType = single_locations_dict[(new_x, new_z)]
                            block_type = obstacle_single_types[obstacleType - 1]
                            if block_type == "wood":
                                list.append(((new_x, new_z), 2))
                            else:
                                list.append(((new_x, new_z), 5))
                        elif (new_x, new_z) in cluster_locations_dict:
                            obstacleType = cluster_locations_dict[(new_x, new_z)]
                            block_type = obstacle_cluster_types[obstacleType - 1]
                            if block_type == "stone":
                                list.append(((new_x, new_z), 3))
                            elif block_type == "water":
                                list.append(((new_x, new_z), 4))
                            elif block_type == "lava":
                                list.append(((new_x, new_z), 6))
                        else:
                            list.append(((new_x, new_z), 1))
                dijkstraDictionary[(x, z)] = list

    return dijkstraDictionary

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
def homeGeneration(settings):
    home_tile_positions = []
    x = random.randint(settings.get_home_min_z(), settings.get_home_max_z())
    z = random.randint(0, settings.get_world_size() - settings.get_home_size() - 10)
    for dx in range(settings.get_home_size()):
        for dz in range(settings.get_home_size()):
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
def generateMap(tile_map, tile_coordinates, block_positions, obstacle_positions, home_tile_positions, settings):
        # Initialize the tile map
    for x in range(settings.get_world_size()):
        row = [] #declare a row to store the tile status (Free Space or Obstacle) (True or False)
        list = []
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
            list.append((x, z))
        tile_coordinates.append(list)
        tile_map.append(row)

def update_blocks_on_path(game, path, block_type):
    world_size = game.game_screen.settings.get_world_size()
    if path is None:
        return

    for x, z in path:
        # Ensure coordinates are within world bounds
        if 0 <= x < world_size and 0 <= z < world_size:
            world_position = (x, -5, z)  # Convert to 3D world coordinates
            if world_position in game.game_screen.block_positions:
                block = game.visible_blocks.get(world_position)
                if block:
                    # Update existing block to the new type
                    block.block_type = block_type
                    block.texture = game.settings.block_textures.get(block_type)
                else:
                    # Add new block for the path
                    game.visible_blocks[world_position] = Block(
                        position=world_position, block_type=block_type
                    )
            # Persist in block_positions to ensure it isn't culled by render logic
            game.game_screen.block_positions[world_position] = False