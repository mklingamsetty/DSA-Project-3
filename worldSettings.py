from ursina import Entity
########################################################### GLOBAL VARIABLES ##################################################
###############################################################################################################################
# World settings
world_size = 1000                                           # This creates a world with 100,489 blocks
render_distance = 8                                         # reduce this value if you have a slow computer
total_tiles = world_size * world_size                       # Compute total number of tiles
total_obstacles = int(0.1 * total_tiles)                    # Compute total number of obstacles (10% of total tiles)
num_clusters = total_obstacles // 10                        # Number of Obstacle clusters (occupies 9 tiles)
num_single_obstacles = total_obstacles - (num_clusters * 9) # Number of Obstacle singles (occupies 1 tiles)
player_spawn_x = world_size // 2                            # Player spawn x position
player_spawn_z = world_size - 10                            # Player spawn z position
player_speed = 8                                           # Player movement speed
home_size = 30                                              # Home size x Home size
home_min_z = world_size - (5*home_size)                     # Home min z position
home_max_z = world_size - home_size - 10                    # Home max z position

# create boundaries
leftWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(-1, 0, (world_size / 2) - 0.5), collider="box", visible=False)
rightWall = Entity(model="cube", scale=(1, world_size, world_size + 1), position=(world_size , 0, (world_size / 2) - 0.5), collider="box", visible=False)
frontWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, world_size), collider="box", visible=False)
backWall = Entity(model="cube", scale=(world_size + 1, world_size, 1), position=(world_size / 2, 0, -1), collider="box", visible=False)
###############################################################################################################################
###############################################################################################################################
