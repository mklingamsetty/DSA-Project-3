Data Structures and Algorthims Fall 2024 

Project 3 - "I Want To Go Home!"
Team Name: I Survived Segmentation Fault

Algorithms:
    Breadth First Search (BFS)
    Depth First Search (DFS)
    Dijkstra's Algorithm

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

How to Run Code:

After installing ursina and Pillow, press the 'run' button and you should be redirected to the game window.
You will be transported into a 3D world which takes in the user inputs 'W','S','A','D' to move forward, backward, left and right respecively.
The space bar will allow you to jump.
Upon pressing 'm', the minimap will maximize to display a large map as well as the interface to choose the algorithm to guide you home.
You can choose between Breadth First Search, Depth First Search, and Dijkstra's Algorithm. After selecting your algorithm of choice, wait for the 
algorithm to visit the nearby nodes until it reaches the 'home' waypoint, to which the map will regenerate, highlighting visited nodes in purple
and showing the path from player location to home in blue. 
Pressing 'r' will allow the user to return to the game, and if they look down they will notice that the algorithm they selected has been revealed to them on the ground,
effectively guiding them to the 'home' location.
When following the path home, the player must be careful, as there are various obstacles in their path. Trees and stones are in their way to block their path,
and pools of water serve to slow the player down. Additionally, coming into contact with lava lakes and mobs will cause the player to take damage,
and after falling to 0 health, the application will quit.
Additionally, whenn the player is finished with the game, they may close the application by pressing 'q'.