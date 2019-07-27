#!/usr/bin/env python

from tanks import SimpleTank

def action(obv):
  print(obv)
  return 1, 0

tank = SimpleTank(action)
tank.run()
