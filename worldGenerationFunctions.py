from ursina import *
import random
from worldSettings import *
from textures import *

# Block class
class Block(Entity):
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1), block_type="grass", **kwargs):
        if block_type == "zombie":
            model = "minecraft_starter/assets/models/AnyConv.com__zombie.obj"
            texture = mob_textures.get("zombie")
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

# Generate Home Structure
def homeGeneration():
    home_tile_positions = []
    x = random.randint(0, world_size - home_size - 10)
    z = random.randint(home_min_z, home_max_z)
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
        obstacleType = random.randint(1, 2) # Randomly select the obstacle type
        
        # If the position is not already taken by an obstacle, add it to the obstacle set
        if (x, z) not in obstacle_positions and (x, z) not in home_tile_positions:
            obstacle_positions.add((x, z))
            single_locations.append(((x, z), obstacleType))

# Generate the Map
def generateMap(tile_map, block_positions, obstacle_positions):
        # Initialize the tile map
    for x in range(world_size):
        row = [] #declare a row to store the tile status (Free Space or Obstacle) (True or False)
        for z in range(world_size):
            position = (x, -5, z)
            is_free_space = (x, z) not in obstacle_positions
            block_positions[position] = is_free_space
            row.append(is_free_space)
        tile_map.append(row)