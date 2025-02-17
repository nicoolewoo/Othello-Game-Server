#!/usr/bin/python

import sys
import json
import socket
import random
#static board with weights assigned to each spot.
#based off this article I found (page 6): https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/miniproject1_vaishu_muthu/Paper/Final_Paper.pdf
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
#array storing all possible directions (left, right, diagonal, etc.)
directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)] 

def flip(sim_board, move, player):
  """
  Simulates flipping the appropiate pieces based on the inputted move. 
  """
  for nr, nc in directions:
    x, y = move[0] + nr, move[1] + nc
    flips = []
    while 0 <= x < len(sim_board) and 0 <= y < len(sim_board) and sim_board[x][y] not in {0, player}:
      flips.append((x, y))
      x += nr
      y += nc 
    if 0 <= x < len(sim_board) and 0 <= y < len(sim_board[0]) and sim_board[x][y] == player: 
      for fx, fy in flips:
        sim_board[fx][fy] = player
    sim_board[move[0]][move[1]] = player


def simulated_board(move, player, board):
  """
  Creates a copy of the current game state board and predicts the next game state based on the inputted move. 
  """
  sim_board = [row.copy() for row in board]
  sim_board[move[0]][move[1]] = player
  flip(sim_board, move, player)
  return sim_board

def if_valid_move(board, r, c):
  """
  Checks if the inputted move is valid based on the current game state. A move is valid if it flanks an opponent piece. 
  """
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

def get_all_moves(player, board):
  """
  Based on current game state returns an array of all valid moves.
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
      
def dfs(board, depth, MAX, player, a, b):
  """
  Finds the optimal move by doing an adjusted depth first search and maximizing the value of the predicted boards. Stops searching a branch when it finds a higher scoring subtree.
  """
  if depth == 0:
    return calculate_score(player, board), None 
  moves = get_all_moves(player, board)
  if not moves:
    return calculate_score(player, board), None
  high_score = float("-inf") if MAX else float ("-inf")
  turn = None 

  for move in moves:
    sim_board = simulated_board(move, player, board)
    curr_score, _ = dfs(sim_board, depth - 1, False, player, a, b)
    if MAX:
      if curr_score > high_score:
        high_score = curr_score
        turn = move 
      a = max(a, curr_score)
    else: #assumes opponent plays optimally
      if curr_score < high_score:
        high_score = curr_score
        turn = move 
      b = min(b, curr_score)
    if b <= a:
      break
  return high_score, turn 

def get_move(player, board):
  """
  Plays the optimal move based on the above dfs function, and if no optimal move plays a random valid move. 
  """
  _, move = dfs(board, 7, True, player, float('-inf'), float('inf')) #7 seems to be the max depth without performance issues
  if move:
    return move
  else:
    return random.choice(get_all_moves(player, board)) 
 
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
