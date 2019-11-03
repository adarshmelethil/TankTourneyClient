#!/usr/bin/env python
import sys
from TankTourneyClient import SimpleTank
import random
import time
import matplotlib.pyplot as plt
import numpy as np


def rotate(vector, degree):
  theta = np.radians(degree)
  c, s = np.cos(theta), np.sin(theta)
  R = np.array(
    ((c,-s),
     (s, c)))
  return np.matmul(R, vector)

def lidarToObstacle(obv):
  obstacle_x = []
  obstacle_y = []
  position = np.array([obv["Position"]["X"], obv["Position"]["Y"]])
  direction = np.array([obv["Direction"]["X"], obv["Direction"]["Y"]])
  degree_increment = 360/len(obv["Lidar"])

  for i in range(len(obv["Lidar"])):
    direction_vector = rotate(direction, (i * degree_increment))
    obsticle_location = position + (direction_vector * obv["Lidar"][i])

    obstacle_x.append(obsticle_location[0])
    obstacle_y.append(obsticle_location[1])

  return obstacle_x, obstacle_y

obstacle_xs = []
obstacle_ys = []
plt.ion()
def plotObsticles(obv):
  global obstacle_xs, obstacle_ys
  # xs, ys = lidarToObstacle(obv)
  # obstacle_xs.extend(xs)
  # obstacle_ys.extend(ys)

  # plt.plot(obstacle_xs, obstacle_ys, ".k")
  # plt.plot(xs, ys, ".k")

  plt.plot([obv["Position"]["X"]], [obv["Position"]["Y"]], ".g")
  if old_pos is not None:
    plt.plot([old_pos[0]], [old_pos[1]], "or")

  plt.draw()
  plt.pause(0.0001)
  plt.clf()

old_pos = None
old_dir = np.array([1, 0])
def update_prediction(obv):
  global old_pos, old_dir
  if old_pos is not None:
    old_dir = rotate(old_dir, -obv["AngleTurned"])
    old_pos = old_pos + ( old_dir * obv["DistanceTravelled"] ) 
  else:
    old_pos = np.array([obv["Position"]["X"], obv["Position"]["Y"]])
    old_dir = np.array([obv["Direction"]["X"], obv["Direction"]["Y"]])

def newAction(move, turn, fire):
  if move != 0:
    move = 0
    turn = 0
    while not turn:
      turn = random.randint(-1,1)
  else:
    move = 0
    turn = 0
    while not move:
      move = random.randint(-1,1)
  return move, turn, fire

import time
move, turn, fire, refresh = 0, 0, 0, False
old_time = time.time()
total = 0
freq = 2
actions = 0
def action(obv):
  global move, turn, fire, old_time, total
  now = time.time()
  
  if (now - old_time) > freq and refresh:
    old_time = now
    move, turn, fire = newAction(move, turn, fire)

  update_prediction(obv)
  # print(total, end="\r")

  myend = "\r" if obv["DistanceTravelled"] == 0 else "\n"

  real = (obv["Position"]["X"], obv["Position"]["Y"])
  mine = old_pos
  error = (real[0]-mine[0], real[1]-mine[1])
  print("({:06.4f}) - [{:06.4f}, {:06.4f}] = [{:06.4f}, {:06.4f}], err: [{:06.4f}, {:06.4f}]".format(
    obv["DistanceTravelled"], mine[0], mine[1], real[0], real[1], error[0], error[1]), end=myend)

  time.sleep(0.01)
  # plotObsticles(obv)
  
  global actions
  if actions < 1:
    actions += 1

  # if actions == 1:
  #   actions += 1
  #   return 0, 1, 0
  # else:
  #   return None
  return None

player_num = 1;
if len(sys.argv) > 1:
  player_num = int(sys.argv[1])
  
tank = SimpleTank(action, player_num=player_num)
tank.run()

