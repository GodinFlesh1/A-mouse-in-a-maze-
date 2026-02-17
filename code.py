#region VEXcode Generated Robot Configuration
import math
import random
from vexcode_vr import *

brain=Brain()

drivetrain = Drivetrain("drivetrain", 0)
pen = Pen("pen", 8)
pen.set_pen_width(THIN)
left_bumper = Bumper("leftBumper", 2)
right_bumper = Bumper("rightBumper", 3)
front_eye = EyeSensor("frontEye", 4)
down_eye = EyeSensor("downEye", 5)
front_distance = Distance("frontdistance", 6)
distance = front_distance
magnet = Electromagnet("magnet", 7)
location = Location("location", 9)

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
#   Project:      Distinction Level Maze Solver
#   Author:       TAMAL JANA
#   Description:  Explores, Maps, and Calculates Shortest Path
# ------------------------------------------

class MazeBot:
    def __init__(self):
        self.GRID_SIZE = 250  
    
        self.map_graph = {}
        
        self.gx = 0
        self.gy = 0
        
        self.heading_idx = 0 

    def record_movement(self, new_gx, new_gy):
       
        current_node = (self.gx, self.gy)
        new_node = (new_gx, new_gy)
        
        if current_node not in self.map_graph: self.map_graph[current_node] = []
        if new_node not in self.map_graph: self.map_graph[new_node] = []
        
        if new_node not in self.map_graph[current_node]:
            self.map_graph[current_node].append(new_node)
        if current_node not in self.map_graph[new_node]:
            self.map_graph[new_node].append(current_node)
            
       
        self.gx = new_gx
        self.gy = new_gy

    def solve_shortest_path_bfs(self, target_node):
       
        start_node = (self.gx, self.gy)
        
        queue = [[start_node]]
        visited = {start_node}
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node == target_node:
                return path
            
            if node in self.map_graph:
                for neighbor in self.map_graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
        return []

def main():
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    
    bot = MazeBot()
    
    brain.clear()
    brain.print("Phase 1: Mapping Maze...")
    
    # ---------------------------------------------------------
    # PHASE 1: EXPLORATION (Right-Hand Rule)
    # ---------------------------------------------------------
    while not down_eye.detect(RED):
        
        drivetrain.turn_for(RIGHT, 90, DEGREES)
        bot.heading_idx = (bot.heading_idx + 1) % 4 
        
        
        if distance.get_distance(MM) > 200:
            drivetrain.drive_for(FORWARD, 250, MM)
            
            
            dx, dy = 0, 0
            if bot.heading_idx == 0: dy = 1   # North
            elif bot.heading_idx == 1: dx = 1 # East
            elif bot.heading_idx == 2: dy = -1 # South
            elif bot.heading_idx == 3: dx = -1 # West
            bot.record_movement(bot.gx + dx, bot.gy + dy)
            continue 
            
        
        drivetrain.turn_for(LEFT, 90, DEGREES)
        bot.heading_idx = (bot.heading_idx - 1) % 4
        
        if distance.get_distance(MM) > 200:
            drivetrain.drive_for(FORWARD, 250, MM)
            
            dx, dy = 0, 0
            if bot.heading_idx == 0: dy = 1
            elif bot.heading_idx == 1: dx = 1
            elif bot.heading_idx == 2: dy = -1
            elif bot.heading_idx == 3: dx = -1
            bot.record_movement(bot.gx + dx, bot.gy + dy)
            continue

        
        drivetrain.turn_for(LEFT, 90, DEGREES)
        bot.heading_idx = (bot.heading_idx - 1) % 4
        
        if distance.get_distance(MM) > 200:
            drivetrain.drive_for(FORWARD, 250, MM)
            
            dx, dy = 0, 0
            if bot.heading_idx == 0: dy = 1
            elif bot.heading_idx == 1: dx = 1
            elif bot.heading_idx == 2: dy = -1
            elif bot.heading_idx == 3: dx = -1
            bot.record_movement(bot.gx + dx, bot.gy + dy)
            continue

        
        drivetrain.turn_for(LEFT, 90, DEGREES)
        bot.heading_idx = (bot.heading_idx - 1) % 4
        drivetrain.drive_for(FORWARD, 250, MM)
        
        dx, dy = 0, 0
        if bot.heading_idx == 0: dy = 1
        elif bot.heading_idx == 1: dx = 1
        elif bot.heading_idx == 2: dy = -1
        elif bot.heading_idx == 3: dx = -1
        bot.record_movement(bot.gx + dx, bot.gy + dy)

    # ---------------------------------------------------------
    # PHASE 2: CALCULATE FASTEST ROUTE
    # ---------------------------------------------------------
    brain.clear()
    brain.print("Exit Found! Calculating Path...")
    
    fastest_path = bot.solve_shortest_path_bfs((0, 0))
    
    if not fastest_path:
        brain.print("Error: No path home.")
        stop()

    # ---------------------------------------------------------
    # PHASE 3: RETURN HOME
    # ---------------------------------------------------------
    brain.print("Returning Home (Optimized)...")
    pen.set_pen_color(GREEN)
    pen.move(DOWN)
    
    for i in range(1, len(fastest_path)):
        target = fastest_path[i] 
        current = fastest_path[i-1] 
        
        req_heading = 0
        if target[1] > current[1]: req_heading = 0   # North
        elif target[0] > current[0]: req_heading = 1 # East
        elif target[1] < current[1]: req_heading = 2 # South
        elif target[0] < current[0]: req_heading = 3 # West
        
       
        drivetrain.turn_to_heading(req_heading * 90, DEGREES)
        drivetrain.drive_for(FORWARD, 250, MM)
        
    brain.clear()
    brain.print("Assessment Complete.")

vr_thread(main)