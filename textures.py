from ursina import *
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
    "leaves" : load_texture("minecraft_starter/assets/textures/leaf.png"),
    "wall" : load_texture("minecraft_starter/assets/textures/wallStone.png"),
    "darkstone" : load_texture("minecraft_starter/assets/textures/stone02.png"),
    "mud" : load_texture("minecraft_starter/assets/textures/groundMud.png"),
    "trimmedGrass" : load_texture("minecraft_starter/assets/textures/stone06.png"),
    # Add other block textures if needed
}

mob_textures = {
    "zombie" : load_texture("minecraft_starter/assets/textures/zombie.png"),
    "enderman" : load_texture("minecraft_starter/assets/textures/enderman.png"),
    "creeper" : load_texture("minecraft_starter/assets/textures/creeper.png"),
    "skeleton" : load_texture("minecraft_starter/assets/textures/skeleton.png"),
    # Add other mob textures if needed
}