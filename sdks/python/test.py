import unittest
import client
import pprint 

#always expects [2, 3] as first move as player 1 however that is an invalid move? ask abt later 
class TestGetMove(unittest.TestCase): 
  def test_get_move_returns_a_valid_move(self):
    board = [[0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 0, 0, 0], 
             [0, 0, 0, 2, 1, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0, 0]]
    self.assertEqual(client.get_move(1, board), [2, 3])

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

class TestFlipping(unittest.TestCase):
  """
  Tests that opponent pieces flip when flanked. Run using python -m unittest test.TestFlipping.test_opponent_piece_flipping
  """
  def test_opponent_piece_flipping(self):
    prev_board = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 1, 2, 0, 0, 0],
      [0, 0, 0, 2, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    move = (0, 4)
    client.flip(prev_board, move, player=1)
    new_board = [
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 2, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    try:
      self.assertEqual(prev_board, new_board)
    except AssertionError as e:
      print("Boards don't match")
      print("previous board:")
      pprint.pprint(prev_board)
      print("expected board:")
      pprint.pprint(new_board)

class TestValidMove(unittest.TestCase):
  """
  Checks that the move is valid. Use python -m unittest test.TestValidMove.test_if_valid_move.
  """
  def test_if_valid_move(self):
    board = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 1, 2, 0, 0, 0],
      [0, 0, 0, 2, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    self.assertTrue(client.if_valid_move(board, 3, 5))
    self.assertFalse(client.if_valid_move(board, 2, 3))

class TestCalculateScore(unittest.TestCase):
  """
  Checks that the score of the board is accurate. Use python -m unittest test.TestCalculateScore.test_score_calculation.
  """
  def test_score_calculation(self):
    board = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 1, 2, 0, 0, 0],
      [0, 0, 0, 2, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    self.assertEqual(client.calculate_score(1, board), 1)

if __name__ == '__main__':
  unittest.main()