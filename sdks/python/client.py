#!/usr/bin/python

import sys
import json
import socket
import random

def if_valid_move(board, r, c):
  directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)] 
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
        break 
      x += nr
      y += nc 
  return False 

def get_all_moves(player, board): #this bouta be slow af maybe optimize later 
  moves = []
  for r in range(len(board)):
    for c in range(len(board[0])):
      if board[r][c] == 0 and if_valid_move(board, r, c):
        moves.append([r, c])
  return moves

def calculate_score(player, board):
  score = 0 
  for row in board:
    score += row.count(player)
  return score 
      
#should return score, move
def dfs(board, depth, max, player):
  if depth == 0:
    return calculate_score(player, board), None #if we reach depth limit return the board's score
  moves = get_all_moves(player, board)
  if not moves: #if no moves, return current score
    return calculate_score(player, board), None
  turn = None #tracks optimal move

  if max: #find highest score 
    max_score = 0
    for move in moves:
      curr_score, _ = dfs(board, depth - 1, False, player)
      if curr_score > max_score:
        max_score = curr_score
        turn = move 
    return max_score, turn 
  else: #assumes opponent plays optimally
    min_score = 65 #the UI had 64 squares i think 
    for move in moves:
      curr_score, _ = dfs(board, depth - 1, True, player)
      if curr_score < min_score:
        min_score = curr_score
        turn = move 
    return min_score, turn 

#this output feeds into prepare response 
def get_move(player, board):
  _, move = dfs(board, 6, True, player)
  if move:
    return move
  else:
    return random.choice(get_all_moves(player, board)) #in case fails might not need gotta check later
 
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
