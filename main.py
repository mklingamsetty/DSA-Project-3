from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

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
    "torch" : load_texture("minecraft_starter/assets/textures/Diffuse.png")
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
# World settings
world_size = 20    # This creates a world with 100,489 blocks
render_distance = 8 # reduce this value if you have a slow computer
                    # Render Distance of 8 will render 8x8 blocks around the player
                    # In order to prevent FPS drop and lag, keep the render distance low

# create boundaries
leftWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(-1, 0, (world_size / 2) - 0.5), collider="box", visible=False)
rightWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(world_size , 0, (world_size / 2) - 0.5), collider="box", visible=False)
frontWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, world_size), collider="box", visible=False)
backWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, -1), collider="box", visible=False)

# Store all block positions in a set (all unique blocks with uniqe positions)
block_positions = set()
for x in range(world_size):
    for z in range(world_size):
        block_positions.add((x, -5, z))

# Dictionary to keep track of visible blocks due to render distance
visible_blocks = {}

# initialize the player controller
player=FirstPersonController(
  mouse_sensitivity=Vec2(100, 100),
  position=(5, 5, 5)
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
                visible_blocks[position] = Block(position=position, block_type="grass")
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