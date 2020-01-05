import random

class LambdaPart():
  def __init__(self, func):
    self.func = func

  def update(self, *args):
    return self.func(*args)

