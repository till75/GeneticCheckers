import copy

class Move:
    def __init__(self, path, captures=None):
        self.path = path          # List of (row, col) tuples e.g., [(5, 2), (4, 3)]
        self.captures = captures if captures else [] # List of enemy pieces jumped


class Board:
    def __init__(self):
        # 0 = empty, 1 = Red Normal, 2 = Red King, -1 = Black Normal, -2 = Black King
        self.grid = self._initialize_board()
        self.current_turn = 1  # 1 for Red, 2 for Black

    def _initialize_board(self):
        grid = [[0 for _ in range(8)] for _ in range(8)]
        for r in range(3):
            for c in range(8):
                if (r + c) % 2 == 1:
                    grid[r][c] = -1  # Black normal pieces
        for r in range(5, 8):
            for c in range(8):
                if (r + c) % 2 == 1:
                    grid[r][c] = 1  # Red normal pieces
        return grid

    def clone(self):
        new_board = Board()
        new_board.grid = copy.deepcopy(self.grid)
        new_board.current_turn = self.current_turn
        return new_board

    def get_legal_moves(self, player):
        """Generates all legal step and jump moves for the given player."""
        legal_moves = []
        jumps = []

        # Directions: Red (1) moves "up" (row - 1), Black (2) moves "down" (row + 1)
        # Kings (abs == 2) can move in both directions.
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece == 0:
                    continue

                # Verify piece ownership (Positive = Player 1, Negative = Player 2)
                is_owner = (piece > 0) if player == 1 else (piece < 0)
                if not is_owner:
                    continue

                is_king = (abs(piece) == 2)

                # Determine allowed row directions
                directions = []
                if player == 1 or is_king:
                    directions.append(-1)  # Up
                if player == 2 or is_king:
                    directions.append(1)  # Down

                # Check diagonal moves
                for dr in directions:
                    for dc in [-1, 1]:
                        target_r, target_c = r + dr, c + dc
                        jump_r, jump_c = r + 2 * dr, c + 2 * dc

                        # 1. Check for single step moves
                        if 0 <= target_r < 8 and 0 <= target_c < 8:
                            if self.grid[target_r][target_c] == 0:
                                legal_moves.append(Move([(r, c), (target_r, target_c)]))

                        # 2. Check for jump moves (captures)
                        if 0 <= jump_r < 8 and 0 <= jump_c < 8:
                            middle_piece = self.grid[target_r][target_c]
                            # Is there an enemy piece in the middle and landing is empty?
                            if middle_piece != 0 and self.grid[jump_r][jump_c] == 0:
                                is_enemy = (middle_piece < 0) if player == 1 else (middle_piece > 0)
                                if is_enemy:
                                    jumps.append(Move([(r, c), (jump_r, jump_c)], captures=[(target_r, target_c)]))

        # Enforce mandatory jump rule: if jumps exist, only jumps are legal
        return jumps if jumps else legal_moves

    def make_move(self, move):
        """Applies a move path, handles captures, king promotion, and toggles turn."""
        start_r, start_c = move.path[0]
        end_r, end_c = move.path[-1]

        piece = self.grid[start_r][start_c]
        self.grid[start_r][start_c] = 0

        # Handle captures if any
        for cap_r, cap_c in move.captures:
            self.grid[cap_r][cap_c] = 0

        # Handle King Promotion
        # Red (1) reaches row 0 -> becomes Red King (2)
        # Black (-2) reaches row 7 -> becomes Black King (-2)
        if player_1_piece := (piece == 1 and end_r == 0):
            piece = 2
        elif player_2_piece := (piece == -1 and end_r == 7):
            piece = -2

        self.grid[end_r][end_c] = piece

        # Toggle turn
        self.current_turn = 2 if self.current_turn == 1 else 1

    def is_game_over(self):
        """Returns True if the current player has no pieces or no legal moves."""
        player_pieces = 0
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p != 0:
                    if (self.current_turn == 1 and p > 0) or (self.current_turn == 2 and p < 0):
                        player_pieces += 1

        if player_pieces == 0:
            return True

        # If they have pieces but zero legal moves, they are blocked/lose
        if not self.get_legal_moves(self.current_turn):
            return True

        return False

    def display(self):
        """Displays the board state using sign for player and magnitude for type."""
        RED_COLOR = "\033[91m"
        BLUE_COLOR = "\033[94m"
        RESET_COLOR = "\033[0m"

        print("    " + " ".join([str(c) for c in range(8)]))
        print("  +" + "---" * 8 + "-+")

        for r in range(8):
            row_str = f"{r} |"
            for c in range(8):
                piece = self.grid[r][c]
                if piece == 0:
                    row_str += " ."
                else:
                    # Magnitude determines piece type: 1 = Normal, 2 = King
                    symbol = "K" if abs(piece) == 2 else "O"

                    # Sign determines player: Positive = Red (Player 1), Negative = Black (Player 2)
                    if piece > 0:
                        row_str += f" {RED_COLOR}{symbol}{RESET_COLOR}"
                    else:
                        row_str += f" {BLUE_COLOR}{symbol}{RESET_COLOR}"

            row_str += " |"
            print(row_str)

        print("  +" + "---" * 8 + "-+")

    def print_legal_moves(self, player):
        """Prints a readable list of all legal moves available for the given player."""
        legal_moves = self.get_legal_moves(player)

        if not legal_moves:
            print(f"No legal moves available for Player {player}.")
            return

        # Check if mandatory jumps are active
        has_jumps = any(len(move.captures) > 0 for move in legal_moves)
        if has_jumps:
            print("--- MANDATORY JUMPS AVAILABLE ---")
        else:
            print("--- Legal Step Moves ---")

        for i, move in enumerate(legal_moves):
            path_str = " -> ".join([str(coord) for coord in move.path])
            if move.captures:
                print(f"  {i + 1}: [JUMP] {path_str} (captures enemy at {move.captures})")
            else:
                print(f"  {i + 1}: [STEP] {path_str}")