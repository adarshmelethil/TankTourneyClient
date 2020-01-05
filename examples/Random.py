#!/usr/bin/env python
'''
Usage:
  Random.py (1|2)
'''
from docopt import docopt
import sys
from TankTourneyClient import Tank, ControllerPart, ObservationPart, LambdaPart
from random import uniform
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

def main(player_number):
  tank = Tank()

  def randomAction():
    return uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)

  tank.add(LambdaPart(randomAction), outputs=["rnd/fwd", "rnd/turn", "rnd/fire"])

  tank.add(ObservationPart(player_number),
    outputs=["flag", "lidar", "distanceTravelled", "angleTurned", "paused", "debug/position", "debug/direction", "debug/obstacles"],
    threaded=True)

  def prettyPrint(*args):
    print(f"{', '.join(map(str, args))}")
  tank.add(LambdaPart(prettyPrint), inputs=["debug/position", "debug/direction"])

  def printObv(obv):
    print(type(obv))
    if type(obv) is None:
      print(len(obv))
      print(obv[0])
  tank.add(LambdaPart(printObv), inputs=["debug/obstacles"])

  tank.add(ControllerPart(player_number), inputs=["rnd/fwd", "rnd/turn", "rnd/fire"])

  tank.start(rate_hz=1)

if __name__ == "__main__":
  arguments = docopt(__doc__, version='Naval Fate 2.0')
  
  if arguments["1"]:
    main(1)
  else:
    main(2)

  # main()
