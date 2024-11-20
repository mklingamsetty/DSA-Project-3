from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Initialize the app
app = Ursina()
window.exit_button.visible = True # Show the Red X window close button

# Load block textures
block_textures = {
    "grass": load_texture("minecraft_starter/assets/textures/groundEarth.png"),
    "dirt": load_texture("minecraft_starter/assets/textures/groundMud.png"),
    "stone": load_texture("minecraft_starter/assets/textures/Stone01.png"),
    "bedrock": load_texture("minecraft_starter/assets/textures/stone07.png"),
    "lava": load_texture("minecraft_starter/assets/textures/lava01.png"),
    "water": load_texture("minecraft_starter/assets/textures/water.png"),
    "torch" : load_texture("minecraft_starter/assets/textures/Diffuse.png"),
    "obstacleTile" : load_texture("minecraft_starter/assets/textures/wallBrick05.png"),
    "wood" : load_texture("minecraft_starter/assets/textures/Wood.png")
    # Add other block textures if needed
}

# Block class
class Block(Entity):
    def __init__(self, position=(0,0,0), block_type="grass"):
        super().__init__(
            position=position,
            model="minecraft_starter/assets/models/block_model",
            scale = 1,
            origin_y = 0.5,
            texture=block_textures.get(block_type),
            collider='box'
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
########################################################### GLOBAL VARIABLES ##################################################
###############################################################################################################################
# World settings
world_size = 1000                                           # This creates a world_size x world_size grid (Minimum number needs to be 317 for at least 100,000 Datapoints)
render_distance = 8                                         # reduce this value if you have a slow computer
total_tiles = world_size * world_size                       # Compute total number of tiles
total_obstacles = int(0.1 * total_tiles)                    # Compute total number of obstacles (10% of total tiles)
num_clusters = total_obstacles // 10                        # Number of Obstacle "clusters" (occupies 9 tiles)
num_single_obstacles = total_obstacles - (num_clusters * 9) # Number of Obstacle "singles" (occupies 1 tiles)
player_spawn_x = world_size // 2                            # Player spawn x position
player_spawn_z = world_size - 10                            # Player spawn z position
player_speed = 15                                           # Player movement speed
home_min_x = world_size - 100                               # Home min x position
home_max_x = world_size - 10                                # Home max x position
home_min_z = world_size - 10                                # Home min z position
home_max_z = world_size - 100                               # Home max z position
###############################################################################################################################
###############################################################################################################################

# create boundaries
leftWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(-1, 0, (world_size / 2) - 0.5), collider="box", visible=False)
rightWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(world_size , 0, (world_size / 2) - 0.5), collider="box", visible=False)
frontWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, world_size), collider="box", visible=False)
backWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, -1), collider="box", visible=False)

# Store all block positions in a dictionary (all unique blocks with uniqe positions)
block_positions = {}

# Will contain 2D map of obstacle positions and free spaces
tile_map = []

# Set to store unique obstacle positions
obstacle_positions = set()

# Set to store obstacle clusters
obstacle_cluster_positions = set()

# Set to store obstacle singles
obstacle_single_positions = set()

# Place 3x3 clusters of obstacles
for i in range(num_clusters):
    placed = False
    while not placed:
        # Declaring the cluster position to be inside of the world and not outside of it
        x = random.randint(0, world_size - 3) # x pos
        z = random.randint(0, world_size - 3) # z pos
        
        # create a vector<pair<int, int>> equivalent to mark the cluster obstacle positions
        cluster_positions = [(x + dx, z + dz) for dx in range(3) for dz in range(3)]
        # Creates a 3x3 cluster starting at the randomly generated x and z positions
        # Now using a nested for loop, we marks the clustered position 3 in the x from the start and 3 in the z from the start
        
        # cluster_positions in C++: vector<pair<int, int>> cluster_positions = {{x, z}, {x + 1, z}, {x + 2, z}, 
        #                                                                       {x, z + 1}, {x + 1, z + 1}, {x + 2, z + 1}, 
        #                                                                       {x, z + 2}, {x + 1, z + 2}, {x + 2, z + 2}};
        
        # Now we need to check if any of the coordinates in cluster_positions are already occupied by an obstacle
        if all((cx, cz) not in obstacle_positions for (cx, cz) in cluster_positions):
            # if all the coordinates in cluster_positions are not in obstacle_positions
            # meaning now the obstacle cluster CAN be placed
            
            # Then I should Add the cluster positions to the obstacle set
            obstacle_positions.update(cluster_positions)

            # Add the cluster positions to the obstacle cluster set
            obstacle_cluster_positions.update(cluster_positions)
            placed = True

# Place single tile obstacles
while len(obstacle_positions) < total_obstacles: # Remaining obstacles will be single tiled
    # Declare world bounds for the obstacles
    x = random.randint(0, world_size - 1)
    z = random.randint(0, world_size - 1)
    
    # If the position is not already taken by an obstacle, add it to the obstacle set
    if (x, z) not in obstacle_positions:
        obstacle_positions.add((x, z))
        obstacle_single_positions.add((x, z))

# Initialize the tile map
for x in range(world_size):
    row = [] #declare a row to store the tile status (Free Space or Obstacle) (True or False)
    for z in range(world_size):
        position = (x, -5, z)
        is_free_space = (x, z) not in obstacle_positions
        block_positions[position] = is_free_space
        row.append(is_free_space)
    tile_map.append(row)

# Dictionary to keep track of visible blocks due to render distance
visible_blocks = {}

# Ensure the player doesn't spawn on an obstacle
while (player_spawn_x, player_spawn_z) in obstacle_positions:
    player_spawn_x += 1  # Adjust as necessary

# initialize the player controller
player=FirstPersonController(
  mouse_sensitivity=Vec2(100, 100), # Mouse sensitivity
  position=(player_spawn_x, 5, player_spawn_z), # Player spawn position
  speed=player_speed # Player movement speed
)

# Create the night sky background
Sky(texture="minecraft_starter/assets/textures/nightSky.png")

def update_visible_blocks():
    player_x = int(player.x)
    player_z = int(player.z)
    for x in range(player_x - render_distance, player_x + render_distance):
        for z in range(player_z - render_distance, player_z + render_distance):
            position = (x, -5, z)
            if position in block_positions and position not in visible_blocks:
                # Use the appropriate texture based on whether it's an obstacle
                block_type = "grass" if block_positions[position] else "obstacleTile"
                visible_blocks[position] = Block(position=position, block_type=block_type)
    # Remove blocks that are out of range
    for position in list(visible_blocks):
        if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
            destroy(visible_blocks[position])
            del visible_blocks[position]

# This is an Ursina function that is called every frame
def update():
    #Every frame, update the visible blocks
    update_visible_blocks()

# Run the app in main function
def main():
    update() # Call update function
    app.run() # Run the app

if __name__ == "__main__":
    main()