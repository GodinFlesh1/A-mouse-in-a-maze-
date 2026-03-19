# Robotics Assessment: A Mouse in a Maze

**Author:** Tamal Jana  
**Module:** Robotics (55-608216)  
**Platform:** VEX code VR (Dynamic Wall Maze)

## Task Description
The goal of this project is to program a VEX VR robot to autonomously navigate a randomly generated maze, find the exit, and return to the starting position using the most efficient route possible.

### Tasks Attempted:

1.  **Autonomous Mapping:** Using a Depth-First Search (DFS) algorithm to explore every reachable cell and build an adjacency list of the environment in real-time.
2.  **Red Tile Detection:** Utilizing the `down_eye` sensor to identify the exit node and record its grid coordinates for future navigation.
3.  **Shortest Path Calculation:** Implementation of a Breadth-First Search (BFS) after mapping to identify the mathematically optimal route between the start and exit.
4.  **Return to Home:** Executing the optimized BFS path with visual tracking (color-coded pen) to return to the starting point.

## How the Code Works

  - **Graph Theory:** The maze is treated as a series of nodes (250mm apart). The robot uses a stack-based DFS to "uncover" the maze and a dictionary-based graph to store connections.
  - **Sensors:** - `Distance Sensor`: Used to survey all four cardinal directions at each cell to detect wall openings.
      - `Down Eye`: Used to detect the Red floor tiles signaling the maze exit.
  - **Navigation:** The robot employs a three-phase system: Exploration (mapping), the Race (Shortest path to exit via BFS), and the Return (Shortest path home via BFS).

## Video Demonstration
https://shu.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=c4f3b41b-3f13-415e-a320-b4120026e12b

## References
-https://en.wikipedia.org/wiki/Maze-solving_algorithm#Tremaux's_algorithm

-https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/

-https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/