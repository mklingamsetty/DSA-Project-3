Data Structures and Algorthims Fall 2024 

Project 3 - "I Want To Go Home!"

Algorithms:
    Breadth First Search (BFS)
    Depth First Search (DFS)

Members:
    Murali Lingamsetty
    Zhiting Li
    Rayyan Shaikh

Dependencies Installed:
    pip install ursina
    pip install Pillow

Credits/References:
   - http://www.codingwithruss.com/ursina/minecraft-in-python-3d-game-tutorial/
   - https://www.kenney.nl/assets/tower-defense-top-down
   - https://www.ursinaengine.org/installation.html
   - https://www.ursinaengine.org/documentation.html
   - https://www.youtube.com/watch?v=tONNC-bWSFM&ab_channel=BeauCarnes
   - https://sketchfab.com/3d-models/minecraft-torch-e88c4214d4bc4437ae6d249237591071
   - https://www.youtube.com/watch?v=IWhA6lV_sxg&ab_channel=Codeandcraft
   - https://sketchfab.com/3d-models/minecraft-wood-block-d498c39e40974966836fc1140c263d22
   - https://sketchfab.com/3d-models/minecraft-enderman-216552744553461d960dd0cdf3a0592a
   - https://sketchfab.com/3d-models/zombie-minecraft-9fb165f3ecf443e1af6ad2cb39f8f161
   - https://sketchfab.com/3d-models/minecraft-creeper-fd66182f07e5408eb04fa5a88ae16055#download
   - https://sketchfab.com/3d-models/minecraft-skeleton-3ea04380d84f498a81f07043acad19f0#download
   - https://pillow.readthedocs.io/en/stable/



********** DELETE EACH TASK WHEN FINISHED **********
    TASKS !!!!
    - Edit our Algorithms
        - Both Algorithms are written out still needs to be tested
    - Player UI
        - MiniMap
            - WARNING : game start up will be a bit longer (like extra 5-10secs) due to generating an image
            - I have created an Image using the Pillow Library in python to represent the world 2 Dimensional.
              The way I did it was by making an image with a pixel count of world_size x world_size as seen in the GameScreen class.
              There is a function called draw_minimap() which draws on the blank image pixel by pixel according to what the block is (whether a free space or obstacle or home)
              *** TASKS FOR MINIMAP ***
                Preliminary Fix (OPTIONAL FIX CAN BE FIXED LATER): There is a bug with displaying the home on the minimap, 
                 it displays parts of it like smal/ clusters. Maybe a problem with how the home is generated?? Look into it plz.

                1. We must now add this image as a texture to the MiniMap entity I have made in the top right of the GameScreen
                2. Now we have to focus the image. Since everything is so small on the image (a pixel is very small) we need to 
                   zoom in on the player's position and when the player moves, so does the map. 
                3. When we press the 'm' key, we need to be able to show a HUD (Heads-Up-Display) (Defintion for Zhiting) which
                   basically creates a big RECTANGLE entity in the middle of the screen, displays the minimap on the LEFT and 2 options on the RIGHT (BFS or DFS).  
                    - We can use a key input ('B' key for BFS or 'D' key for DFS)                
                    - We must show how the algorithms work, be shading in the pixels in the Map
                        - similar to how the GTA project worked
                        - (OPTIONAL) after best route is found, shade the actual blocks on the actual world to help
    
    - OPTIONAL (WORK ON THIS LAST)
        - IF WE DO THIS THEN WE MIGHT NEED TO USE DJISKTRAS!!!!
        - music (default minecraft music)
        - block effects
            - water -> player speed + 5
            - lava -> player speed - 5
        