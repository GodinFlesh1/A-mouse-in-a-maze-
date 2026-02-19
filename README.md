# A-mouse-in-a-maze-# Robotics Assessment: A Mouse in a Maze
**Author:** Tamal Jana  
**Module:** Robotics (55-608216)  
**Platform:** VEX code VR (Dynamic Wall Maze)

## Task Description
The goal of this project is to program a VEX VR robot to autonomously navigate a randomly generated maze, find the exit, and return to the starting position using the most efficient route possible.

### Tasks Attempted:
1. **Maze Exploration:** Using a Right-Hand Rule algorithm to navigate corridors without hitting walls.
2. **Autonomous Mapping:** Real-time generation of a coordinate-based graph while exploring.
3. **Shortest Path Calculation:** Implementation of a Breadth-First Search (BFS) to identify the optimal route back to base.
4. **Return to Home:** Executing the optimized path to return to the starting point.

## How the Code Works
- **Graph Theory:** The maze is treated as a series of nodes (250mm apart). Connections are mapped only when the robot successfully moves between points.
- **Sensors:** - `Distance Sensor`: Used to detect walls before moving.
    - `Down Eye`: Used to detect the Red floor tiles signaling the maze exit.
- **Navigation:** The robot uses absolute heading control for the return trip to minimize turning time.


## Video Demonstration
https://shu.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=e5a1287a-3b3c-4ab5-bb09-b3f6001c091f
## References
- https://en.wikipedia.org/wiki/Maze-solving_algorithm#Wall_follower
- https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/