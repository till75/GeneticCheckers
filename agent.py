class MinimaxAgent:
    def __init__(self, name, weights, depth=3):
        # weights = [w1: regular piece, w2: king piece, w3: center control, w4: defense]
        self.name = name
        self.weights = weights
        self.depth = depth

    def __str__(self):
        """Allows direct string representation when printing or formatting (e.g., f'{agent}')."""
        return self.name

    def evaluate(self, board, evaluating_player):
        """
        Evaluates board state based on piece weights and position.
        evaluating_player: 1 (Red) or 2 (Black)
        """
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board.grid[r][c]
                if piece == 0:
                    continue

                # Determine if piece belongs to evaluating player
                is_eval_player_piece = (piece > 0) if evaluating_player == 1 else (piece < 0)
                sign = 1 if is_eval_player_piece else -1

                # Magnitude check for King (2) vs Normal (1)
                is_king = (abs(piece) == 2)
                is_center = 2 <= c <= 5 and 2 <= r <= 5

                # Back-row defense check:
                # Red (Player 1) defends row 7; Black (Player 2) defends row 0
                is_back_row = (r == 7 and piece > 0) or (r == 0 and piece < 0)

                material = self.weights[1] if is_king else self.weights[0]
                center_bonus = self.weights[2] if is_center else 0
                defense_bonus = self.weights[3] if is_back_row else 0

                score += sign * (material + center_bonus + defense_bonus)
        return score

    def get_move(self, board):
        """Entry point for getting the best move using Minimax with Alpha-Beta."""
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        current_player = board.current_turn
        legal_moves = board.get_legal_moves(current_player)

        for move in legal_moves:
            next_board = board.clone()
            next_board.make_move(move)

            # Evaluate move via minimax recursion
            score = self.minimax(next_board, self.depth - 1, False, alpha, beta, current_player)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def minimax(self, board, depth, maximizing_player, alpha, beta, evaluating_player):
        """Recursive minimax search with Alpha-Beta pruning."""
        if depth == 0 or board.is_game_over():
            base_score = self.evaluate(board, evaluating_player)

            # Minor Ply/Depth Preference:
            # Calculate how deep we are from the root (self.depth - remaining depth).
            # Subtracting a tiny fraction per ply penalizes longer, stalling paths
            # and breaks flat-score ties, forcing the AI to make forward progress.
            ply_from_root = self.depth - depth
            return base_score - (ply_from_root * 0.001)

        current_player = board.current_turn
        legal_moves = board.get_legal_moves(current_player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                next_board = board.clone()
                next_board.make_move(move)
                eval_score = self.minimax(next_board, depth - 1, False, alpha, beta, evaluating_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                next_board = board.clone()
                next_board.make_move(move)
                eval_score = self.minimax(next_board, depth - 1, True, alpha, beta, evaluating_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval