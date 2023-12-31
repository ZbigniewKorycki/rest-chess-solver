from figure import Figure
from chessboard import Chessboard
from collections import namedtuple
from typing import Optional, Tuple


class Bishop(Figure):
    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = []
        directions = [
            Chessboard.get_field_after_move_up_left,
            Chessboard.get_field_after_move_up_right,
            Chessboard.get_field_after_move_down_left,
            Chessboard.get_field_after_move_down_right,
        ]
        for direction in directions:
            for distance_to_possible_field in range(1, 8):
                possible_field = direction(
                    self.current_field, distance_to_possible_field
                )
                if Chessboard.check_if_field_in_chessboard(possible_field):
                    available_moves.append(possible_field)
                else:
                    break
        return sorted(available_moves)

    def validate_move(self, dest_field: str) -> bool:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")
        if not dest_field.upper() in self.list_available_moves():
            return False
        else:
            return True


class King(Figure):
    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = []
        directions = [
            Chessboard.get_field_after_move_up,
            Chessboard.get_field_after_move_down,
            Chessboard.get_field_after_move_left,
            Chessboard.get_field_after_move_right,
            Chessboard.get_field_after_move_up_left,
            Chessboard.get_field_after_move_up_right,
            Chessboard.get_field_after_move_down_left,
            Chessboard.get_field_after_move_down_right,
        ]
        for direction in directions:
            dist_to_poss_field = 1
            possible_field = direction(self.current_field, dist_to_poss_field)
            if Chessboard.check_if_field_in_chessboard(possible_field):
                available_moves.append(possible_field)
        return sorted(available_moves)

    def validate_move(self, dest_field: str) -> bool:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")
        if not dest_field.upper() in self.list_available_moves():
            return False
        else:
            return True


class Knight(Figure):
    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = []
        directions_combinations = [
            [
                Chessboard.get_field_after_move_up,
                Chessboard.get_field_after_move_right,
            ],
            [
                Chessboard.get_field_after_move_up,
                Chessboard.get_field_after_move_left,
            ],
            [
                Chessboard.get_field_after_move_down,
                Chessboard.get_field_after_move_right,
            ],
            [
                Chessboard.get_field_after_move_down,
                Chessboard.get_field_after_move_left,
            ],
            [
                Chessboard.get_field_after_move_left,
                Chessboard.get_field_after_move_up,
            ],
            [
                Chessboard.get_field_after_move_left,
                Chessboard.get_field_after_move_down,
            ],
            [
                Chessboard.get_field_after_move_right,
                Chessboard.get_field_after_move_up,
            ],
            [
                Chessboard.get_field_after_move_right,
                Chessboard.get_field_after_move_down,
            ],
        ]
        for direction in directions_combinations:
            dist_to_inter_field = 2
            dist_to_poss_field = 1
            possible_field = direction[1](
                direction[0](self.current_field, dist_to_inter_field),
                dist_to_poss_field,
            )
            if Chessboard.check_if_field_in_chessboard(possible_field):
                available_moves.append(possible_field)
        return sorted(available_moves)

    def validate_move(self, dest_field: str) -> bool:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")
        if not dest_field.upper() in self.list_available_moves():
            return False
        else:
            return True


class Pawn(Figure):
    MoveValidationFigureColor = Tuple[Optional[bool], Optional[bool]]

    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = [{"blacks": [], "whites": []}]
        direction_for_whites = Chessboard.get_field_after_move_up
        direction_for_blacks = Chessboard.get_field_after_move_down
        current_column, current_row = Chessboard.get_col_and_row_from_field(
            self.current_field
        )

        def add_to_available_moves(color, field):
            if Chessboard.check_if_field_in_chessboard(field):
                available_moves[0][color].append(field)

        if current_row == 2:
            for dist_to_poss_field_for_whites in [1, 2]:
                add_to_available_moves(
                    "whites",
                    direction_for_whites(
                        self.current_field, dist_to_poss_field_for_whites
                    ),
                )
            add_to_available_moves(
                "blacks", direction_for_blacks(self.current_field, 1)
            )

        elif current_row == 7:
            add_to_available_moves(
                "whites", direction_for_whites(self.current_field, 1)
            )

            for dist_to_poss_field_for_blacks in [1, 2]:
                add_to_available_moves(
                    "blacks",
                    direction_for_blacks(
                        self.current_field, dist_to_poss_field_for_blacks
                    ),
                )

        elif 3 <= current_row <= 6:
            add_to_available_moves(
                "whites", direction_for_whites(self.current_field, 1)
            )
            add_to_available_moves(
                "blacks", direction_for_blacks(self.current_field, 1)
            )

        elif current_row == 1:
            return [{"whites": None, "blacks": []}]
        elif current_row == 8:
            return [{"whites": [], "blacks": None}]
        return available_moves

    def validate_move(self, dest_field: str) -> MoveValidationFigureColor:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")

        available_moves = self.list_available_moves()[0]
        is_valid_for_color = namedtuple("valid_for_color", ["white", "black"])

        if available_moves["blacks"] is None:
            return is_valid_for_color(False, None)

        elif available_moves["whites"] is None:
            return is_valid_for_color(None, False)

        dest_field_in_whites = dest_field.upper() in available_moves["whites"]
        dest_field_in_blacks = dest_field.upper() in available_moves["blacks"]

        return is_valid_for_color(dest_field_in_whites, dest_field_in_blacks)


class Queen(Figure):
    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = []
        directions = [
            Chessboard.get_field_after_move_up,
            Chessboard.get_field_after_move_down,
            Chessboard.get_field_after_move_left,
            Chessboard.get_field_after_move_right,
            Chessboard.get_field_after_move_up_left,
            Chessboard.get_field_after_move_up_right,
            Chessboard.get_field_after_move_down_left,
            Chessboard.get_field_after_move_down_right,
        ]
        for direction in directions:
            for distance_to_possible_field in range(1, 8):
                possible_field = direction(
                    self.current_field, distance_to_possible_field
                )
                if Chessboard.check_if_field_in_chessboard(possible_field):
                    available_moves.append(possible_field)
                else:
                    break
        return sorted(available_moves)

    def validate_move(self, dest_field: str) -> bool:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")
        if not dest_field.upper() in self.list_available_moves():
            return False
        else:
            return True


class Rook(Figure):
    def __init__(self, current_field: str):
        super().__init__(current_field)

    def list_available_moves(self) -> list:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        available_moves = []
        directions = [
            Chessboard.get_field_after_move_up,
            Chessboard.get_field_after_move_down,
            Chessboard.get_field_after_move_left,
            Chessboard.get_field_after_move_right,
        ]
        for direction in directions:
            for distance_to_possible_field in range(1, 8):
                possible_field = direction(
                    self.current_field, distance_to_possible_field
                )
                if Chessboard.check_if_field_in_chessboard(possible_field):
                    available_moves.append(possible_field)
                else:
                    break
        return sorted(available_moves)

    def validate_move(self, dest_field: str) -> bool:
        if not Chessboard.check_if_field_in_chessboard(self.current_field):
            raise ValueError("current field does not exist")
        if not Chessboard.check_if_field_in_chessboard(dest_field):
            raise ValueError("destination field does not exist")
        if not dest_field.upper() in self.list_available_moves():
            return False
        else:
            return True
