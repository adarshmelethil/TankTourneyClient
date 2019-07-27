
import socket
import json
import time

TCP_IP = "127.0.0.1"
PLAYER = 1
TCP_PORT = 26000 + PLAYER
BUFFER_SIZE = 1024
msg = [
  "1,0",
  "0.1,1",
  "0.1,-1",
  "0.7,0.3",
]

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((TCP_IP, TCP_PORT))
  
  for _ in range(1000):
    s.sendall(msg[0].encode("utf-8"))
    data = s.recv(BUFFER_SIZE).decode("utf-8")
    
  for i in range(len(msg)*10):
    s.sendall(msg[i//10].encode("utf-8"))
    data = s.recv(BUFFER_SIZE).decode("utf-8")
    print("Received:\n{}\n---".format(data))
    jsonData = json.loads(data)
    print("JSON: {}".format(jsonData))

    # time.sleep(1)

finally:
  s.close()

