#!/usr/bin/env python

import socket
import sys

BYTE_SIZE = 2048;

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = ("127.0.0.1", 27001)

import json

try:
  for i in range(10):
    sock.sendto(b'obv', addr)

    # Send data
    obv_data, server_addr = sock.recvfrom(BYTE_SIZE)

    obv = json.loads(obv_data)
    print("#{}: ({}): '{}'".format(i, server_addr, d))

except socket.timeout as sto:
  print("timeout:", sto)
finally:
  print('closing socket')
  sock.close()
