from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Initialize the app
app = Ursina()
window.exit_button.visible = True # Show the Red X window close button

# Loading textures and worldGen must occur after app in initialized
from textures import *
from worldGenerationFunctions import *
from worldSettings import *

# Store all block positions in a set (all unique blocks with uniqe positions)
block_positions = {}

# Will contain 2D map of obstacle positions and free spaces
tile_map = []

# Generate the Home
home_tile_positions = homeGeneration()
            
# Set and Dictionaries to store unique obstacle positions
obstacle_positions = set()
cluster_locations = []
single_locations = []

# Generate Cluster Obstacles
clusterGeneration(home_tile_positions, obstacle_positions, cluster_locations)

# Generate Single Obstacles
singlesGeneration(obstacle_positions, home_tile_positions, single_locations)

# Initialize the tile map
generateMap(tile_map, block_positions, obstacle_positions)

# Dictionary to keep track of visible blocks due to render distance
visible_blocks = {}
visible_mobs = {}

# Ensure the player doesn't spawn on an obstacle
while (player_spawn_x, player_spawn_z) in obstacle_positions:
    player_spawn_x += 1  # Adjust as necessary

# initialize the player controller
player=FirstPersonController(
  mouse_sensitivity=Vec2(100, 100), # Mouse sensitivity
  position=(player_spawn_x, 5, home_min_z), # Player spawn position
  speed=player_speed # Player movement speed
)

# Create the night sky background
Sky(texture="minecraft_starter/assets/textures/nightSky.png")


def update_visible_blocks():
    obstacle_cluster_types = ["stone", "lava", "water"]
    obstacle_single_types = ["wood", "bedrock"]
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
                
                if (x, z) in home_tile_positions:
                    block_type = "wall"
                    visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    middle_obstacle_position = (x, -3, z)
                    visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    top_obstacle_position = (x, -2, z)
                    visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    visible_blocks[position] = Block(position=position, block_type=block_type)
                    
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
                                            if leaf_position not in visible_blocks: visible_blocks[leaf_position] = Block(position=leaf_position, block_type="leaves", double_sided=True)

                            elif block_type == "bedrock":
                                visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="zombie", double_sided=True, scale=0.08)
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -4, z)
                                # print("Spawning Zombie at: ", mob_position)
                                if mob_position not in visible_mobs and mob_position not in visible_blocks:
                                    visible_blocks[position] = Block(position=mob_position, scale=0.07, block_type="zombie", double_sided=True)
                                    #visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                            if position not in visible_blocks:        
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
    if player.y < -10: # If player falls off the world
        player.y = 10
    update_visible_blocks()

# Run the app in main function
def main():
    update() # Call update function
    app.run() # Run the app

if __name__ == "__main__":
    main()