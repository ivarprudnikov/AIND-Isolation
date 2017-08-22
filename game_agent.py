"""TODO improve main heuristic"""

import math


SCORES = dict()


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    global SCORES

    # retrieve score from cache if any

    game_hash = game.hash()
    if game_hash in SCORES:
        return SCORES[game_hash]

    p1 = player
    p2 = game.get_opponent(player)

    # Calculates moves scores

    p1_legal_moves = game.get_legal_moves(p1)
    p2_legal_moves = game.get_legal_moves(p2)

    p1_moves_weight = 0.5
    p2_moves_weight = 0.4

    p1_moves_score = len(p1_legal_moves) * p1_moves_weight
    p2_moves_score = len(p2_legal_moves) * p2_moves_weight

    moves_score = p1_moves_score - p2_moves_score

    # Calculates centerness based on game progress

    game_progress = get_game_progress(game)
    centerness_score = 0

    if game_progress < 0.4:
        c_weight = centerness_weight(game)
        p1_centerness = centerness(game, p1)
        p2_centerness = centerness(game, p2)
        centerness_score = (p1_centerness - p2_centerness) * c_weight

    # Fancy attack score, does not affect results too much

    attack_score = 0.01 if game.get_player_location(p1) in game._Board__get_moves(game.get_player_location(p2)) else 0

    sum_of_p1_deeper_moves = nested_available_moves_impact(game, p1)
    sum_of_p2_deeper_moves = nested_available_moves_impact(game, p2)
    deeper_score = sum_of_p1_deeper_moves - sum_of_p2_deeper_moves
    val = centerness_score + moves_score + attack_score + deeper_score

    # store score

    SCORES[game_hash] = val

    return val


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_centerness = centerness(game, player)
    opp_centerness = centerness(game, game.get_opponent(player))

    return own_centerness * 2 - opp_centerness * 0.5


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    p1 = player
    p2 = game.get_opponent(player)
    pos_p1 = game.get_player_location(p1)
    pos_p2 = game.get_player_location(p2)
    return distance_between(pos_p1, pos_p2)


def nested_available_moves_impact(game, player):
    direct_moves = game.get_legal_moves(player)

    level_1_moves = set()
    for m in direct_moves:
        level_1_moves = level_1_moves.union(game._Board__get_moves(m))

    level_2_moves = set()
    for m in level_1_moves:
        level_2_moves = level_2_moves.union(game._Board__get_moves(m))

    return len(set().union(direct_moves, level_1_moves, level_2_moves))


def get_game_progress(game):
    moves = game.move_count
    size = game.width * game.height
    return moves / size


def centerness_weight(game):
    return 1 / game.move_count


def centerness(game, player):
    """
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        Distance from center score
    """
    current_location = game.get_player_location(player)

    center_row_idx = game.height/2-0.5
    center_col_idx = game.width/2-0.5
    center_location = (center_row_idx, center_col_idx)

    if current_location == center_location:
        return 1.

    distance_from_center = distance_between(center_location, current_location)

    return 1/distance_from_center


def distance_between(pos1, pos2):
    """
    Parameters
    ----------
    pos1 : float, float
        Position
    pos2 : float, float
        Position

    Returns
    -------
    float
        Distance between positions
    """
    if pos1 == pos2:
        return 0.

    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.alpha = None
        self.beta = None

    def terminal_test(self, game, depth=None):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        Returns
        -------
        bool
            Return True if the game is over for the active player
            and False otherwise.
        """
        if callable(self.time_left) and self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if (depth is not None) and (depth == 0):
            return True

        return not bool(game.get_legal_moves())

    def min_value(self, game, depth, alpha=None, beta=None):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search from this point
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            Return the value for a win (+100) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
        """

        v = float("inf")

        if callable(self.time_left) and self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game, depth):
            return self.score(game, self)

        for m in game.get_legal_moves():

            v = min(v, self.max_value(game.forecast_move(m), depth - 1, alpha, beta))

            # if maximum is already more than it can be then skip rest
            if (alpha is not None) and (v <= alpha):
                break

            # update upper bound
            if beta is not None:
                beta = min(beta, v)

        return v

    def max_value(self, game, depth, alpha=None, beta=None):
        """
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search from this point
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            Return the value for a loss (-1) if the game is over,
            otherwise return the maximum value over all legal child
            nodes.
        """

        v = float("-inf")

        if callable(self.time_left) and self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self.terminal_test(game, depth):
            return self.score(game, self)

        for m in game.get_legal_moves():

            v = max(v, self.min_value(game.forecast_move(m), depth - 1, alpha, beta))

            # if maximum is already more than it can be then skip rest
            if (beta is not None) and (v >= beta):
                break

            # update lower bound
            if alpha is not None:
                alpha = max(alpha, v)

        return v


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    # use min/max from super class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            moves = game.get_legal_moves()
            if len(moves) > 0:
                best_move = moves[0]  # whatever move to keep playing

        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        best_move = (-1, -1)
        score = float("-inf")
        moves = game.get_legal_moves(self)

        if callable(self.time_left) and self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth > 0 and len(game.get_legal_moves()) > 0:
            for m in moves:
                v = self.min_value(game.forecast_move(m), depth - 1)
                if v > score:
                    score = v
                    best_move = m

        if best_move == (-1, -1) and len(moves) > 0:
            best_move = moves[0]

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    # use min/max from super class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass

        moves = game.get_legal_moves(self)

        if best_move == (-1, -1) and len(moves) > 0:
            best_move = moves[0]

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        best_move = (-1, -1)

        if callable(self.time_left) and self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth > 0 and len(game.get_legal_moves()) > 0:
            v = float("-inf")
            for m in game.get_legal_moves():
                v = self.min_value(game.forecast_move(m), depth - 1, alpha, beta)

                # update lower bound
                if v > alpha:
                    self.alpha = alpha = v
                    best_move = m

                # if maximum is already more than it can be then skip rest
                if v >= beta:
                    break

            # update upper bound
            self.beta = beta = v

        return best_move
