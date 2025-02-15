#!/usr/bin/python

import sys
import json
import socket
import random

def if_valid(player, board, r, c):
  directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)] #might b able to optimize here later 
  for nr, nc in directions:
    x = nr + r
    y = nc + c 
    opp_piece = False 
    while 0 <= x < len(board) and 0 <= y < len(board[0]):
      if board[x][y] == 2:
        opp_piece = True
      elif board[x][y] == 1:
        if opp_piece:
          return True 
        break
      else:
        print("out of bounds or something else")
        break 
      x += nr
      y += nc 

  return False 
      



#this output feeds into prepare response 
def get_move(player, board):
  # TODO determine valid moves
  # TODO determine best move
  options = []
  row, col = len(board), len(board[0])
  for r in range(row):
    for c in range(col):
      if board[r][c] == 0 and if_valid(player, board, r, c):
        options.append([r, c])
  if not options:
    print("no move")
    return None 
  move = random.choice(options)
  print(f"player {player} move")
  return move

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      if move is None:
        print("No valid moves")
        continue 

      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
