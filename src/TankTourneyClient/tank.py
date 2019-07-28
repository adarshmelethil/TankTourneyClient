
import logging
import socket
import json

BUFFER_SIZE = 1024

class TankBase():
  def __init__(self, player_num, port=26000, game_addr="127.0.0.1", logger=None):
    self.logger = logger
    if not self.logger:
      self.logger = logging.getLogger(__name__)
      logger.setLevel(logging.INFO)

    self.port = port
    self.player_num = player_num
    self.game_addr = game_addr

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def clampAction(self, val, val_name, min_val=-1, max_val=1):
    if val > max_val:
      self.logger.warning("Received '{0}' for {1}, should be less than {2}".format(val, val_name, max_val))
      return max_val
    elif val < min_val:
      self.logger.warning("Received '{0}' for {1}, should be greater than {2}".format(val, val_name, min_val))
      return min_val
    else:
      return val

  def run(self):
    winner = None
    try:
      self.socket.connect((self.game_addr, self.port+self.player_num))
      
      # start communication
      self.socket.sendall("obv".encode("utf-8"))
      obv_str = self.socket.recv(BUFFER_SIZE).decode("utf-8") # first observation
      obv = json.loads(obv_str)
      while winner is None:
        move, turn = self.action(obv)
        move = self.clampAction(move, "movement")
        turn = self.clampAction(turn, "turn")
        action_msg = "{:.4f},{:.4f}".format(move, turn)
        
        self.socket.sendall(action_msg.encode("utf-8"))
        obv_str = self.socket.recv(BUFFER_SIZE).decode("utf-8") 
        obv = json.loads(obv_str)
        
        if "winner" in obv:
          winner = obv["winner"]
          break

    except Exception as e:
      raise e
    finally:
      self.socket.close()
    
    return winner

  def action(self, obv):
    raise NotImplementedError()

class SimpleTank(TankBase):
  def __init__(self, action_func, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.action = action_func
