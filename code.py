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

# ═══════════════════════════════════════════════════════════════════
#  Project     : Distinction Level Maze Solver
#  Author      : Tamal Jana
DIR_X = [ 0,  1,  0, -1]
DIR_Y = [ 1,  0, -1,  0]

CELL_MM         = 250   
WALL_THRESHOLD  = 200   

class MazeBot:

    def __init__(self):
        self.map_graph   = {}      
        self.visited     = set()   
        self.gx          = 0       
        self.gy          = 0       
        self.heading_idx = 0       
        self.exit_node   = None    

    def add_edge(self, x1, y1, x2, y2):
        n1, n2 = (x1, y1), (x2, y2)
        self.map_graph.setdefault(n1, [])
        self.map_graph.setdefault(n2, [])
        if n2 not in self.map_graph[n1]:
            self.map_graph[n1].append(n2)
        if n1 not in self.map_graph[n2]:
            self.map_graph[n2].append(n1)

    def turn_to(self, target_h):
        diff = (target_h - self.heading_idx) % 4
        if diff == 1:
            drivetrain.turn_for(RIGHT, 90, DEGREES)
        elif diff == 2:
            drivetrain.turn_for(RIGHT, 180, DEGREES)
        elif diff == 3:
            drivetrain.turn_for(LEFT, 90, DEGREES)
        self.heading_idx = target_h

    def step(self, h, nx, ny):
        self.turn_to(h)
        drivetrain.drive_for(FORWARD, CELL_MM, MM)
        self.gx, self.gy = nx, ny

    def bfs(self, start, goal):
        if start == goal:
            return [start]
        queue   = [[start]]
        visited = {start}
        while queue:
            path = queue.pop(0)
            node = path[-1]
            for neighbour in self.map_graph.get(node, []):
                if neighbour not in visited:
                    if neighbour == goal:
                        return path + [neighbour]
                    visited.add(neighbour)
                    queue.append(path + [neighbour])
        return []

def follow_path(bot, path):
    
    for i in range(1, len(path)):
        cur = path[i - 1]
        nxt = path[i]
        dx  = nxt[0] - cur[0]
        dy  = nxt[1] - cur[1]
        for h in range(4):
            if DIR_X[h] == dx and DIR_Y[h] == dy:
                bot.step(h, nxt[0], nxt[1])
                break

def main():
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)

    bot   = MazeBot()
    START = (0, 0)

    bot.visited.add((0, -1))

    # PHASE 1 : Full DFS exploration and maze mapping
    brain.print("Phase 1: Mapping maze...")

    bot.visited.add(START)
    dfs_stack = [START]  
    while dfs_stack:
        cx, cy = bot.gx, bot.gy

        if down_eye.detect(RED):
            if bot.exit_node is None:
                bot.exit_node = (cx, cy)
                brain.print("Exit at", bot.exit_node)
            dfs_stack.pop()
            if not dfs_stack:
                break
            bx, by = dfs_stack[-1]
            dx, dy = bx - cx, by - cy
            for h in range(4):
                if DIR_X[h] == dx and DIR_Y[h] == dy:
                    bot.step(h, bx, by)
                    break
            continue

        first_unvisited_h  = None
        first_unvisited_nx = None
        first_unvisited_ny = None

        for h in range(4):
            bot.turn_to(h)                          
            nx = cx + DIR_X[h]
            ny = cy + DIR_Y[h]

            if distance.get_distance(MM) > WALL_THRESHOLD:
                bot.add_edge(cx, cy, nx, ny)

                if (nx, ny) not in bot.visited and first_unvisited_h is None:
                    first_unvisited_h  = h
                    first_unvisited_nx = nx
                    first_unvisited_ny = ny
        if first_unvisited_h is not None:
            next_cell = (first_unvisited_nx, first_unvisited_ny)
            bot.visited.add(next_cell)
            dfs_stack.append(next_cell)
            bot.step(first_unvisited_h, first_unvisited_nx, first_unvisited_ny)
        else:
            dfs_stack.pop()
            if not dfs_stack:
                break   

            bx, by = dfs_stack[-1]
            dx, dy = bx - cx, by - cy
            for h in range(4):
                if DIR_X[h] == dx and DIR_Y[h] == dy:
                    bot.step(h, bx, by)
                    break
    brain.clear()
    brain.print("Map done:", len(bot.visited) - 1, "cells")   

    if bot.exit_node is None:
        brain.print("ERROR: No exit found!")
        return
    # PHASE 2 : Navigate the BFS-shortest path from start to exit
    brain.print("Phase 2: Racing to exit...")

    path_to_exit = bot.bfs(START, bot.exit_node)
    if not path_to_exit:
        brain.print("ERROR: No path to exit!")
        return

    brain.print("Shortest path:", len(path_to_exit) - 1, "steps")

    pen.set_pen_color(BLUE)
    pen.move(DOWN)
    follow_path(bot, path_to_exit)
    pen.move(UP)

    brain.clear()
    brain.print("Exit reached!")

    # PHASE 3 : Navigate the BFS-shortest path back to start (home)
    brain.print("Phase 3: Returning home...")

    path_to_home = bot.bfs(bot.exit_node, START)
    if not path_to_home:
        brain.print("ERROR: No path home!")
        return

    pen.set_pen_color(GREEN)
    pen.move(DOWN)
    follow_path(bot, path_to_home)
    pen.move(UP)

    brain.clear()
    brain.print("Home! Mission complete.")
    brain.print("Cells mapped:", len(bot.visited) - 1)
    brain.print("Exit path:", len(path_to_exit) - 1, "steps")


vr_thread(main)