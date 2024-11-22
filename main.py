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
    "wood" : load_texture("minecraft_starter/assets/textures/Wood.png"),
    "leaves" : load_texture("minecraft_starter/assets/textures/leaf.png")
    # Add other block textures if needed
}

mob_textures = {
    "zombie" : load_texture("minecraft_starter/assets/textures/zombie.png")
}

mob_models = {
    "zombie" : load_model("minecraft_starter/assets/models/AnyConv.com__zombie.obj")
}

# Block class
class Block(Entity):
    def __init__(self, position=(0,0,0), scale=(1, 1, 1), block_type="grass"):
        super().__init__(
            position=position,
            model="minecraft_starter/assets/models/block_model",
            scale = scale,
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
world_size = 500                                            # This creates a world with 100,489 blocks
render_distance = 7                                         # reduce this value if you have a slow computer
total_tiles = world_size * world_size                       # Compute total number of tiles
total_obstacles = int(0.1 * total_tiles)                    # Compute total number of obstacles (10% of total tiles)
num_clusters = total_obstacles // 10                        # Number of Obstacle clusters (occupies 9 tiles)
num_single_obstacles = total_obstacles - (num_clusters * 9) # Number of Obstacle singles (occupies 1 tiles)
player_spawn_x = world_size // 2                            # Player spawn x position
player_spawn_z = world_size - 10                            # Player spawn z position
player_speed = 10                                           # Player movement speed
home_min_x = 217                                            # Home min x position
home_max_x = 317                                            # Home max x position
home_min_z = 217                                            # Home min z position
home_max_z = 317                                            # Home max z position
###############################################################################################################################
###############################################################################################################################

# create boundaries
leftWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(-1, 0, (world_size / 2) - 0.5), collider="box", visible=False)
rightWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(world_size , 0, (world_size / 2) - 0.5), collider="box", visible=False)
frontWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, world_size), collider="box", visible=False)
backWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, -1), collider="box", visible=False)

# Store all block positions in a set (all unique blocks with uniqe positions)
block_positions = {}

# Will contain 2D map of obstacle positions and free spaces
tile_map = []

# Set to store unique obstacle positions
obstacle_positions = set()
cluster_locations = []
single_locations = []

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
        if all((cx, cz) not in obstacle_positions for (cx, cz) in cluster_positions):
            # if all the coordinates in cluster_positions are not in obstacle_positions
            # meaning now the obstacle cluster CAN be placed
            
            # Then I should Add the cluster positions to the obstacle set
            obstacle_positions.update(cluster_positions)
            cluster_locations.append((cluster_positions, obstacleType))
            placed = True

# Place single tile obstacles
while len(obstacle_positions) < total_obstacles: # Remaining obstacles will be single tiled
    # Declare world bounds for the obstacles
    x = random.randint(0, world_size - 1)
    z = random.randint(0, world_size - 1)
    obstacleType = random.randint(1, 2) # Randomly select the obstacle type
    
    # If the position is not already taken by an obstacle, add it to the obstacle set
    if (x, z) not in obstacle_positions:
        obstacle_positions.add((x, z))
        single_locations.append(((x, z), obstacleType))

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
visible_mobs = {}

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

obstacle_cluster_types = ["stone", "lava", "water"]
obstacle_single_types = ["wood", "bedrock"]
def update_visible_blocks():
    player_x = int(player.x)
    player_z = int(player.z)
    for x in range(player_x - render_distance, player_x + render_distance):
        for z in range(player_z - render_distance, player_z + render_distance):
            position = (x, -5, z)
            obstacle_position = (x, -4, z)
            if position in block_positions and position not in visible_blocks:
                # Use the appropriate texture based on whether it's an obstacle
                if block_positions[position]: 
                    block_type = "grass"
                    visible_blocks[position] = Block(position=position, block_type=block_type)
                    #visible_blocks[obstacle_position] = Zombie(position=obstacle_position, scale = 0.1)
                    #zombie = Entity(model=mob_models.get("zombie"), texture = mob_textures.get("zombie"), scale=0.07, double_sided=True, y = -4, x = x, z = z)
                    
                if (x, z) in obstacle_positions and obstacle_position not in visible_blocks:
                    # Now I need to check if (x, z) is in cluster_locations
                    for cluster_positions, obstacleType in cluster_locations:
                        if (x, z) in cluster_positions:
                            block_type = obstacle_cluster_types[obstacleType - 1]
                            if block_type == "stone":
                                visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                middle_obstacle_position = (x, -3, z)
                                visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                top_obstacle_position = (x, -2, z)
                                visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                            visible_blocks[position] = Block(position=position, block_type=block_type)
                            break

                    for single_position, obstacleType in single_locations:
                        if (x, z) == single_position:
                            block_type = obstacle_single_types[obstacleType - 1]
                            if block_type == "wood":
                                visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                bottom_obstacle_position = (x, -3, z)
                                visible_blocks[bottom_obstacle_position] = Block(position=bottom_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                middle_obstacle_position = (x, -2, z)
                                visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                top_obstacle_position = (x, -1, z)
                                visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                # Generate Tree's Leaves now
                                for dx in range(-2, 3):
                                    for dz in range(-2, 3):
                                        if (dx, dz) != (0, 0):
                                            leaf_position = (x + dx, -1, z + dz)
                                            if leaf_position not in visible_blocks: visible_blocks[leaf_position] = Block(position=leaf_position, block_type="leaves")

                            elif block_type == "bedrock":
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -4, z)
                                print("Spawning Zombie at: ", mob_position)
                                zombie = Block(position=mob_position, scale=0.08, block_type="grass")
                                zombie.model = mob_models.get("zombie")
                                zombie.texture = mob_textures.get("zombie")
                                zombie.double_sided = True
                                visible_blocks[mob_position] = zombie
                                    
                            visible_blocks[position] = Block(position=position, block_type=block_type)
                            break

    
    # Remove blocks that are out of range
    for position in list(visible_blocks):
        if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
            destroy(visible_blocks[position])
            del visible_blocks[position]

    # Remove mobs that are out of range
    for position in list(visible_mobs):
        if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
            destroy(visible_mobs[position])
            del visible_mobs[position]

# This is an Ursina function that is called every frame
def update():
    #Every frame, update the visible blocks
    if player.y < -10:
        player.y = 10
    update_visible_blocks()

# Run the app in main function
def main():
    update() # Call update function
    app.run() # Run the app

if __name__ == "__main__":
    main()