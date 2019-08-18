import sys
import socket
import json

BUFFER_SIZE = 1024

class TankBase():
  def __init__(self, player_num, control_port=26000, obv_port=27000, game_addr="127.0.0.1", retry_count=10):

    self.ctrl_addr = (game_addr, control_port+player_num)
    self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.obv_addr = (game_addr, obv_port+player_num)
    self.obv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.RETRY_COUNT = retry_count
    self.OBV_BYTE_SIZE = 2048

  def getObservation():
    obv = {}
    for _ in range(self.RETRY_COUNT):
      try:
        sock.sendto(b'obv', addr)
        # Send data
        obv_data, server_addr = sock.recvfrom(BYTE_SIZE)
        obv = json.loads(obv_data)

      except socket.timeout as sto:
        eprint("Timeout: {}".format(sto), )
      finally:
        sock.close()

      if obv is not None:
        return obv

  def clampAction(self, val, val_name, min_val=-1, max_val=1):
    if val > max_val:
      eprint("Received '{0}' for {1}, should be less than {2}".format(val, val_name, max_val))
      return max_val
    elif val < min_val:
      eprint("Received '{0}' for {1}, should be greater than {2}".format(val, val_name, min_val))
      return min_val
    else:
      return val

  def actionToString(self, move, turn, fire):
    move = self.clampAction(move, "movement")
    turn = self.clampAction(turn, "turn")
    fire = self.clampAction(fire, "fire")

    return "{:.4f},{:.4f},{:.4f}".format(move, turn, fire)


  def run(self):
    winner = None
    import time
    try:
      # Initial action used to contact server to get first observation
      move, turn, fire = 0, 0, 0
      obv = None
      while winner is None:
        # Take action
        if obv:
          move, turn, fire = self.action(obv)
        action_msg = self.actionToString(move, turn, fire)
        self.ctrl_socket.sendto(bytearray(action_msg, 'utf8'), self.ctrl_addr)

        # Wait for observation
        obv_data, server_addr = self.ctrl_socket.recvfrom(self.OBV_BYTE_SIZE)
        eprint("Obv: '{}' bytes".format(len(obv_data)))
        obv = json.loads(obv_data)

        if obv is not None and "winner" in obv:
          winner = obv["winner"]
          break

    except Exception as e:
      raise e
    finally:
      self.ctrl_socket.close()
    
    return winner

  def action(self, obv):
    raise NotImplementedError()

class SimpleTank(TankBase):
  def __init__(self, action_func, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.action = action_func

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)
