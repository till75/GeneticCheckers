class MinimaxAgent:

    def __init__(self, name, weights, depth=3):
        self.name = name
        # Weights: [regular_value, king_value, center_bonus, back_row_bonus, edge_bonus, endgame_proximity_bonus]
        self.weights = weights
        self.depth = depth

    def __str__(self):
        """Allows direct string representation when printing or formatting (e.g., f'{agent}')."""
        return self.name

    def evaluate(self, board, player_color):
        score = 0.0
        red_pieces_coords = []
        blue_pieces_coords = []

        for r in range(8):
            for c in range(8):
                piece = board.grid[r][c]
                if piece == 0:
                    continue

                if piece > 0:
                    red_pieces_coords.append((r, c, abs(piece) == 2))
                else:
                    blue_pieces_coords.append((r, c, abs(piece) == 2))

                is_king = abs(piece) == 2

                # Material value
                piece_val = self.weights[1] if is_king else self.weights[0]

                # Center control bonus (columns 2-5, rows 2-5)
                center_bonus = self.weights[2] if (2 <= c <= 5 and 2 <= r <= 5) else 0.0

                # Back-row defense bonus (Red on row 7, Blue on row 0)
                back_row_bonus = self.weights[3] if ((piece > 0 and r == 7) or (piece < 0 and r == 0)) else 0.0

                # Edge / Border occupation bonus (Columns 0 and 7)
                edge_bonus = self.weights[4] if (c == 0 or c == 7) else 0.0

                total_piece_score = piece_val + center_bonus + back_row_bonus + edge_bonus

                if (piece > 0 and player_color == 1) or (piece < 0 and player_color == -1):
                    score += total_piece_score
                else:
                    score -= total_piece_score

        # ENDGAME PROXIMITY HUNTING: Triggered when total pieces <= 6
        total_pieces = len(red_pieces_coords) + len(blue_pieces_coords)
        if total_pieces <= 6 and len(self.weights) > 5:
            proximity_weight = self.weights[5]

            # Calculate distance gradient between opposing pieces
            red_score_modifier = 0.0
            blue_score_modifier = 0.0

            if red_pieces_coords and blue_pieces_coords:
                # For each Red piece, find minimum Manhattan distance to any Blue piece
                min_red_dist = float('inf')
                for rr, rc, _ in red_pieces_coords:
                    for br, bc, _ in blue_pieces_coords:
                        dist = abs(rr - br) + abs(rc - bc)
                        if dist < min_red_dist:
                            min_red_dist = dist
                # Closer distance = higher reward (invert distance)
                red_score_modifier = (14.0 - min_red_dist) * proximity_weight

                # For each Blue piece, find minimum distance to any Red piece
                min_blue_dist = float('inf')
                for br, bc, _ in blue_pieces_coords:
                    for rr, rc, _ in red_pieces_coords:
                        dist = abs(br - rr) + abs(bc - rc)
                        if dist < min_blue_dist:
                            min_blue_dist = dist
                blue_score_modifier = (14.0 - min_blue_dist) * proximity_weight

            if player_color == 1:
                score += (red_score_modifier - blue_score_modifier)
            else:
                score += (blue_score_modifier - red_score_modifier)

        return score

    def get_move(self, board):
        """Adaptive depth: Increase search depth if the board is sparse (endgame)."""
        total_pieces = 0
        for r in range(8):
            for c in range(8):
                if board.grid[r][c] != 0:
                    total_pieces += 1

        # If 6 or fewer pieces remain, boost depth to 5 for precise tactical vision
        current_depth = 5 if total_pieces <= 6 else self.depth

        # Run minimax search at the adjusted depth
        best_move = None
        best_score = float('-inf') if board.current_turn == 1 else float('inf')

        legal_moves = board.get_legal_moves(board.current_turn)
        if not legal_moves:
            return None

        for move in legal_moves:
            board_copy = board.clone()
            board_copy.make_move(move)

            # Evaluate using minimax
            score = self.minimax(board_copy, current_depth - 1, False, float('-inf'), float('inf'), board.current_turn)

            if board.current_turn == 1:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

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