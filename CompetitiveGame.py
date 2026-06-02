import random
import math

# =====================================
# Competitive Resource Allocation Game
# Player vs AI
# =====================================

TOTAL_TURNS = 5
INITIAL_RESOURCES = 20

# Store player's previous moves
player_history = []

# =====================================
# Game State
# =====================================
class GameState:

    def __init__(self, turn,
                 player_resources,
                 ai_resources,
                 player_score,
                 ai_score):

        self.turn = turn
        self.player_resources = player_resources
        self.ai_resources = ai_resources
        self.player_score = player_score
        self.ai_score = ai_score

    def is_terminal(self):

        return (
            self.turn >= TOTAL_TURNS
            or self.player_resources <= 0
            or self.ai_resources <= 0
        )


# =====================================
# Utility Function
# CO4
# =====================================
def evaluate(state):

    return state.ai_score - state.player_score


# =====================================
# Possible Moves
# =====================================
def get_possible_moves(resources):

    moves = []

    for i in range(1, min(6, resources + 1)):
        moves.append(i)

    return moves


# =====================================
# Greedy Search
# CO2
# =====================================
def greedy_prediction(resources):

    moves = get_possible_moves(resources)

    return max(moves)


# =====================================
# Heuristic Function
# CO4
# =====================================
def heuristic(move):

    return move * random.uniform(0.8, 1.2)


# =====================================
# Bayesian Prediction
# CO5
# =====================================
def bayesian_prediction(resources):

    possible_moves = get_possible_moves(resources)

    if len(player_history) == 0:
        return random.choice(possible_moves)

    most_common = max(
        set(player_history),
        key=player_history.count
    )

    if most_common in possible_moves:
        return most_common

    return random.choice(possible_moves)


# =====================================
# CSP Constraint Check
# CO3
# =====================================
def valid_move(move, resources):

    return 1 <= move <= min(5, resources)


# =====================================
# Minimax with Alpha-Beta
# CO4
# =====================================
def minimax(state,
            depth,
            alpha,
            beta,
            maximizing_player):

    if depth == 0 or state.is_terminal():
        return evaluate(state)

    # AI Turn
    if maximizing_player:

        max_eval = -math.inf

        moves = get_possible_moves(
            state.ai_resources
        )

        for move in moves:

            predicted_player = bayesian_prediction(
                state.player_resources
            )

            new_state = GameState(
                state.turn + 1,
                state.player_resources - predicted_player,
                state.ai_resources - move,
                state.player_score + predicted_player,
                state.ai_score + move
            )

            score = minimax(
                new_state,
                depth - 1,
                alpha,
                beta,
                False
            )

            max_eval = max(max_eval, score)

            alpha = max(alpha, score)

            if beta <= alpha:
                break

        return max_eval

    # Human Turn
    else:

        min_eval = math.inf

        moves = get_possible_moves(
            state.player_resources
        )

        for move in moves:

            predicted_ai = greedy_prediction(
                state.ai_resources
            )

            new_state = GameState(
                state.turn + 1,
                state.player_resources - move,
                state.ai_resources - predicted_ai,
                state.player_score + move,
                state.ai_score + predicted_ai
            )

            score = minimax(
                new_state,
                depth - 1,
                alpha,
                beta,
                True
            )

            min_eval = min(min_eval, score)

            beta = min(beta, score)

            if beta <= alpha:
                break

        return min_eval


# =====================================
# AI Best Move
# Hybrid AI
# CO6
# =====================================
def best_move(state):

    best_score = -math.inf
    best_action = 1

    moves = get_possible_moves(
        state.ai_resources
    )

    for move in moves:

        predicted_player = bayesian_prediction(
            state.player_resources
        )

        new_state = GameState(
            state.turn + 1,
            state.player_resources - predicted_player,
            state.ai_resources - move,
            state.player_score + predicted_player,
            state.ai_score + move
        )

        score = minimax(
            new_state,
            3,
            -math.inf,
            math.inf,
            False
        )

        score += heuristic(move)

        if score > best_score:

            best_score = score
            best_action = move

    return best_action


# =====================================
# Display State
# =====================================
def display(state):

    print("\n================================")
    print("Turn :", state.turn)
    print("================================")

    print("Your Resources :", state.player_resources)
    print("AI Resources   :", state.ai_resources)

    print("Your Score     :", state.player_score)
    print("AI Score       :", state.ai_score)


# =====================================
# Main Game
# =====================================
def play_game():

    state = GameState(
        0,
        INITIAL_RESOURCES,
        INITIAL_RESOURCES,
        0,
        0
    )

    print("========================================")
    print(" COMPETITIVE RESOURCE ALLOCATION GAME ")
    print("            PLAYER VS AI")
    print("========================================")

    while not state.is_terminal():

        display(state)

        while True:

            try:

                move = int(
                    input(
                        "\nAllocate resources (1-5): "
                    )
                )

                if valid_move(
                        move,
                        state.player_resources):

                    player_move = move
                    break

                else:
                    print("Invalid Move!")

            except ValueError:
                print("Enter Numbers Only!")

        # Store move history
        player_history.append(player_move)

        # AI Move
        ai_move = best_move(state)

        print("\nYou Allocated :", player_move)
        print("AI Allocated  :", ai_move)

        # Update State
        state = GameState(
            state.turn + 1,
            state.player_resources - player_move,
            state.ai_resources - ai_move,
            state.player_score + player_move,
            state.ai_score + ai_move
        )

    # Final Result
    print("\n================================")
    print("FINAL RESULT")
    print("================================")

    display(state)

    if state.player_score > state.ai_score:

        print("\nYOU WIN!")

    elif state.ai_score > state.player_score:

        print("\nAI WINS!")

    else:

        print("\nGAME DRAW")


# =====================================
# Run Program
# =====================================
if __name__ == "__main__":
    play_game()