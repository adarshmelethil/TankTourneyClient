#!/usr/bin/env python
import sys
from TankTourneyClient import SimpleTank
from random import uniform
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

old_time = time.time()
freq = 1

def newAction():
  return uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)


printObv = False
move, turn, fire = newAction()
def action(obv):

  global move, turn, fire, old_time, printObv
  now = time.time()
  if (now - old_time) > freq:
    old_time = now
    move, turn, fire = newAction()

  if not printObv:
    pp.pprint(obv)
    printObv = True

  print("Pos: ({}, {}) \t Dist: {} \t Angle: {}".format(obv["Position"]["X"], obv["Position"]["Y"], obv["DistanceTravelled"], obv["AngleTurned"]), end="\r")
  return move, turn, fire

player_num = 1;
if len(sys.argv) > 1:
  player_num = int(sys.argv[1])
  
tank = SimpleTank(action, player_num=player_num)
tank.run()
