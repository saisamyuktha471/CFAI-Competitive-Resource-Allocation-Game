import random
import math

TOTAL_TURNS = 5
START_RESOURCES = 20

class GameState:
    def __init__(self, turn, p1_res, p2_res, p1_score, p2_score):
        self.turn = turn
        self.p1_res = p1_res
        self.p2_res = p2_res
        self.p1_score = p1_score
        self.p2_score = p2_score

    def game_over(self):
        return (
            self.turn >= TOTAL_TURNS or
            self.p1_res <= 0 or
            self.p2_res <= 0
        )

def evaluate(state):
    return state.p1_score - state.p2_score

def get_moves(resources):
    return list(range(1, min(6, resources + 1)))

def predict_move(resources):
    moves = get_moves(resources)

    probs = [random.random() for _ in moves]
    total = sum(probs)

    probs = [p / total for p in probs]

    return random.choices(moves, probs)[0]


def heuristic(move):
    return move * random.uniform(0.8, 1.2)

def minimax(state, depth, alpha, beta, maximize):

    if depth == 0 or state.game_over():
        return evaluate(state)

    if maximize:
        best = -math.inf

        for move in get_moves(state.p1_res):

            opp = predict_move(state.p2_res)

            new_state = GameState(
                state.turn + 1,
                state.p1_res - move,
                state.p2_res - opp,
                state.p1_score + move,
                state.p2_score + opp
            )

            score = minimax(new_state, depth - 1, alpha, beta, False)

            best = max(best, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                break

        return best

    else:
        best = math.inf

        for move in get_moves(state.p2_res):

            player = predict_move(state.p1_res)

            new_state = GameState(
                state.turn + 1,
                state.p1_res - player,
                state.p2_res - move,
                state.p1_score + player,
                state.p2_score + move
            )

            score = minimax(new_state, depth - 1, alpha, beta, True)

            best = min(best, score)
            beta = min(beta, score)

            if beta <= alpha:
                break

        return best

def best_move(state):

    best_score = -math.inf
    chosen_move = 1

    for move in get_moves(state.p1_res):

        opp = predict_move(state.p2_res)

        next_state = GameState(
            state.turn + 1,
            state.p1_res - move,
            state.p2_res - opp,
            state.p1_score + move,
            state.p2_score + opp
        )

        score = minimax(next_state, 3, -math.inf, math.inf, False)
        score += heuristic(move)

        if score > best_score:
            best_score = score
            chosen_move = move

    return chosen_move

def valid_move(move, resources):
    return 0 < move <= resources

def show_state(state):
    print("\nTurn:", state.turn)
    print("Player 1 Resources:", state.p1_res)
    print("Player 2 Resources:", state.p2_res)
    print("Player 1 Score:", state.p1_score)
    print("Player 2 Score:", state.p2_score)

def play_game():

    state = GameState(
        0,
        START_RESOURCES,
        START_RESOURCES,
        0,
        0
    )

    print("Competitive Resource Allocation Game")

    while not state.game_over():

        show_state(state)

        p1_move = best_move(state)
        p2_move = predict_move(state.p2_res)

        if not valid_move(p1_move, state.p1_res):
            p1_move = 1

        if not valid_move(p2_move, state.p2_res):
            p2_move = 1

        print("\nPlayer 1 selected:", p1_move)
        print("Player 2 selected:", p2_move)

        state = GameState(
            state.turn + 1,
            state.p1_res - p1_move,
            state.p2_res - p2_move,
            state.p1_score + p1_move,
            state.p2_score + p2_move
        )

    print("\nFinal Scores")
    show_state(state)

    if state.p1_score > state.p2_score:
        print("\nWinner: Player 1")
    elif state.p2_score > state.p1_score:
        print("\nWinner: Player 2")
    else:
        print("\nMatch Draw")

if __name__ == "__main__":
    play_game()