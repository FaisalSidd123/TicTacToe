import time
from collections import defaultdict


class TicTacToe:
    """A strategic battle of X's and O's with unbeatable AI opponents"""

    def __init__(self):
        """Prepare a fresh 3x3 battlefield"""
        self.grid = [' '] * 9  # 3x3 game grid
        self.victor = None  # Tracks the winning player

    def display(self):
        """Render the current game state with borders"""
        print("\n" + "=" * 13)
        for row in [self.grid[i * 3:(i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")
            print("=" * 13)

    @staticmethod
    def show_reference():
        """Display position guide for players"""
        print("\nPosition Guide:")
        print("=" * 13)
        for i in range(3):
            print(f"| {i * 3} | {i * 3 + 1} | {i * 3 + 2} |")
            print("=" * 13)

    def free_spaces(self):
        """List all available move positions"""
        return [i for i, cell in enumerate(self.grid) if cell == ' ']

    def has_space(self):
        """Check if moves remain"""
        return ' ' in self.grid

    def count_free(self):
        """Number of remaining moves"""
        return self.grid.count(' ')

    def place_marker(self, pos, symbol):
        """Attempt to claim a position"""
        if self.grid[pos] == ' ':
            self.grid[pos] = symbol
            if self.check_win(pos, symbol):
                self.victor = symbol
            return True
        return False

    def check_win(self, pos, symbol):
        """Determine if last move won the game"""
        # Row check
        row = pos // 3
        if all(self.grid[row * 3 + col] == symbol for col in range(3)):
            return True

        # Column check
        col = pos % 3
        if all(self.grid[col + row * 3] == symbol for row in range(3)):
            return True

        # Diagonal checks (only for corner/center moves)
        if pos % 2 == 0:
            # Top-left to bottom-right
            if all(self.grid[i] == symbol for i in [0, 4, 8]):
                return True
            # Top-right to bottom-left
            if all(self.grid[i] == symbol for i in [2, 4, 6]):
                return True
        return False


def smart_move_finder(game_state, is_maximizing, player, memory=None):
    """Unbeatable AI using minimax with performance optimization"""
    memory = memory or {}

    # Check for cached results
    state_key = tuple(game_state.grid)
    if state_key in memory:
        return memory[state_key]

    opponent = 'O' if player == 'X' else 'X'

    # Game outcome scenarios
    if game_state.victor == player:
        return {'move': None, 'value': 1 * (game_state.count_free() + 1)}
    elif game_state.victor == opponent:
        return {'move': None, 'value': -1 * (game_state.count_free() + 1)}
    elif not game_state.has_space():
        return {'move': None, 'value': 0}

    if is_maximizing:
        best = {'move': None, 'value': -float('inf')}
        for move in game_state.free_spaces():
            game_state.place_marker(move, player)
            outcome = smart_move_finder(game_state, False, player, memory)

            # Revert move
            game_state.grid[move] = ' '
            game_state.victor = None

            outcome['move'] = move
            if outcome['value'] > best['value']:
                best = outcome
        memory[state_key] = best
        return best
    else:
        best = {'move': None, 'value': float('inf')}
        for move in game_state.free_spaces():
            game_state.place_marker(move, opponent)
            outcome = smart_move_finder(game_state, True, player, memory)

            # Revert move
            game_state.grid[move] = ' '
            game_state.victor = None

            outcome['move'] = move
            if outcome['value'] < best['value']:
                best = outcome
        memory[state_key] = best
        return best


def optimized_move_finder(game_state, is_maximizing, player, alpha=-float('inf'), beta=float('inf'), memory=None):
    """Enhanced AI using alpha-beta pruning for faster decisions"""
    memory = memory or {}

    state_key = tuple(game_state.grid)
    if state_key in memory:
        return memory[state_key]

    opponent = 'O' if player == 'X' else 'X'

    # Terminal state evaluation
    if game_state.victor == player:
        return {'move': None, 'value': 1 * (game_state.count_free() + 1)}
    elif game_state.victor == opponent:
        return {'move': None, 'value': -1 * (game_state.count_free() + 1)}
    elif not game_state.has_space():
        return {'move': None, 'value': 0}

    if is_maximizing:
        best = {'move': None, 'value': -float('inf')}
        for move in game_state.free_spaces():
            game_state.place_marker(move, player)
            outcome = optimized_move_finder(game_state, False, player, alpha, beta, memory)

            # Undo move
            game_state.grid[move] = ' '
            game_state.victor = None

            outcome['move'] = move
            if outcome['value'] > best['value']:
                best = outcome

            alpha = max(alpha, best['value'])
            if beta <= alpha:
                break
        memory[state_key] = best
        return best
    else:
        best = {'move': None, 'value': float('inf')}
        for move in game_state.free_spaces():
            game_state.place_marker(move, opponent)
            outcome = optimized_move_finder(game_state, True, player, alpha, beta, memory)

            # Undo move
            game_state.grid[move] = ' '
            game_state.victor = None

            outcome['move'] = move
            if outcome['value'] < best['value']:
                best = outcome

            beta = min(beta, best['value'])
            if beta <= alpha:
                break
        memory[state_key] = best
        return best


def benchmark_ai():
    """Compare the performance of both AI algorithms"""
    test_game = TicTacToe()

    # Warm-up runs
    smart_move_finder(test_game, True, 'X')
    optimized_move_finder(test_game, True, 'X')

    # Minimax benchmark
    start = time.perf_counter()
    for _ in range(10):
        smart_move_finder(test_game, True, 'X')
    classic_time = time.perf_counter() - start

    # Alpha-beta benchmark
    start = time.perf_counter()
    for _ in range(10):
        optimized_move_finder(test_game, True, 'X')
    optimized_time = time.perf_counter() - start

    print("\n⚡ AI Performance Report ⚡")
    print("-" * 30)
    print(f"Classic Minimax: {classic_time / 10:.6f}s per decision")
    print(f"Optimized AB:    {optimized_time / 10:.6f}s per decision")
    print(f"Performance gain: {((classic_time - optimized_time) / classic_time) * 100:.1f}% faster")


def run_game(game, x_strategy, o_strategy, show_moves=True):
    """Orchestrate the game between two players"""
    if show_moves:
        game.show_reference()

    current_player = 'X'
    while game.has_space():
        if current_player == 'O':
            position = o_strategy(game, current_player)
        else:
            position = x_strategy(game, current_player)

        if game.place_marker(position, current_player):
            if show_moves:
                print(f"\n{current_player} claims position {position}")
                game.display()

            if game.victor:
                if show_moves:
                    print(f"\n🌟 {current_player} triumphs! 🌟")
                return current_player

            current_player = 'O' if current_player == 'X' else 'X'
        time.sleep(0.3)

    if show_moves:
        print("\n⚔️ The battle tied ⚔️")
    return None


def human_strategy(game, symbol):
    """Process human player's moves"""
    while True:
        try:
            move = int(input(f"{symbol}, choose your position (0-8): "))
            if move in game.free_spaces():
                return move
            print("Position already taken. Try again.")
        except ValueError:
            print("Please enter a number between 0-8.")


def minimax_strategy(game, symbol):
    """AI using classic minimax approach"""
    time.sleep(0.6)  # More natural delay
    return smart_move_finder(game, True, symbol)['move']


def alphabeta_strategy(game, symbol):
    """AI using optimized alpha-beta pruning"""
    time.sleep(0.6)  # More natural delay
    return optimized_move_finder(game, True, symbol)['move']


def launch_game():
    """Game interface and mode selection"""
    print("\n" + "=" * 30)
    print(" TIC-TAC-TOE: ULTIMATE EDITION ")
    print("=" * 30)
    print("\n1. Challenge Minimax AI")
    print("2. Face Alpha-Beta AI")
    print("3. Benchmark AI Performance")
    print("4. Witness AI Clash")
    print("5. Exit to Desktop")

    while True:
        selection = input("\nSelect an option (1-5): ").strip()

        if selection == '5':
            print("\nThanks for playing! Until next time.")
            break

        arena = TicTacToe()

        if selection == '1':
            print("\n🔥 Human (X) vs Minimax AI (O) 🔥")
            run_game(arena, human_strategy, minimax_strategy)
        elif selection == '2':
            print("\n💻 Human (X) vs Optimized AI (O) 💻")
            run_game(arena, human_strategy, alphabeta_strategy)
        elif selection == '3':
            benchmark_ai()
        elif selection == '4':
            print("\n🤖 AI Showdown: Minimax vs Alpha-Beta 🤖")
            run_game(arena, minimax_strategy, alphabeta_strategy)
        else:
            print("Please select a valid option (1-5)")


if __name__ == "__main__":
    launch_game()