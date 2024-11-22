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

Credits/References:
   - http://www.codingwithruss.com/ursina/minecraft-in-python-3d-game-tutorial/
   - https://www.kenney.nl/assets/tower-defense-top-down
   - https://www.ursinaengine.org/installation.html
   - https://www.ursinaengine.org/documentation.html
   - https://www.youtube.com/watch?v=tONNC-bWSFM&ab_channel=BeauCarnes
   - https://sketchfab.com/3d-models/minecraft-torch-e88c4214d4bc4437ae6d249237591071
   - https://www.youtube.com/watch?v=IWhA6lV_sxg&ab_channel=Codeandcraft
   - https://sketchfab.com/3d-models/minecraft-wood-block-d498c39e40974966836fc1140c263d22


********** DELETE EACH TASK WHEN FINISHED **********
    TASKS !!!!
    - Home Creation
        - Set bounds of where house can spawn
        - Build design of the house with given block textures
            - (OPTIONAL) get a door model and texture
            - (OPTIONAL) get a window model and texture
    - Construct our Algorithms
        - BFS implementation
        - DFS implementation
    - Player UI
        - Map
            - When the 'k' key is pressed, a new miniature window, "MAP" should now appear
            - User should be able to select with algorithm to use (BFS or DFS)
            - Map should contain positions of the following:
                - Player position
                - obstacle positions
                - home position
            - We must show how the algorithms work, be shading in the pixels in the Map
                - similar to how the GTA project worked
            - (OPTIONAL) after best route is found, shade the actual blocks on the actual world to help
    - OPTIONAL (WORK ON THIS LAST)
        - music (default minecraft music)
        - block effects
            - water -> player speed + 5
            - lava -> player speed - 5
        