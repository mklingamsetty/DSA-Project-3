########################################################### GLOBAL VARIABLES ##################################################
###############################################################################################################################
# World settings
class worldSettings:
    def __init__(self):
        self.world_size = 317                                                      # This creates a world with world_size x world_size amount of blocks (min must be 317)
        self.render_distance = 8                                                    # reduce this value if you have a slow computer
        self.total_tiles = self.world_size * self.world_size                        # Compute total number of tiles
        self.total_obstacles = int(0.15 * self.total_tiles)                         # Compute total number of obstacles (10% of total tiles)
        self.num_clusters = self.total_obstacles // 10                              # Number of Obstacle clusters (occupies 9 tiles)
        self.num_single_obstacles = self.total_obstacles - (self.num_clusters * 9)  # Number of Obstacle singles (occupies 1 tiles)
        self.player_spawn_x = self.world_size // 2                                  # Player spawn x position
        self.player_spawn_z = self.world_size - 10                                  # Player spawn z position
        self.player_speed = 8                                                       # Player movement speed
        self.home_size = 30                                                         # Home size x Home size
        self.home_min_z = self.world_size - 80                                      # Home min z position
        self.home_max_z = self.world_size - 50     
        
        from ursina import *
        
        # Load block textures
        self.block_textures = {
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
            "snow" : load_texture("minecraft_starter/assets/textures/snow.png"), #BFS and DFS
            # Add other block textures if needed
        }

        self.mob_textures = {
            "zombie" : load_texture("minecraft_starter/assets/textures/zombie.png"),
            "enderman" : load_texture("minecraft_starter/assets/textures/enderman.png"),
            "creeper" : load_texture("minecraft_starter/assets/textures/creeper.png"),
            "skeleton" : load_texture("minecraft_starter/assets/textures/skeleton.png"),
            # Add other mob textures if needed
        }

    # Home max z position

    def get_world_size(self):
        return self.world_size
    
    def get_render_distance(self):
        return self.render_distance
    
    def get_total_tiles(self):
        return self.total_tiles
    
    def get_total_obstacles(self):
        return self.total_obstacles
    
    def get_num_clusters(self):
        return self.num_clusters

    def get_num_single_obstacles(self):
        return self.num_single_obstacles
    
    def get_player_spawn_x(self):
        return self.player_spawn_x

    def get_player_spawn_z(self):
        return self.player_spawn_z

    def get_player_speed(self):
        return self.player_speed
    
    def get_home_size(self):
        return self.home_size
    
    def get_home_min_z(self):
        return self.home_min_z
    
    def get_home_max_z(self):
        return self.home_max_z
    

###############################################################################################################################
###############################################################################################################################