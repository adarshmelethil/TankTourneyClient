# import the pygame module, so you can use it
import sys
import os
import json
import time
import threading
from math import radians, sin, cos

import pygame

PLAYER_SIZE=(1.5, 1.6)
OBSTACLE_SIZE=(0.5*9.290687, 0.2*11.32651)

WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(0,255,0)

BACKGROUND=(200, 200, 200)
TERRAIN=(50, 50, 50)
OBSTACLE=(140, 40, 40)
PLAYER=(200, 50, 50)


class DebugDisplayPart():
  def __init__(self, size=(600, 600), padding=20):
    pygame.init()
    pygame.display.set_caption("Map")
    
    self.size = size
    self.DISPLAY=pygame.display.set_mode(self.size)
    self.running = True

    self.padding = padding
    self.position = (0, 0)
    self.edges = []
    self.obstacles = []

  def update(self, position, edges, obstacles):
    self.updateData(position, edges, obstacles)
    self.updateScreen()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

    pygame.display.update()

  def unityValToPy(self, val, offset):
    return int(((val+offset)*self.scaler)+self.padding)

  def unityToPy(self, points):
    return (
      self.unityValToPy(points[0], self.x_offset),
      self.unityValToPy(points[1], self.y_offset))


  def updateScaler(self):
    x_edge, y_edge, _ = list(zip(*self.edges))
    x_min_edge = min(x_edge)
    y_min_edge = min(y_edge)

    self.x_offset = 0 - (x_min_edge)
    self.y_offset = 0 - (y_min_edge)
    x_max_edge = max(x_edge) + self.x_offset
    y_max_edge = max(y_edge) + self.y_offset

    max_range = max([x_max_edge, y_max_edge])
    self.scaler = (min(self.size)-(self.padding*2))/max_range

  def dictToArr(self, d):
    return (d["X"], d["Y"], d["R"])

  def updateData(self, position, edges, obstacles):
    if None in [position, edges, obstacles]:
      return
    self.position = self.dictToArr(position)
    self.edges = [self.dictToArr(e) for e in edges]
    new_obstacles = [self.dictToArr(o) for o in obstacles]
    for new_obstacle in new_obstacles:
      if new_obstacle not in self.obstacles:
        self.obstacles.append(new_obstacle)
    self.updateScaler()


  def rotate(self, point, origin, angle):
    angle = radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return int(qx), int(qy)

  def customDraw(self, col, points):
    # print(points)
    for i in range(1, len(points)):
      pygame.draw.line(self.DISPLAY, col, points[i-1], points[i])
    pygame.draw.line(self.DISPLAY, col, points[-1], points[0])

  def drawRect(self, pos, size, color):
    half_width = size[0]/2
    half_height = size[1]/2
    points = [
      (pos[0]-half_width, pos[1]-half_height),
      (pos[0]+half_width, pos[1]-half_height),
      (pos[0]+half_width, pos[1]+half_height),
      (pos[0]-half_width, pos[1]+half_height)]
    
    # pygame.draw.polygon(self.DISPLAY, (0, 255, 0), points)
    center = (pos[0], pos[1])
    points = [self.rotate(p, center, pos[2]) for p in points]
    points = [self.unityToPy(p) for p in points]
    
    # pygame.draw.polygon(self.DISPLAY, color, points)
    self.customDraw(color, points)
    
    pycenter = self.unityToPy(center)
    pygame.draw.circle(self.DISPLAY, (255,0,0), pycenter, 2)


  def updateScreen(self):
    self.DISPLAY.fill(BACKGROUND)
    if not self.edges:
      return

    # Playable area
    edges = [self.unityToPy(e) for e in self.edges]
    edge_x = [e[0] for e in edges]
    edge_y = [e[1] for e in edges]
    edge_rect = (min(edge_x), min(edge_y), max(edge_x)-min(edge_x), max(edge_y)-min(edge_y))
    pygame.draw.rect(self.DISPLAY, TERRAIN, edge_rect)

    # player location
    self.drawRect(self.position, PLAYER_SIZE, PLAYER)

    for obs in self.obstacles:
      self.drawRect(obs, OBSTACLE_SIZE, OBSTACLE)

  def threadLoop(self):
    while self.running:
      self.updateScreen()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      if self.running:
        pygame.display.update()
      time.sleep(0)
        

  def shutdown(self):
    self.running = False
    pygame.quit()


def main():
  d = DebugDisplayPart()

  obs_folder = "observations"
  observations = []
  for obs in os.listdir(obs_folder):
    with open(os.path.join(obs_folder, obs), "r") as fp:
      observations.append(json.load(fp))
  
  obv_index = 0
  while d.running:
    d.update(**observations[obv_index])
    # obv_index += 1
    # obv_index %= len(observations)

  d.shutdown()

if __name__=="__main__":
  main()
