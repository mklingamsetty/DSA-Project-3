from ursina import *
# from ursina.prefabs.health_bar import HealthBar
from PIL import Image, ImageDraw
import random
import time

class Game:
    def __init__(self):
        # Dictionary to keep track of visible blocks due to render distance
        self.visible_blocks = {}
        self.visible_mobs = {}

        self.last_save_time = time.time()
        self.save_interval = 2

        self.game_screen = GameScreen()
        self.default_speed = self.game_screen.player_speed
        self.current_block_type = None
        self.draw = ImageDraw.Draw(self.game_screen.image)

        self.rectangle_entity = None
        self.map = Entity()
        self.mPressed = False
        self.health_bar = HealthBar(bar_color=color.green.tint(-.25), roundness=.5, scale=(0.5,.06))
        self.last_damage_time = time.time()
        self.damage_interval = 1
        self.index = 0
        self.pathBFS = None
        self.pathDFS = None
        self.pathDijkstra = None
        self.showBFS = False
        self.showDFS = False
        self.showDijkstra = False

        self.settings = worldSettings()

        # create boundaries
        self.leftWall = Entity(model="cube", scale=(1, self.settings.get_world_size(), self.settings.get_world_size() + 1), position=(-1, 0, (self.settings.get_world_size() / 2) - 0.5), collider="box", visible=False)
        self.rightWall = Entity(model="cube", scale=(1, self.settings.get_world_size(), self.settings.get_world_size() + 1), position=(self.settings.get_world_size() , 0, (self.settings.get_world_size() / 2) - 0.5), collider="box", visible=False)
        self.frontWall = Entity(model="cube", scale=(self.settings.get_world_size() + 1, self.settings.get_world_size(), 1), position=(self.settings.get_world_size() / 2, 0, self.settings.get_world_size()), collider="box", visible=False)
        self.backWall = Entity(model="cube", scale=(self.settings.get_world_size() + 1, self.settings.get_world_size(), 1), position=(self.settings.get_world_size() / 2, 0, -1), collider="box", visible=False)

        Sky(texture="minecraft_starter/assets/textures/nightSky.png")

    def toggle_health_bar(self, visible = True, value = 100):
        if visible == True:
            if not self.health_bar:
                self.health_bar = HealthBar(value=value, bar_color=color.green.tint(-.25), roundness=.5, scale=(0.5,.06))
        else:
            if self.health_bar:
                value = self.health_bar.value
                destroy(self.health_bar)
                self.health_bar = None

    def damage(self, power):
        self.health_bar.value -= power
        if (self.health_bar.value <= 50):
            self.health_bar.bar_color = color.yellow.tint(-.25)
        if (self.health_bar.value <= 25):
            self.health_bar.bar_color = color.red.tint(-.25)
        if (self.health_bar.value <= 0):
            print("Player has Died")
            application.quit()

    def update(self):       
        #Every frame, update the visible blocks
        if self.game_screen.player.y < -10: # If player falls off the world
            self.game_screen.player.y = 10
        self.update_visible_blocks() # constantly update the visible blocks
        
        # Define your world size
        player_x = int(self.game_screen.player.x)
        player_z = int(self.game_screen.player.z)
        player_position = (player_x, -5, player_z)
        mirrored_x = self.settings.get_world_size() - player_x - 1
        new_position = (mirrored_x, player_z)

        #new_position = (int(game_screen.player.x), int(game_screen.player.z))
        if(new_position != self.game_screen.current_position):
            self.draw.point(new_position, fill=(255, 192, 203, 255))
            self.draw.point(self.game_screen.current_position, fill=(0, 255, 0, 255))
        current_time = time.time()
        if player_position in self.visible_blocks:
            block = self.visible_blocks[player_position]
            if block.block_type != self.current_block_type:
                self.current_block_type = block.block_type
                self.game_screen.player.speed = self.default_speed
            if (block.block_type == "bedrock" or block.block_type == "mud" or block.block_type == "darkstone" or block.block_type == "trimmedGrass") and current_time - self.last_damage_time >= self.damage_interval:
                self.damage(5)
                self.last_damage_time = current_time
            if block.block_type == "lava" and current_time - self.last_damage_time >= self.damage_interval:
                self.game_screen.player.speed = self.default_speed / 4
                self.damage(5)
                self.last_damage_time = current_time
            elif block.block_type == "water":
                self.game_screen.player.speed = self.default_speed / 4
        else:
            if self.current_block_type is not None:
                self.current_block_type = None
                self.game_screen.player_speed = self.default_speed
        self.game_screen.current_position = new_position
        if current_time - self.last_save_time >= self.save_interval:
            self.last_save_time = current_time
            #game_screen.image = game_screen.image.transpose(Image.FLIP_LEFT_RIGHT)
            #game_screen.image = game_screen.image.transpose(Image.ROTATE_90)
            # self.game_screen.image.save("minimap.png")

    def update_visible_blocks(self):
        # Update the visible blocks based on the player's position
        obstacle_cluster_types = ["stone", "lava", "water"] # Cluster obstacle types
        obstacle_single_types = ["wood", "bedrock", "mud", "darkstone", "trimmedGrass"] # Single obstacle types

        player_x = int(self.game_screen.player.x) # Player's x position
        player_z = int(self.game_screen.player.z) # Player's z position
        render_distance = self.settings.get_render_distance()
        prevBFSPath = None
        prevDFSPath = None
        for x in range(player_x - render_distance, player_x + render_distance): # Loop through x position +/- render_distance
            for z in range(player_z - render_distance, player_z + render_distance): # Loop through z positions +/- render_distance
                position = (x, -5, z) # Position of the blocks that are visible to us at the moment
                obstacle_position = (x, -4, z) # Position of the obstacles that are visible to us at the moment
                if position in self.game_screen.block_positions and position not in self.visible_blocks:
                    
                    # Use the appropriate texture based on whether it's an obstacle
                    if self.game_screen.block_positions[position]: # If the position is not an obstacle
                        block_type = "grass" # Default block type
                        self.visible_blocks[position] = Block(position=position, block_type=block_type)

                    # if self.pathBFS is None or self.pathDFS is None: 
                    #     block_type = "grass"
                    #     self.visible_blocks[position] = Block(position=position, block_type=block_type)   
                    if self.showBFS and (x, z) in self.pathBFS:
                        block_type = "redstone" # Redstone block type
                        self.visible_blocks[position] = Block(position=position, block_type=block_type)
                        
                        #self.visible_blocks[obstacle_position] = Zombie(position=obstacle_position, scale = 0.1)
                        #zombie = Entity(model=mob_models.get("zombie"), texture = mob_textures.get("zombie"), scale=0.07, double_sided=True, y = -4, x = x, z = z)
                    if self.showDFS and (x, z) in self.pathDFS:
                        block_type = "bluestone" # Bluestone block type   
                        self.visible_blocks[position] = Block(position=position, block_type=block_type)

                    if self.showDijkstra and (x, z) in self.pathDijkstra:
                        block_type = "snow"
                        self.visible_blocks[position] = Block(position=position, block_type=block_type)

                    if self.showBFS is False and self.pathBFS is not None:
                        if self.pathDijkstra is not None:
                            if (x, z) in self.pathBFS:
                                block_type = "snow"
                        if self.pathDFS is not None:
                            if (x, z) in self.pathDFS:
                                block_type = "bluestone"
                        if (x, z) in self.pathBFS:
                            block_type = "redstone"
                            self.visible_blocks[position] = Block(position=position, block_type=block_type)
                    if self.showDFS is False and self.pathDFS is not None:
                        if self.pathBFS is not None:
                            if (x, z) in self.pathBFS:
                                block_type = "redstone"
                        if self.pathDijkstra is not None:
                            if (x, z) in self.pathDijkstra:
                                block_type = "snow"
                        if (x, z) in self.pathDFS:
                            block_type = "bluestone"
                            self.visible_blocks[position] = Block(position=position, block_type=block_type)
                    if self.showDijkstra is False and self.pathDijkstra is not None:
                        if self.pathBFS is not None:
                            if (x, z) in self.pathBFS:
                                block_type = "redstone"
                        if self.pathDFS is not None:
                            if (x, z) in self.pathDFS:
                                block_type = "bluestone"
                        if (x, z) in self.pathDijkstra:
                            block_type = "snow"
                            self.visible_blocks[position] = Block(position=position, block_type=block_type)
                
                    # Check if the position is a home tile position
                    if (x, z) in self.game_screen.home_tile_positions:
                        block_type = "wall"
                        self.visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                        middle_obstacle_position = (x, -3, z) # Middle obstacle position
                        self.visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                        top_obstacle_position = (x, -2, z) # Top obstacle position
                        self.visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                        self.visible_blocks[position] = Block(position=position, block_type=block_type)
                        
                    # Check if the position is an obstacle position
                    if (x, z) in self.game_screen.obstacle_positions and obstacle_position not in self.visible_blocks:
                        # Now I need to check if (x, z) is in cluster_locations
                        for cluster_positions, obstacleType in self.game_screen.cluster_locations:
                            if (x, z) in cluster_positions: 
                                block_type = obstacle_cluster_types[obstacleType - 1]
                                if block_type == "stone": # If the block type is stone then we need to make it tall
                                    self.visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    middle_obstacle_position = (x, -3, z)
                                    self.visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    top_obstacle_position = (x, -2, z)
                                    self.visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                
                                # If the block type is lava and/or water we can just change the texture
                                self.visible_blocks[position] = Block(position=position, block_type=block_type)
                                break

                        for single_position, obstacleType in self.game_screen.single_locations:
                            if (x, z) == single_position:
                                block_type = obstacle_single_types[obstacleType - 1]
                                if block_type == "wood":
                                    self.visible_blocks[obstacle_position] = Block(position=obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    bottom_obstacle_position = (x, -3, z)
                                    self.visible_blocks[bottom_obstacle_position] = Block(position=bottom_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    middle_obstacle_position = (x, -2, z)
                                    self.visible_blocks[middle_obstacle_position] = Block(position=middle_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    top_obstacle_position = (x, -1, z)
                                    self.visible_blocks[top_obstacle_position] = Block(position=top_obstacle_position, scale=(1, 1, 1), block_type=block_type)
                                    # Generate Tree's Leaves now
                                    for dx in range(-2, 3):
                                        for dz in range(-2, 3):
                                            if (dx, dz) != (0, 0):
                                                leaf_position = (x + dx, -1, z + dz)
                                                if leaf_position not in self.visible_blocks: self.visible_blocks[leaf_position] = Block(position=leaf_position, block_type="leaves", double_sided=True)

                                elif block_type == "bedrock":
                                    #self.visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type=block_type, double_sided=True, scale=0.08)
                                    # Now we need to spawn a zombie on the bedrock
                                    mob_position = (x, -4, z)
                                    # print("Spawning Zombie at: ", mob_position)
                                    if mob_position not in self.visible_mobs:
                                        self.visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="zombie", double_sided=True)
                                        #self.visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                                elif block_type == "mud":
                                    #self.visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="mud", double_sided=True, scale=0.08)
                                    # Now we need to spawn a zombie on the bedrock
                                    mob_position = (x, -3, z)
                                    # print("Spawning Zombie at: ", mob_position)
                                    if mob_position not in self.visible_mobs:
                                        self.visible_mobs[mob_position] = Block(position=mob_position, scale=0.10, block_type="enderman", double_sided=True)
                                        #self.visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                                elif block_type == "darkstone":
                                    #self.visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="darkstone", double_sided=True, scale=0.08)
                                    # Now we need to spawn a zombie on the bedrock
                                    mob_position = (x, -4, z)
                                    # print("Spawning Zombie at: ", mob_position)
                                    if mob_position not in self.visible_mobs:
                                        self.visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="creeper", double_sided=True)
                                        #self.visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                                elif block_type == "trimmedGrass":
                                    #self.visible_blocks[obstacle_position] = Block(position=obstacle_position, block_type="trimmedGrass", double_sided=True, scale=0.08)
                                    # Now we need to spawn a zombie on the bedrock
                                    mob_position = (x, -4, z)
                                    # print("Spawning Zombie at: ", mob_position)
                                    if mob_position not in self.visible_mobs:
                                        self.visible_mobs[mob_position] = Block(position=mob_position, scale=0.07, block_type="skeleton", double_sided=True)
                                        #self.visible_blocks[mob_position] = Block(position=mob_position, block_type="zombie", double_sided=True, scale=0.08)
                                if position not in self.visible_blocks:        
                                    self.visible_blocks[position] = Block(position=position, block_type=block_type)
                                break
        
        
        # Remove blocks that are out of range
        for position in list(self.visible_blocks):
            if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
                destroy(self.visible_blocks[position])
                del self.visible_blocks[position]

        # Remove mobs that are out of range
        for position in list(self.visible_mobs):
            self.visible_mobs[position].look_at(self.game_screen.player, 'forward')
            self.visible_mobs[position].rotation_x = 0
            self.visible_mobs[position].rotation_z = 0
            if abs(position[0] - player_x) > render_distance or abs(position[2] - player_z) > render_distance:
                destroy(self.visible_mobs[position])
                del self.visible_mobs[position]

    def get_rectangle_entity(self):
        return self.rectangle_entity
    
    def get_map(self):
        return self.map
    
    def get_mPressed(self):
        return self.mPressed

    def set_rectangle_entity(self, rectangle_entity):
        self.rectangle_entity = rectangle_entity
    
    def set_map(self, map):
        self.map = map

    def set_mPressed(self, mPressed):
        self.mPressed = mPressed
    

# Initialize the app
app = Ursina()
window.exit_button.visible = True # Show the Red X window close button

# Loading textures and worldGen must occur after app in initialized
from worldGenerationFunctions import *
from worldSettings import *

game = Game()

def input(key):
    rectangle_entity = game.get_rectangle_entity()
    map = game.get_map()
    mPressed = game.get_mPressed()
    global text_entity     

    if key == 'q':
        application.quit()
    elif key == 'm':
        mPressed = True
        game.toggle_health_bar(visible=False)
        #destroy(game.health_bar)
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
                scale=(0.9, 0.9),
                texture = "minimap.png"
            )

            text_entity = Text(
                text="Please Choose an Algorithm: \n Press 'B' for BFS \n Press 'D' for DFS \n Press 'J' for Dijkstra's",
                position=(0.09, 0),
                parent=camera.ui,
                scale=2,
                color=color.white
            )
    elif key == 'b' and mPressed:
        print("BFS Algorithm")
        map.texture = "minimap.png"  # Reset the minimap texture
        game.pathBFS = game.game_screen.BFS()  # Compute the path
        update_blocks_on_path(game, game.pathBFS, "redstone")  # Place redstone blocks
        game.showBFS = True
        game.showDFS = False
        game.showDijkstra = False
        #game.pathDFS = None  # Reset the path
        #update_blocks_on_path(game, game.pathDFS, "grass")  # Remove bluestone blocks
        map.texture = "minimapAlgorithmPathBFS.png"  # Update the minimap texture

    elif key == 'd' and mPressed:
        print("DFS Algorithm")
        map.texture = "minimap.png"  # Reset the minimap texture
        game.pathDFS = game.game_screen.DFS()  # Compute the path
        update_blocks_on_path(game, game.pathDFS, "bluestone")  # Place bluestone blocks
        game.showBFS = False
        game.showDFS = True
        game.showDijkstra = False
        #game.pathBFS = None  # Reset the path
        #update_blocks_on_path(game, game.pathBFS, "grass") # Remove redstone blocks
        map.texture = "minimapAlgorithmPathDFS.png"  # Update the minimap texture
    elif key == 'j' and mPressed:
        print("Dijkstra's Algorithm")
        map.texture = "minimap.png"  # Reset the minimap texture
        game.pathDijkstra = None  # Reset the path
        game.pathDijkstra = game.game_screen.dijkstra()  # Compute the path
        game.showBFS = False
        game.showDFS = False
        game.showDijkstra = True
        update_blocks_on_path(game, game.pathDijkstra, "snow")  # Place gold blocks
        map.texture = "minimapAlgorithmPathDijkstra.png"  # Update the minimap texture
    elif key == 'r':
        map.texture = "minimap.png"  # Reset the minimap texture
        game.toggle_health_bar(visible=True)
        if rectangle_entity:
            destroy(rectangle_entity)
            destroy(map)
            destroy(text_entity)
            rectangle_entity = None
            mPressed = False
        # if (path == game.game_screen.BFS()):
        #     update_blocks_on_path(game, path, "redstone")
        # if (path == game.game_screen.DFS()):
        #     update_blocks_on_path(game, path, "bluestone")
    game.set_rectangle_entity(rectangle_entity)
    game.set_map(map)
    game.set_mPressed(mPressed)

def update():
    game.update()

# Run the app in main function
def main():
    update() # Call update function
    app.run() # Run the app


if __name__ == "__main__":
    main()
