from ursina import *
from PIL import Image, ImageDraw
import random
import time

# Initialize the app
app = Ursina()
window.exit_button.visible = True # Show the Red X window close button

# Loading textures and worldGen must occur after app in initialized
from textures import *
from worldGenerationFunctions import *
from worldSettings import *

# Dictionary to keep track of visible blocks due to render distance
visible_blocks = {}
visible_mobs = {}

last_save_time = time.time()
save_interval = 2

game_screen = GameScreen()
draw = ImageDraw.Draw(game_screen.image)

rectangle_entity = None
doBFS = False
doDFS = False
map = Entity()
mPressed = False
index = 0
path = None

def input(key):
    global rectangle_entity
    global map
    global text_entity  # Add a variable to store the text entity
    global mPressed
    global doBFS, doDFS
    #global DFSTest
    #global BFSTest
    # Check if the player presses the 'q' key
    if key == 'q':
        # Quit the game
        application.quit()
    elif key == 'm':
        mPressed = True
        print("I pressed m")
        if not rectangle_entity:
            rectangle_entity = Button(
                model='quad',
                scale=(10, 10),
                color=color.black,
                position=(4, 4),
                parent=camera.ui,
            )
            map = Entity(
            parent=camera.ui,
            model='quad',
            position=(-0.4, 0),
            scale=(0.9, 0.9)
            )
            map.texture = "minimap.png"
            # Add text next to the rectangle
            text_entity = Text(
                text="Please Choose an Algorithm: \n Press 'B' for BFS \n Press 'D' for DFS",
                position=(0.1, 0),
                parent=camera.ui,
                scale=2,
                color=color.white
            )
            print("Rectangle Entity Created")
    elif key == 'b' and mPressed:
        print("BFS Algorithm")
        doBFS = True
        path = game_screen.BFS()
    elif key == 'd' and mPressed:
        print("DFS Algorithm")
        doDFS = True
        path = game_screen.DFS()
    elif key == 'r':
        if rectangle_entity:
            destroy(rectangle_entity)
            destroy(map)
            destroy(text_entity)
            rectangle_entity = None
            mPressed = False
    
    
def update_visible_blocks():
    # Update the visible blocks based on the player's position

    obstacle_cluster_types = ["stone", "lava", "water"] # Cluster obstacle types
    obstacle_single_types = ["wood", "bedrock", "mud", "darkstone", "trimmedGrass"] # Single obstacle types

    player_x = int(game_screen.player.x) # Player's x position
    player_z = int(game_screen.player.z) # Player's z position

    for x in range(player_x - render_distance, player_x + render_distance): # Loop through x position +/- render_distance
        for z in range(player_z - render_distance, player_z + render_distance): # Loop through z positions +/- render_distance
            position = (x, -5, z) # Position of the blocks that are visible to us at the moment
            obstacle_position = (x, -4, z) # Position of the obstacles that are visible to us at the moment
            if position in game_screen.block_positions and position not in visible_blocks:
                # Use the appropriate texture based on whether it's an obstacle
                if game_screen.block_positions[position]: 
                    block_type = "grass" # Default block type
                    visible_blocks[position] = Block(position=position, block_type=block_type)
                    #visible_blocks[obstacle_position] = Zombie(position=obstacle_position, scale = 0.1)
                    #zombie = Entity(model=mob_models.get("zombie"), texture = mob_textures.get("zombie"), scale=0.07, double_sided=True, y = -4, x = x, z = z)
                
                # Check if the position is a home tile position
                if (x, z) in game_screen.home_tile_positions:
                    block_type = "wall"
                    visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    middle_obstacle_position = (x, -3, z) # Middle obstacle position
                    visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    top_obstacle_position = (x, -2, z) # Top obstacle position
                    visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                    visible_blocks[position] = Block(position=position, block_type=block_type)
                    
                # Check if the position is an obstacle position
                if (x, z) in game_screen.obstacle_positions and obstacle_position not in visible_blocks:
                    # Now I need to check if (x, z) is in cluster_locations
                    for cluster_positions, obstacleType in game_screen.cluster_locations:
                        if (x, z) in cluster_positions: 
                            block_type = obstacle_cluster_types[obstacleType - 1]
                            if block_type == "stone": # If the block type is stone then we need to make it tall
                                visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                middle_obstacle_position = (x, -3, z)
                                visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                top_obstacle_position = (x, -2, z)
                                visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                            
                            # If the block type is lava and/or water we can just change the texture
                            visible_blocks[position] = Block(position=position, block_type=block_type)
                            break

                    for single_position, obstacleType in game_screen.single_locations:
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
                                #visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type=block_type, double_sided=True, scale=0.08)
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -4, z)
                                # print("Spawning Zombie at: ", mob_position)
                                if mob_position not in visible_mobs:
                                    visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="zombie", double_sided=True)
                                    #visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                            elif block_type == "mud":
                                #visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="mud", double_sided=True, scale=0.08)
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -3, z)
                                # print("Spawning Zombie at: ", mob_position)
                                if mob_position not in visible_mobs:
                                    visible_mobs[mob_position] = Block(position=mob_position, scale=0.10, block_type="enderman", double_sided=True)
                                    #visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                            elif block_type == "darkstone":
                                #visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="darkstone", double_sided=True, scale=0.08)
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -4, z)
                                # print("Spawning Zombie at: ", mob_position)
                                if mob_position not in visible_mobs:
                                    visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="creeper", double_sided=True)
                                    #visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                            elif block_type == "trimmedGrass":
                                #visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="trimmedGrass", double_sided=True, scale=0.08)
                                # Now we need to spawn a zombie on the bedrock
                                mob_position = (x, -4, z)
                                # print("Spawning Zombie at: ", mob_position)
                                if mob_position not in visible_mobs:
                                    visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="skeleton", double_sided=True)
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
        visible_mobs[position].look_at(game_screen.player, 'forward')
        visible_mobs[position].rotation_x = 0
        visible_mobs[position].rotation_z = 0
        if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
            destroy(visible_mobs[position])
            del visible_mobs[position]

# This is an Ursina function that is called every frame
def update(algorithmDraw=False, coordinates=None):
    global last_save_time, save_interval, doBFS, doDFS, map, index, path
    
    #Every frame, update the visible blocks
    if game_screen.player.y < -10: # If player falls off the world
        game_screen.player.y = 10
    update_visible_blocks() # constantly update the visible blocks
    
    # Define your world size
    player_x = int(game_screen.player.x)
    player_z = int(game_screen.player.z)
    mirrored_x = world_size - player_x - 1
    new_position = (mirrored_x, player_z)

    #new_position = (int(game_screen.player.x), int(game_screen.player.z))
    if(new_position != game_screen.current_position):
        draw.point(new_position, fill=(255, 192, 203, 255))
        draw.point(game_screen.current_position, fill=(0, 255, 0, 255))
    current_time = time.time()
    game_screen.current_position = new_position
    if current_time - last_save_time >= save_interval:
        last_save_time = current_time
        #game_screen.image = game_screen.image.transpose(Image.FLIP_LEFT_RIGHT)
        #game_screen.image = game_screen.image.transpose(Image.ROTATE_90)
        game_screen.image.save("minimap.png")


# Run the app in main function
def main():
    
    update() # Call update function
    app.run() # Run the app


if __name__ == "__main__":
    main()