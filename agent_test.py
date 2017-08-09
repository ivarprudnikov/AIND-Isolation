"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
from importlib import reload

import game_agent
import isolation

basic_player_1 = "Player1"
basic_player_2 = "Player2"


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setup_game(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.game = isolation.Board(self.p1, self.p2)

    def setUp(self):
        reload(game_agent)

    def test_player2_moves_after_player1(self):
        self.setup_game(basic_player_1, basic_player_2)
        self.game.apply_move((2, 3))
        self.assertTrue(self.p2 == self.game.active_player)

    def test_player1_loses_when_no_moves_available(self):
        """      0   1   2   3   4   5   6
            0  | - | - | - | - | - | - | - |
            1  | - | - | - | - | - | - | - |
            2  | - | - | - | - | - | - | 1 |
            3  | - | - | - | - | - | - | 2 |
            4  | - | - | - | - | - | - |   |
            5  | - | - | - | - | - | - |   |
            6  | - | - | - | - | - | - |   |
            """
        self.setup_game(basic_player_1, basic_player_2)
        # fill board with moves until player1 has nowhere to move
        filling_moves = [(i, j) for j in range(self.game.width) for i in range(self.game.height)]
        del filling_moves[-3:]
        for m in filling_moves:
            self.game.apply_move(m)
        self.assertTrue(self.p1 == self.game.active_player)
        self.assertTrue(self.game.is_loser(self.p1))
        self.assertTrue(self.game.is_winner(self.p2))

    def test_player2_loses_when_no_moves_available(self):
        """      0   1   2   3   4   5   6
            0  | - | - | - | - | - | - | - |
            1  | - | - | - | - | - | - | - |
            2  | - | - | - | - | - | - | - |
            3  | - | - | - | - | - | - | 2 |
            4  | - | - | - | - | - | - | 1 |
            5  | - | - | - | - | - | - |   |
            6  | - | - | - | - | - | - |   |
            """
        self.setup_game(basic_player_1, basic_player_2)
        # fill board with moves until player1 has nowhere to move
        filling_moves = [(i, j) for j in range(self.game.width) for i in range(self.game.height)]
        del filling_moves[-2:]
        for m in filling_moves:
            self.game.apply_move(m)
        self.assertTrue(self.p2 == self.game.active_player)
        self.assertTrue(self.game.is_loser(self.p2))
        self.assertTrue(self.game.is_winner(self.p1))

    def test_player_2_finds_minimax_move(self):
        """      0   1   2   3   4   5   6
            0  | - | - | - | - | - |   |   |
            1  | - | - | - | - | - | 2 |   |
            2  | - | - | - | - | - |   |   |
            3  | - | - | - | - | 1 |   |   |
            4  | - | - | - | - | - |   |   |
            5  | - | - | - | - | - |   |   |
            6  | - | - | - | - | - |   |   |
            """
        self.setup_game(game_agent.MinimaxPlayer(), game_agent.MinimaxPlayer())
        filling_moves = [(i, j) for j in range(4) for i in range(self.game.height)]
        filling_moves.append((0, 4))
        filling_moves.append((1, 4))
        filling_moves.append((2, 4))
        filling_moves.append((4, 4))
        filling_moves.append((5, 4))
        filling_moves.append((6, 4))
        for m in filling_moves:
            self.game.apply_move(m)

        self.game.apply_move((3, 4))
        self.game.apply_move((1, 5))

        print(self.game.to_string())
        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        result = self.p1.minimax(self.game, 100)

        # both rows are valid and have same minimax value
        self.assertTrue(result[0] == 2 or result[0] == 4)
        self.assertEqual(result[1], 6)


    def test_player_2_finds_minimax_move_limited_with_depth(self):
        """      0   1   2   3   4   5   6
            0  | - | - | - | - | - |   |   |
            1  | - | - | - | - | - | 2 |   |
            2  | - | - | - | - | - |   |   |
            3  | - | - | - | - | 1 |   |   |
            4  | - | - | - | - | - |   |   |
            5  | - | - | - | - | - |   |   |
            6  | - | - | - | - | - |   |   |
            """
        self.setup_game(game_agent.MinimaxPlayer(), game_agent.MinimaxPlayer())
        filling_moves = [(i, j) for j in range(4) for i in range(self.game.height)]
        filling_moves.append((0, 4))
        filling_moves.append((1, 4))
        filling_moves.append((2, 4))
        filling_moves.append((4, 4))
        filling_moves.append((5, 4))
        filling_moves.append((6, 4))
        for m in filling_moves:
            self.game.apply_move(m)

        self.game.apply_move((3, 4))
        self.game.apply_move((1, 5))

        print(self.game.to_string())
        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        result = self.p1.minimax(self.game, 100)

        # both rows are valid and have same minimax value
        self.assertTrue(result[0] == 2 or result[0] == 4)
        self.assertEqual(result[1], 6)


if __name__ == '__main__':
    unittest.main()