from ursina import *
import random
from worldSettings import *
from textures import *
from algorithms import *
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image, ImageDraw


class GameScreen:
    def __init__(self):
        self.player_spawn_x = player_spawn_x
        self.player_spawn_z = player_spawn_z
        self.player_speed = player_speed
       
        # Store all block positions in a set (unique blocks with unique positions)
        self.block_positions = {}
        
        # 2D map of obstacle positions and free spaces
        self.tile_map = []
        
        # Generate the Home
        self.home_tile_positions = homeGeneration()
        
        # Sets and lists to store unique obstacle positions
        self.obstacle_positions = set()
        self.cluster_locations = []
        self.single_locations = []
        
        # Generate Cluster Obstacles
        clusterGeneration(self.home_tile_positions, self.obstacle_positions, self.cluster_locations)
        
        # Generate Single Obstacles
        singlesGeneration(self.obstacle_positions, self.home_tile_positions, self.single_locations)
          
        # Generate the map
        generateMap(self.tile_map, self.block_positions, self.obstacle_positions, self.home_tile_positions)

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
        self.image = Image.new('RGB', (world_size, world_size), color=(0, 0, 0, 0))
        self.colorMap = []
        draw_minimap(self.image, self.tile_map, self.colorMap)
        self.MiniMap.texture = "minimap.png"
        

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


mini_block = Entity(
  parent=camera,
  model="minecraft_starter/assets/models/Torch",
  texture=block_textures.get("torch"),
  scale= 0.2,
  position=(0.35, -0.25, 0.5),
  rotation=(-15, -30, -5)
)

# Draw the texture for the MiniMap
def draw_minimap(image, tile_map, colorMap):
    
    colorChar = ''
    draw = ImageDraw.Draw(image)
    for x in range(world_size):
        row = []
        for z in range(world_size):
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
            draw.point((world_size - x - 1, z), fill=color)
            row.append(colorChar)
        colorMap.append(row)
    #image = image.transpose(Image.ROTATE_90)
    
    image.save("minimap.png")
    print("MiniMap Created")

# Generate Home Structure
def homeGeneration():
    home_tile_positions = []
    z = random.randint(home_min_z, world_size)
    x = random.randint(home_min_z, home_max_z)
    for dx in range(home_size):
        for dz in range(home_size):
            home_tile_positions.append((x + dx, z + dz))
    return home_tile_positions

# Generate Cluster Obstacles
def clusterGeneration(home_tile_positions, obstacle_positions, cluster_locations):
    # Place 3x3 clusters of obstacles
    for i in range(num_clusters):
        placed = False
        while not placed:
            # Declaring the cluster position to be inside of the world and not outside of it
            x = random.randint(0, world_size - 3) # x pos
            z = random.randint(0, world_size - 3) # z pos
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
def singlesGeneration(obstacle_positions, home_tile_positions, single_locations):
    # Place single tile obstacles
    while len(obstacle_positions) < total_obstacles: # Remaining obstacles will be single tiled
        # Declare world bounds for the obstacles
        x = random.randint(0, world_size - 1)
        z = random.randint(0, world_size - 1)
        obstacleType = random.randint(1, 5) # Randomly select the obstacle type
        
        # If the position is not already taken by an obstacle, add it to the obstacle set
        if (x, z) not in obstacle_positions and (x, z) not in home_tile_positions:
            obstacle_positions.add((x, z))
            single_locations.append(((x, z), obstacleType))

# Generate the Map
def generateMap(tile_map, block_positions, obstacle_positions, home_tile_positions):
        # Initialize the tile map
    for x in range(world_size):
        row = [] #declare a row to store the tile status (Free Space or Obstacle) (True or False)
        for z in range(world_size):
            position = (x, -5, z)
            is_free_space = (x, z) not in obstacle_positions
            block_positions[position] = is_free_space
            if x == player_spawn_x and z == player_spawn_z:
                row.append("P") # P for Player
            elif is_free_space:
                row.append("F") # F for Free Space
            elif (x, z) in home_tile_positions:
                row.append("H") # H for Home
            else:
                row.append("O") # O for Obstacle
        tile_map.append(row)