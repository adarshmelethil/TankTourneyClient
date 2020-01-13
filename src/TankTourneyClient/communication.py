import sys
import json
import socket

def clampValue(val, min_val=-1, max_val=1):
  return min(max_val, max(min_val, val))

class ControllerPart:

  def __init__(self, player_num, control_port=26000, game_addr="127.0.0.1"):
    self.ctrl_addr = (game_addr, control_port+player_num)
    self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def update(self, fwd, turn, fire):
    assert isinstance(fwd, float)
    assert isinstance(turn, float)
    assert isinstance(fire, float)

    data = json.dumps({
      "fwd": clampValue(fwd),
      "turn": clampValue(turn),
      "fire": clampValue(fire, min_val=0),
    })
    # print(f"Sending: {data}", file=sys.stderr)
    # print(f"Data: {data}")
    self.ctrl_socket.sendto(bytearray(data, 'utf8'), self.ctrl_addr)


class ObservationPart:
  '''
    Listen to the game observation
  '''
  def __init__(self, player_num, obv_port=27000, recv_buff=2048, local_port="0.0.0.0"):
    self.UDP_IP = local_port
    self.UDP_PORT = obv_port + player_num
    self.RECV_BUFF = recv_buff

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind((self.UDP_IP, self.UDP_PORT))
    self.observation_data = {}
    self.on = True

  def observationDictToList(self):
    # (F)lag, (L)idar, (D)istance(T)ravelled, (A)ngle(T)urned, (P)aused
    data_keys = ["F", "L", "DT", "AT", "P"]
    return [self.observation_data.get(k) for k in data_keys]
  
  def debugObvDictToList(self):
    debug_keys = ["Pos", "Edges", "Obs"]
    return [self.observation_data.get(k) for k in debug_keys]

  def update(self):
    # print(self.observation_data.keys())
    return self.observationDictToList() + self.debugObvDictToList()

  def threadLoop(self):
    print(f"Listening... {self.UDP_IP}:{self.UDP_PORT}")
    while self.on:
      data, addr = self.sock.recvfrom(self.RECV_BUFF)
      # print(data)
      self.observation_data = json.loads(data)

  def shutdown(self):
    self.on = False


