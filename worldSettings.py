########################################################### GLOBAL VARIABLES ##################################################
###############################################################################################################################
# World settings
class worldSettings:
    def __init__(self):
        self.world_size = 317                                                       # This creates a world with world_size x world_size amount of blocks (min must be 317)
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
        self.home_max_z = self.world_size - 50                                      # Home max z position

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