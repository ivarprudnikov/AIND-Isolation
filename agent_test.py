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

    def setup_game(self, p1, p2, width=7, height=7):
        self.p1 = p1
        self.p2 = p2
        self.game = isolation.Board(self.p1, self.p2, width, height)

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

    def test_minimax_calculates_optimal_move_with_bigger_board(self):
        """
             0   1   2   3   4   5   6   7   8
        0  |   |   |   |   |   |   |   |   |   |
        1  |   |   |   |   |   |   |   |   |   |
        2  |   |   |   |   |   |   | - |   |   |
        3  |   |   | - |   |   | - |   |   |   |
        4  |   |   | - | - | - | - |   |   |   |
        5  |   |   |   | - | 2 |   |   |   |   |
        6  |   |   |   | - | - | 1 |   |   |   |
        7  |   |   |   |   |   |   |   |   |   |
        8  |   |   |   |   |   |   |   |   |   |
        """
        self.setup_game(game_agent.MinimaxPlayer(), game_agent.MinimaxPlayer(), 9, 9)
        filling_moves = list()
        filling_moves.append((3, 2))
        filling_moves.append((4, 2))
        filling_moves.append((4, 3))
        filling_moves.append((5, 3))
        filling_moves.append((6, 3))
        filling_moves.append((4, 4))
        filling_moves.append((6, 4))
        filling_moves.append((3, 5))
        filling_moves.append((4, 5))
        filling_moves.append((2, 6))
        filling_moves.append((6, 5))  # player 1
        filling_moves.append((5, 4))  # player 2
        for m in filling_moves:
            self.game.apply_move(m)

        print(self.game.to_string())

        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        self.assertEqual(self.p1.minimax(self.game, 1), (4, 6))

    def test_alphabeta_optimal_move_with_depth_1_and_9x9_board(self):
        """
             0   1   2   3   4   5   6   7   8
        0  |   |   |   |   |   |   |   |   |   |
        1  |   |   |   |   |   |   |   |   |   |
        2  |   |   | - | - |   |   |   |   |   |
        3  |   |   |   |   | - | - | - |   |   |
        4  |   | 1 | - | - | - | - | - |   |   |
        5  |   |   | - |   | - | - |   |   |   |
        6  |   |   |   | - | - | 2 | - |   |   |
        7  |   |   |   |   |   |   |   |   |   |
        8  |   |   |   |   |   |   |   |   |   |
        """
        self.setup_game(game_agent.AlphaBetaPlayer(), game_agent.AlphaBetaPlayer(), 9, 9)
        filling_moves = ((2, 2), (4, 2), (5, 2), (2, 3), (4, 3), (6, 3), (3, 4), (4, 4), (5, 4),
                         (6, 4), (3, 5), (4, 5), (5, 5), (3, 6), (4, 6), (6, 6), (4, 1), (6, 5))
        for m in filling_moves:
            self.game.apply_move(m)

        print(self.game.to_string())

        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        self.assertEqual(self.p1.alphabeta(self.game, 1), (6, 2))

    def test_alphabeta_optimal_move_with_depth_1_and_9x9_board_2(self):
        """
             0   1   2   3   4   5   6   7   8
        0  |   |   |   |   |   |   |   |   |   |
        1  |   |   |   |   |   |   |   |   |   |
        2  |   |   |   | - |   |   |   |   |   |
        3  |   |   |   |   | - | - |   |   |   |
        4  |   |   |   | 2 | - | 1 | - |   |   |
        5  |   |   |   | - | - |   |   |   |   |
        6  |   |   |   | - |   |   |   |   |   |
        7  |   |   |   |   |   |   |   |   |   |
        8  |   |   |   |   |   |   |   |   |   |
        """
        self.setup_game(game_agent.AlphaBetaPlayer(), game_agent.AlphaBetaPlayer(), 9, 9)
        filling_moves = ((2, 3), (5, 3), (6, 3), (3, 4), (4, 4), (5, 4), (3, 5),
                         (4, 6), (4, 5), (4, 3))
        for m in filling_moves:
            self.game.apply_move(m)

        print(self.game.to_string())

        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        result = self.p1.alphabeta(self.game, 1)
        self.assertIn(result, ((2, 4), (6, 4)))

    def test_alphabeta_optimal_move_with_depth_2_and_9x9_board(self):
        """
             0   1   2   3   4   5   6   7   8
        0  |   |   |   |   |   |   |   |   |   |
        1  |   |   |   |   |   | - |   |   |   |
        2  |   |   |   | - | - | - |   |   |   |
        3  |   |   | - | - | - | - | 2 |   |   |
        4  |   |   | - | - |   |   | - |   |   |
        5  |   |   | - | - |   |   | - |   |   |
        6  |   |   |   | 1 | - | - |   |   |   |
        7  |   |   |   |   |   |   |   |   |   |
        8  |   |   |   |   |   |   |   |   |   |
        """
        self.setup_game(game_agent.AlphaBetaPlayer(), game_agent.AlphaBetaPlayer(), 9, 9)
        filling_moves = ((3, 2), (4, 2), (5, 2), (2, 3), (3, 3), (4, 3), (5, 3), (2, 4), (3, 4), (6, 4),
                         (1, 5), (2, 5), (3, 5), (6, 5), (4, 6), (5, 6), (6, 3), (3, 6))
        for m in filling_moves:
            self.game.apply_move(m)

        print(self.game.to_string())

        self.assertTrue(self.p1 == self.game.active_player)
        self.assertFalse(self.game.is_loser(self.p1))
        self.assertFalse(self.game.is_loser(self.p2))

        # (5, 5) or (7, 5)
        alpha = -10.
        beta = 10.
        result = self.p1.alphabeta(self.game, 2, alpha, beta)
        self.assertIn(result, ((5, 5), (7, 5)))


if __name__ == '__main__':
    unittest.main()