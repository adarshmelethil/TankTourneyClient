#!/usr/bin/env python
import sys
from TankTourneyClient import SimpleTank
from random import uniform
import time

old_time = time.time()
freq = 1

def newAction():
  return uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)

move, turn, fire = newAction()
def action(obv):

  global move, turn, fire, old_time
  now = time.time()
  if (now - old_time) > freq:
    old_time = now
    move, turn, fire = newAction()

  return move, turn, fire

player_num = 1;
if len(sys.argv) > 1:
  player_num = int(sys.argv[1])
  
tank = SimpleTank(action, player_num=player_num)
tank.run()
