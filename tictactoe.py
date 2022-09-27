import sys


class TicTacToe:
    step = 1
    symbols = ['X', '0']
    coords = [
        {'row': '1', 'column': '1', 'coord': 1, 'symbol': ' '},
        {'row': '1', 'column': '2', 'coord': 2, 'symbol': ' '},
        {'row': '1', 'column': '3', 'coord': 3, 'symbol': ' '},
        {'row': '2', 'column': '1', 'coord': 4, 'symbol': ' '},
        {'row': '2', 'column': '2', 'coord': 5, 'symbol': ' '},
        {'row': '2', 'column': '3', 'coord': 6, 'symbol': ' '},
        {'row': '3', 'column': '1', 'coord': 7, 'symbol': ' '},
        {'row': '3', 'column': '2', 'coord': 8, 'symbol': ' '},
        {'row': '3', 'column': '3', 'coord': 9, 'symbol': ' '},
    ]
    win_combinations = [
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

    @staticmethod
    def create_table():
        border = "---------\n"
        row = "| {} {} {} |\n"
        return border + row * 3 + border

    def get_coord(self, row, column, player_symbol):
        # ToDo add row and column validation
        for coord in self.coords:
            if coord['row'] == row and coord['column'] == column:
                if coord['symbol'] == ' ':
                    coord['symbol'] = player_symbol
                    return coord['coord']
                else:
                    print('Already marked! Please re-enter')

    def make_a_move(self):
        for _ in range(9):
            player_number = 1 if self.step % 2 != 0 else 2
            player_symbol = self.player_1 if self.step % 2 != 0 else self.player_2
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
            self.step += 1

            if self.step > 5:
                if self.check_win(player_symbol, player_number):
                    return True
        else:
            print('Draw!')

    def fill_table(self):
        return self.create_table().format(*[coord['symbol'] for coord in self.coords])

    def start_game(self):
        self.player_1 = self.validate_input(input('Select symbol for player 1 X or 0:  '))
        self.set_symbol_for_player_2()

        self.make_a_move()

    def validate_input(self, player_input):
        while player_input not in self.symbols:
            player_input = input('Error: please enter a valid symbol X or 0:  ')
        return player_input

    def set_symbol_for_player_2(self):
        symbols_copy = self.symbols.copy()
        self.player_2 = (
            symbols_copy.remove(self.player_1), symbols_copy[0]
        )[1]

    def check_win(self, player_char, player_number):
        set_values = {
            coord['coord'] for coord in self.coords if player_char == coord['symbol']
        }
        for combination in self.win_combinations:
            if set_values.issuperset(combination):
                print(f'Player {player_number} has won!')
                print('Game Over')
                return True


if __name__ == "__main__":
    try:
        while True:
            TicTacToe().start_game()
            again = input('\n' * 3 + 'Do you want to play again ? Y/N:  ')
            if again.lower() == 'y':
                continue
            else:
                break
    except KeyboardInterrupt as k:
        print("  Interrupted")
        sys.exit(0)
