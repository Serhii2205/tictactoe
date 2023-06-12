import sys
from time import sleep
from itertools import product
from functools import cached_property


class TicTacToe:
    STEP = 1
    SYMBOLS = ['X', '0']
    WIN_COMBINATIONS = [
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
        {1, 4, 7},
        {2, 5, 8},
        {3, 6, 9},
        {1, 5, 9},
        {3, 5, 7}
    ]

    def __init__(self):
        self.player_1 = None
        self.player_2 = None

    @cached_property
    def coordinates(self):
        return self.create_coords()

    @staticmethod
    def create_coords():
        coordinates = []
        comb = list(map(str, range(1, 4)))

        for coord, combination in enumerate(product(comb, comb), start=1):
            row, column = combination
            coordinates.append(
                {'row': row, 'column': column, 'coord': coord, 'symbol': ' '}
            )

        return coordinates

    @staticmethod
    def create_table():
        border = "---------\n"
        row = "| {} {} {} |\n"

        return border + row * 3 + border

    def get_coord(self, row: int, column: int, player_symbol: str):
        self.validate_row_and_column_input(row=row, column=column)

        for coord in self.coordinates:
            if coord['row'] == row and coord['column'] == column:
                if coord['symbol'] == ' ':
                    coord['symbol'] = player_symbol
                    return coord['coord']
                else:
                    print('Already marked! Please re-enter')

    def make_a_move(self):
        for _ in range(9):
            player_number = 1 if self.STEP % 2 != 0 else 2
            player_symbol = self.player_1 if self.STEP % 2 != 0 else self.player_2
            coord = None

            while not coord:
                player_input = input(
                    f"Player {player_number}\nEnter the row and column number separated by a space:  "
                )
                try:
                    coord = self.get_coord(*player_input.split(), player_symbol)
                except TypeError:
                    print('Invalid format. Please re-enter')

            print(self.fill_table())
            self.STEP += 1

            if self.STEP > 5:
                if self.check_win(player_symbol, player_number):
                    return True
        else:
            print('Draw!')
            print(self.fill_table())
            sleep(0.3)
            print('Game Over')

    def fill_table(self):
        return self.create_table().format(*[coord['symbol'] for coord in self.coordinates])

    def start_game(self):
        print('Welcome to Tic-Tac-Toe game:) \n_______________________________')
        sleep(0.3)
        self.player_1 = self.validate_input(input("Select symbol for player 1 'X' or '0':  "))
        self.set_symbol_for_player_2()

        self.make_a_move()

    def validate_input(self, player_input: str):
        while player_input not in self.SYMBOLS:
            player_input = input('Error: please enter a valid symbol X or 0:  ')

        return player_input

    @staticmethod
    def validate_row_and_column_input(**kwargs):
        for elem in kwargs.items():
            if not (elem[1].isdigit() and 0 < int(elem[1]) <= 3):
                print(f'{elem[0].capitalize()} value is out of range. Please re-enter')

    def set_symbol_for_player_2(self):
        symbols_copy = self.SYMBOLS.copy()
        self.player_2 = (
            symbols_copy.remove(self.player_1), symbols_copy[0]
        )[1]

    def check_win(self, player_char, player_number):
        set_values = {
            coord['coord'] for coord in self.coordinates if player_char == coord['symbol']
        }
        for combination in self.WIN_COMBINATIONS:
            if set_values.issuperset(combination):
                print(f'Player {player_number} has won!')

                self.render_final_table(combination)
                sleep(0.3)
                print('Game Over')

                return True

    def render_final_table(self, win_combination):
        for coord in self.coordinates:
            if coord['coord'] in win_combination:
                coord['symbol'] = '\u0336' + coord['symbol'] + '\u0336'
        print(self.fill_table())


if __name__ == "__main__":
    try:
        while True:
            TicTacToe().start_game()
            again = input('\n' * 2 + 'Do you want to play again ? Y/N:  ')
            if again.lower() == 'y':
                continue
            else:
                print('Bye :)')
                break
    except KeyboardInterrupt as k:
        print("  Interrupted by user")
        sys.exit(0)
