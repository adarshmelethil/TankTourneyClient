#!/usr/bin/env python
import sys
from tanks import SimpleTank
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def action(obv):
  print(obv)
  return 1, 0

player_num = 1;
if len(sys.argv) > 1:
  player_num = int(sys.argv[1])
  
tank = SimpleTank(action, player_num=player_num, logger=logger)
tank.run()
