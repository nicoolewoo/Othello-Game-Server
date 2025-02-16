#!/usr/bin/python

import sys
import json
import socket
import random

board_weights = [
  [4, -3, 2, 2, 2, 2, -3, 4],
  [-3, -4, -1, -1, -1, -1, -4, -3],
  [2, -1, 1, 0, 0, 1, -1, 2],
  [2, -1, 0, 1, 1, 0, -1, 2],
  [2, -1, 0, 1, 1, 0, -1, 2],
  [2, -1, 1, 0, 0, 1, -1, 2],
  [-3, -4, -1, -1, -1, -1, -4, -3],
  [4, -3, 2, 2, 2, 2, -3, 4]
]
directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)] 

def simulated_board(move, player, board):
  sim_board = [row[:] for row in board]
  sim_board[move[0]][move[1]] = 1
  # flip_pieces = 
  return sim_board

def if_valid_move(board, r, c):
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
  """
  Based on current game state returns an array of all valid moves.

  Parameters:
  Returns:
    tuple array 
  """
  moves = []
  for r in range(len(board)):
    for c in range(len(board[0])):
      if board[r][c] == 0 and if_valid_move(board, r, c):
        moves.append([r, c])
  return moves

def calculate_score(player, board):
  """
  Calculates the current score for the player based on the sum of the static weights and subtracts by the opponents score. 
  """
  player1_score = 0 
  player2_score = 0
  for r in range(len(board)):
    for c in range(len(board[0])):
      if board[r][c] == 1:
        player1_score += board_weights[r][c]
      elif board[r][c] == 2:
        player2_score += board_weights[r][c]
  return player1_score - player2_score
      
#should return score, move
def dfs(board, depth, max, player):
  if depth == 0:
    return calculate_score(player, board), None #if we reach depth limit return the board's score
  moves = get_all_moves(player, board)
  if not moves: #if no moves, return current score
    return calculate_score(player, board), None
  turn = None #tracks optimal move

  if max: #find highest score 
    max_score = float('-inf')
    for move in moves:
      sim_board = simulated_board(move, player, board)
      curr_score, _ = dfs(sim_board, depth - 1, False, player)
      if curr_score > max_score:
        max_score = curr_score
        turn = move 
    return max_score, turn 
  else: #assumes opponent plays optimally
    min_score = float('inf') #the UI had 64 squares i think 
    for move in moves:
      sim_board = simulated_board(move, player, board)
      curr_score, _ = dfs(sim_board, depth - 1, True, player)
      if curr_score < min_score:
        min_score = curr_score
        turn = move 
    return min_score, turn 

#this output feeds into prepare response 
def get_move(player, board):
  _, move = dfs(board, 3, True, player) #this also slow 
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
