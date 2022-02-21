# Author: Raymond Zhang
# Date: 8/4/2021
# Description: Implement Quoridor game class

class Pawn:
    """
    Represents a pawn for specific player
    """

    def __init__(self, player, coord):
        """Initializes pawn at location"""
        self._player = player
        self._coord = coord  #Coordinates should be a tuple

    def get_player(self):
        """Returns player"""
        return self._player

    def get_coord(self):
        """Returns pawn current coordinates"""
        return self._coord

    def set_coord(self, coord):
        """Sets pawn current coordinates"""
        self._coord = coord  # Coordinates should be a tuple


class QuoridorGame:
    """
    Represents a instance of Quoridor game
    """

    def __init__(self):
        """Initialize instance of Quoridor game"""

        # Initialize player resources
        # Player 1 is [0] and Player 2 is [1]
        self._turn = 1
        self._pawns = [Pawn(1, (4, 0)), Pawn(2, (4, 8))]
        self._fences = [10, 10]
        self._placed_fences = {
            "v": [],
            "h": []
        }
        self._winner = None

        # Add borders as fences
        for num in range(0, 9):
            self._placed_fences["v"].append((0, num))
            self._placed_fences["h"].append((num, 0))
            self._placed_fences["v"].append((9, num))
            self._placed_fences["h"].append((num, 9))

    def get_pawns(self):
        """Return pawns list"""
        return self._pawns

    def check_winner(self):
        """Checks for a winner and updates value"""
        pawns = self.get_pawns()

        # Check Player 1 victory
        if pawns[0].get_coord()[1] == 8:
            self._winner = 1

        # Check Player 2 victory
        if pawns[1].get_coord()[1] == 0:
            self._winner = 2

    def is_winner(self, player):
        """Returns whether player is winner"""
        if player == self._winner:
            return True
        else:
            return False

    def is_turn(self, player):
        """Check if this player's turn"""
        if player == self._turn:
            # Player 1's turn
            return True
        else:
            if player == 2 and self._turn != 1:
                # Player 2's turn
                return True
            else:
                # Not player's turn
                return False

    def update_turn(self):
        """Update to the other player's turn"""
        self._turn *= -1

    def get_placed_fences(self):
        """Return placed fences dictionary"""
        return self._placed_fences

    def check_valid_action(self, player, coord):
        """Performs basic checks on player turn and coord in board"""

        if not self.is_turn(player):
            # Not the player's turn
            return False

        if (coord[0] or coord[1]) > 8 or (coord[0] or coord[1]) < 0:
            # Out of board coordinates
            return False

        if self._winner:
            # Winner decided
            return False

        # Valid action
        return True

    def place_fence(self, player, direction, coord):
        """Places a fence at the desired coordinates"""
        def remove_tuple(tuple_coord, v_moves):
            """Removes the tuple from the array of tuples"""
            new_list = [n for n in v_moves if n != tuple_coord]
            return new_list

        if not self.check_valid_action(player, coord):
            # Not a valid action
            return False
        if self._fences[player - 1] <= 0:
            # No fences remaining
            return False
        placed_fences = self.get_placed_fences()
        if coord in placed_fences[direction]:
            # Fence already at location
            return False
        else:
            # Successful fence placement
            placed_fences[direction].append(coord)
            if not self.call_fair_play(player):
                placed_fences[direction] = remove_tuple(coord, placed_fences[direction])
                return "breaks the fair play rule"
            self.update_turn()
            self._fences[player - 1] -= 1
            return True

    def move_pawn(self, player, coord):
        """Moves pawn to the following location"""

        if not self.check_valid_action(player, coord):
            # Not a valid action
            return False

        # Initialize valid moves array
        valid_moves = []

        def remove_tuple(tuple_coord, v_moves):
            """Removes the tuple from the array of tuples"""
            new_list = [n for n in v_moves if n != tuple_coord]
            return new_list

        def check_fence_blocker(chk_player, v_moves):
            """Check for fences and perform 1 square move"""
            pawns = self.get_pawns()

            # Check fences within 1 square
            player_location = pawns[chk_player - 1].get_coord()
            if player_location not in self._placed_fences["v"]:
                # Left clear
                new_location = (player_location[0] - 1, player_location[1])
                v_moves.append(new_location)
            if (player_location[0] + 1, player_location[1]) not in self._placed_fences["v"]:
                # Right clear
                new_location = (player_location[0] + 1, player_location[1])
                v_moves.append(new_location)
            if player_location not in self._placed_fences["h"]:
                # Top clear
                new_location = (player_location[0], player_location[1] - 1)
                v_moves.append(new_location)
            if (player_location[0], player_location[1] + 1) not in self._placed_fences["h"]:
                # Bottom clear
                new_location = (player_location[0], player_location[1] + 1)
                v_moves.append(new_location)

            # Return updated valid moves
            return v_moves

        def opp_pawn_check(chk_player, v_moves):
            """Check moves with adjacent opposing pawn"""

            def calculate_skip_move(player_loc, opp_loc, move_arr):
                """Update with valid skip move"""
                x_diff = opp_loc[0] - player_loc[0]
                y_diff = opp_loc[1] - player_loc[1]

                def y_skip():
                    # Opposing pawn is vertically adjacent
                    if (opp_loc[0], opp_loc[1] + 1) in fences["h"] or opp_loc in fences["h"]:
                        # Diagonal move allowed
                        move_arr.append((opp_loc[0] + 1, opp_loc[1]))
                        move_arr.append((opp_loc[0] - 1, opp_loc[1]))
                    else:
                        # Skip below
                        move_arr.append((opp_loc[0], opp_loc[1] + y_diff))

                    return move_arr

                def x_skip():
                    # Opposing pawn is horizontally adjacent
                    if (opp_loc[0] + 1, opp_loc[1]) in fences["v"] or opp_loc in fences["v"]:
                        # Diagonal move allowed
                        move_arr.append((opp_loc[0], opp_loc[1] + 1))
                        move_arr.append((opp_loc[0], opp_loc[1] - 1))
                    else:
                        # Skip below
                        move_arr.append((opp_loc[0] + x_diff, opp_loc[1]))

                    return move_arr

                fences = self._placed_fences

                if (x_diff in [-1, 1] and y_diff == 0) or (x_diff == 0 and y_diff in [-1, 1]):
                    # Opposing pawn is adjacent, remove position
                    if opp_loc not in move_arr:
                        return move_arr  # Must be a fence blocking this move
                    move_arr = remove_tuple(opp_loc, move_arr)
                    if y_diff in [-1, 1]:
                        move_arr = y_skip()
                    if x_diff in [-1, 1]:
                        move_arr = x_skip()

                return move_arr

            pawns = self.get_pawns()

            # Retrieve opposing pawn location
            player_location = pawns[chk_player - 1].get_coord()
            if chk_player == 1:
                opposing_location = pawns[1].get_coord()
            else:
                opposing_location = pawns[0].get_coord()

            v_moves = calculate_skip_move(player_location, opposing_location, v_moves)

            return v_moves

        # Perform fence check
        valid_moves = check_fence_blocker(player, valid_moves)

        # Perform opposing pawn check
        valid_moves = opp_pawn_check(player, valid_moves)

        # Update pawn position
        if coord in valid_moves:
            self.get_pawns()[player - 1].set_coord(coord)
            self.update_turn()
            self.check_winner()
            return True
        else:
            return False

    def print_board(self):
        """Prints a board state"""

        def initial_board():
            """Creates initial empty board"""

            # Create templates for each board element
            row = ""
            top_borders = ""
            divider = ""
            for j in range(0, 9):
                top_borders += "+===="
                row += "     "
                divider += "+    "
            top_borders += "+"
            row = row[1:45]
            row = "|" + row + "|"
            divider += "+"

            board_arr = []
            for k in range(1, 19):
                if k % 2 == 0:
                    board_arr.append(row)
                else:
                    board_arr.append(divider)
            board_arr[0] = top_borders
            board_arr.append(top_borders)
            return board_arr

        def place_pawns(board):
            """Place pawns on board"""
            pawn_list = self.get_pawns()
            p1 = pawn_list[0]
            p2 = pawn_list[1]

            def put_pawn(pawn, empty_board):
                """Place the specified pawn"""
                coord = pawn.get_coord()
                x = coord[0]
                y = coord[1]

                board_x = 5 * x + 2
                board_y = 2 * y + 1

                row = empty_board[board_y]
                new_row = ""
                for i in range(0, len(row)):
                    if i == board_x:
                        new_row += "P"
                    elif i == board_x + 1:
                        new_row += str(pawn.get_player())
                    else:
                        new_row += row[i]

                empty_board[board_y] = new_row

                return empty_board

            board = put_pawn(p1, board)
            return put_pawn(p2, board)

        def place_fences_print(board):
            """Place fences on board"""

            placed_fences = self.get_placed_fences()

            def print_vert_fence():
                """Print vertical fences"""
                for fence in placed_fences["v"]:
                    if fence[0] != 0:
                        # Not border fence
                        board_x = 5 * fence[0]
                        board_y = 2 * fence[1] + 1

                        row = board[board_y]
                        new_row = ""
                        for i in range(0, len(row)):
                            if i == board_x:
                                new_row += "|"
                            else:
                                new_row += row[i]
                        board[board_y] = new_row

            def print_horz_fence():
                """Print horizontal fences"""
                for fence in placed_fences["h"]:
                    if fence[1] != 0:
                        # Not border fence
                        board_x = 5 * fence[0] + 1
                        board_y = 2 * fence[1]

                        row = board[board_y]
                        new_row = ""
                        for i in range(0, len(row)):
                            if i in range(board_x, board_x + 4):
                                new_row += "="
                            else:
                                new_row += row[i]
                        board[board_y] = new_row

            # Run print fence functions
            print_vert_fence()
            print_horz_fence()

            # return board
            return board

        # Initialize board
        board = initial_board()

        # Add pawns
        board = place_pawns(board)

        # Add fences
        board = place_fences_print(board)

        # Print board
        for text in board:
            print(text)

    def fair_play(self, player):
        """"Check for fair play rules"""

        # Get current coordinates
        curr_coord = self.get_pawns()[player - 1].get_coord()

        # Establish win conditions
        if player == 1:
            win_cond = 8
        else:
            win_cond = 0

        # Establish history
        history = []
        history.append(curr_coord)

        def fair_play_recursive(coord, win_condition, coord_history):
            """Check for path to finish recursively"""

            # Base case - if we have reached the y value for the player's win condition
            for val in coord_history:
                if val[1] == win_condition:
                    return True
            else:
                # Perform recursive call

                def check_moves_fp(coord, win_condition, coord_history):
                    possible_moves = []
                    # Check fences within 1 square
                    if coord not in self._placed_fences["v"]:
                        # Left clear
                        new_location = (coord[0] - 1, coord[1])
                        if new_location not in coord_history:
                            possible_moves.append(new_location)
                    if (coord[0] + 1, coord[1]) not in self._placed_fences["v"]:
                        # Right clear
                        new_location = (coord[0] + 1, coord[1])
                        if new_location not in coord_history:
                            possible_moves.append(new_location)
                    if coord not in self._placed_fences["h"]:
                        # Top clear
                        new_location = (coord[0], coord[1] - 1)
                        if new_location not in coord_history:
                            possible_moves.append(new_location)
                    if (coord[0], coord[1] + 1) not in self._placed_fences["h"]:
                        # Bottom clear
                        new_location = (coord[0], coord[1] + 1)
                        if new_location not in coord_history:
                            possible_moves.append(new_location)

                    coord_history += possible_moves

                    return possible_moves

                possible_moves = check_moves_fp(coord, win_condition, coord_history)

                for move in possible_moves:
                    if fair_play_recursive(move, win_condition, coord_history):
                        return True

        if fair_play_recursive(curr_coord, win_cond, history):
            return True
        else:
            return False

    def call_fair_play(self, player):
        """Calls the fair play function with correct value"""
        if player == 1:
            return self.fair_play(2)
        else:
            return self.fair_play(1)


# q = QuoridorGame()
#
# print(q.place_fence(1,"v", (2,4)))
# print(q.place_fence(2,"h", (2,4)))
# print(q.place_fence(1,"v", (5,5)))
# print(q.move_pawn(2, (3,8)))
# print(q.place_fence(1,"v", (3,8)))
# print(q.move_pawn(2, (3,7)))
# print(q.move_pawn(1, (4,1)))
# print(q.move_pawn(2, (4,7)))
# print(q.move_pawn(1, (4,2)))
# print(q.move_pawn(2, (4,6)))
# print(q.move_pawn(1, (4,3)))
# print(q.move_pawn(2, (4,5)))
# print(q.move_pawn(1, (4,4)))
# print(q.move_pawn(2, (4,3)))
# print(q.move_pawn(1, (5,4)))
# print(q.move_pawn(2, (4,4)))
# print(q.move_pawn(1, (4,3)))
# print(q.place_fence(1,"v", (4,4)))
# print(q.place_fence(2,"v", (6,4)))
# print(q.place_fence(1,"v", (7,4)))
# print(q.place_fence(2,"h", (4,4)))
# print(q.move_pawn(1, (4,3)))
# print(q.place_fence(2,"v", (5,4)))
# print(q.place_fence(1,"h", (4,5)))
# print(q.place_fence(1,"h", (4,5)))
# print(q.place_fence(1,"h", (4,5)))
# print("FAIR PLAY TEST")
# print(q.fair_play(1))
# print(q.fair_play(2))
#
# #print(q.move_pawn(1, (3,4)))
#
#
# q.print_board()
# print("done")
