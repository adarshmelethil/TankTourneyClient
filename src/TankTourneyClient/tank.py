import time

from collections.abc import Iterable
from threading import Thread

'''
Vehicle pattern from Donkeycar
https://github.com/autorope/donkeycar/blob/dev/donkeycar/vehicle.py
'''

class Tank():
  def __init__(self):
    self.datastore = {}
    self.parts = []
    self.on = False

  def add(self, part, inputs=[], outputs=[], threaded=False):
    part_info = {
      "part": part,
      "inputs": inputs,
      "outputs": outputs,
    }
    if threaded:
      part_info["thread"] = Thread(target=part.threadLoop, args=())
      part_info["thread"].daemon = True

    self.parts.append(part_info)

  def start(self, rate_hz=10, verbose=False):
    try:
      self.on = True

      self.startThreadedParts()
      while self.on:
        start_time = time.time()
        self.updateParts()

        sleep_time = 1.0 / rate_hz - (time.time() - start_time)
        if sleep_time > 0.0:
          time.sleep(sleep_time)
        else:
          if verbose:
            print('WARN::Vehicle: jitter violation in vehicle loop '
                  'with {0:4.0f}ms'.format(abs(1000 * sleep_time)))

    except KeyboardInterrupt:
      pass
    finally:
      self.stop()

  def stop(self):
    for part in self.parts:
      try:
          part['part'].shutdown()
      except AttributeError:
          pass
      except Exception as e:
          print(e)

  def getData(self, *keys):
    if isinstance(keys, Iterable):
      return [self.datastore.get(key) for key in keys]
    return [self.datastore.get(keys)]

  def putData(self, **kwargs):
    self.datastore.update(kwargs)

  def startThreadedParts(self):
    for part in self.parts:
      if "thread" in part:
        part["thread"].start()
  def updateParts(self):
    for part in self.parts:
      part_outputs = part['part'].update(*self.getData(*part["inputs"]))
      if part_outputs is not None:
        if not isinstance(part_outputs, Iterable):
          part_outputs = [part_outputs]
        self.putData(**dict(zip(part["outputs"], part_outputs)))


