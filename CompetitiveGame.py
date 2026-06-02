import random
import math

# -----------------------------
# Competitive Resource Allocation Game
# AI Mini Project using Python
# -----------------------------

TOTAL_TURNS = 5
INITIAL_RESOURCES = 20

# -----------------------------------
# Game State
# -----------------------------------
class GameState:
    def __init__(self, turn, p1_resources, p2_resources, p1_score, p2_score):
        self.turn = turn
        self.p1_resources = p1_resources
        self.p2_resources = p2_resources
        self.p1_score = p1_score
        self.p2_score = p2_score

    def is_terminal(self):
        return self.turn >= TOTAL_TURNS or \
               self.p1_resources <= 0 or \
               self.p2_resources <= 0

# -----------------------------------
# Utility Function
# -----------------------------------
def evaluate(state):
    return state.p1_score - state.p2_score

# -----------------------------------
# Valid Moves
# -----------------------------------
def get_possible_moves(resources):
    moves = []

    for i in range(1, min(6, resources + 1)):
        moves.append(i)

    return moves

# -----------------------------------
# Heuristic Function
# -----------------------------------
def heuristic(move):
    return move * random.uniform(0.8, 1.2)

# -----------------------------------
# Bayesian Prediction
# -----------------------------------
def predict_opponent_move(resources):

    possible = get_possible_moves(resources)

    probabilities = []

    total = 0

    for move in possible:
        prob = random.random()
        probabilities.append(prob)
        total += prob

    probabilities = [p / total for p in probabilities]

    predicted_move = random.choices(possible, probabilities)[0]

    return predicted_move

# -----------------------------------
# Minimax with Alpha-Beta Pruning
# -----------------------------------
def minimax(state, depth, alpha, beta, maximizing_player):

    if depth == 0 or state.is_terminal():
        return evaluate(state)

    if maximizing_player:

        max_eval = -math.inf

        moves = get_possible_moves(state.p1_resources)

        for move in moves:

            predicted_opponent = predict_opponent_move(state.p2_resources)

            new_state = GameState(
                state.turn + 1,
                state.p1_resources - move,
                state.p2_resources - predicted_opponent,
                state.p1_score + move,
                state.p2_score + predicted_opponent
            )

            eval = minimax(new_state, depth - 1, alpha, beta, False)

            max_eval = max(max_eval, eval)

            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval

    else:

        min_eval = math.inf

        moves = get_possible_moves(state.p2_resources)

        for move in moves:

            predicted_player = predict_opponent_move(state.p1_resources)

            new_state = GameState(
                state.turn + 1,
                state.p1_resources - predicted_player,
                state.p2_resources - move,
                state.p1_score + predicted_player,
                state.p2_score + move
            )

            eval = minimax(new_state, depth - 1, alpha, beta, True)

            min_eval = min(min_eval, eval)

            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval

# -----------------------------------
# AI Move Selection
# -----------------------------------
def best_move(state):

    best_score = -math.inf
    best_action = 1

    moves = get_possible_moves(state.p1_resources)

    for move in moves:

        predicted_opponent = predict_opponent_move(state.p2_resources)

        new_state = GameState(
            state.turn + 1,
            state.p1_resources - move,
            state.p2_resources - predicted_opponent,
            state.p1_score + move,
            state.p2_score + predicted_opponent
        )

        score = minimax(new_state, 3, -math.inf, math.inf, False)

        score += heuristic(move)

        if score > best_score:
            best_score = score
            best_action = move

    return best_action

# -----------------------------------
# CSP Constraint Checking
# -----------------------------------
def valid_move(move, resources):

    if move <= resources and move > 0:
        return True

    return False

# -----------------------------------
# Display Game State
# -----------------------------------
def display(state):

    print("\n---------------------------")
    print("Turn:", state.turn)
    print("---------------------------")

    print("Player 1 Resources:", state.p1_resources)
    print("Player 2 Resources:", state.p2_resources)

    print("Player 1 Score:", state.p1_score)
    print("Player 2 Score:", state.p2_score)

# -----------------------------------
# Main Game
# -----------------------------------
def play_game():

    state = GameState(
        0,
        INITIAL_RESOURCES,
        INITIAL_RESOURCES,
        0,
        0
    )

    print("======================================")
    print(" Competitive Resource Allocation Game ")
    print("======================================")

    while not state.is_terminal():

        display(state)

        # AI Agent 1
        p1_move = best_move(state)

        if not valid_move(p1_move, state.p1_resources):
            p1_move = 1

        # AI Agent 2
        p2_move = predict_opponent_move(state.p2_resources)

        if not valid_move(p2_move, state.p2_resources):
            p2_move = 1

        print("\nPlayer 1 chooses:", p1_move)
        print("Player 2 chooses:", p2_move)

        # Update State
        state = GameState(
            state.turn + 1,
            state.p1_resources - p1_move,
            state.p2_resources - p2_move,
            state.p1_score + p1_move,
            state.p2_score + p2_move
        )

    # Final Result
    print("\n================================")
    print(" Final Result ")
    print("================================")

    display(state)

    if state.p1_score > state.p2_score:
        print("\nWinner: Player 1 AI Agent")

    elif state.p2_score > state.p1_score:
        print("\nWinner: Player 2 AI Agent")

    else:
        print("\nGame Draw")

# -----------------------------------
# Run Program
# -----------------------------------
if __name__ == "__main__":
    play_game()