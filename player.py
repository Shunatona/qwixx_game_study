# Holds all the information needed for a single player during a game.
class Player:
    # Initiate all the class variables.
    # player_number: Which player they are within the current game (Player 1, Player 2...)
    # amount_of_playable_numbers: The base of a players strategy. How many numbers, out off all the numbers they have
    #   open to play, on the left most side they would consider playing. (A 2 says that a player will only consider
    #   their two leftmost open numbers in any column.)
    # open_numbers: All the numbers the player has open to play based on game rules. (no strategy involved)
    # crossed_out_numbers: Numbers crossed out in their respective colors.
    # amount_of_penalties: The number of penalties a player has taken over a game.
    def __init__(self, player_number, amount_of_playable_numbers):
        self.player_number = player_number
        self.amount_of_playable_numbers = amount_of_playable_numbers
        self.open_numbers = {'red': [i for i in range(2, 12)], 'yellow': [i for i in range(2, 12)],
                             'green': [12 - i for i in range(10)], 'blue': [12 - i for i in range(10)]}
        self.crossed_out_numbers = {'red': [], 'yellow': [], 'green': [], 'blue': []}
        self.amount_of_penalties = 0

    # The string value to be returned when player object is represented.
    def __repr__(self):
        return str('Player({},{})'.format(str(self.player_number), str(self.amount_of_playable_numbers)))

    # The playable numbers of each row for the player based on player strategy and game rules.
    @property
    def playable_numbers(self):
        return {'red': self.get_playable_numbers('red'), 'yellow': self.get_playable_numbers('yellow'),
                'green': self.get_playable_numbers('green'), 'blue': self.get_playable_numbers('blue')}

    # Select which numbers the player will consider for a color based on strategy. For a basic player only the
    #   amount_of_playable_numbers is taken into consideration for strategy.
    def get_playable_numbers(self, color):
        return self.open_numbers[color][0:self.amount_of_playable_numbers]

    # The points the player has in each color based on the amount of crossed out numbers and lock out bonus.
    @property
    def color_points(self):
        return {'red': self.get_score('red'), 'yellow': self.get_score('yellow'), 'green': self.get_score('green'),
                'blue': self.get_score('blue')}

    # Count the number of crossed out numbers and lock out bonus for a color for the player and return the score
    #   associated.
    def get_score(self, color):
        if self.crossed_out_numbers[color] == []:
            number_of_crosses = 0
        else:
            number_of_crosses = len(self.crossed_out_numbers[color])
        score_list = (0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78)
        return score_list[number_of_crosses]

    # The total points the player has by adding all color points and deducting penalties.
    @property
    def total_points(self):
        return self.color_points['red'] + self.color_points['yellow'] + self.color_points['blue'] + self.color_points[
            'green'] - 5 * self.amount_of_penalties

    # Print out all the information held of a player.
    def print_player_info(self):
        print('Information on Player {}'.format(self.player_number))
        print("\tPlayer's Strategy")
        print('\t\tBasic {} Playable Numbers'.format(self.amount_of_playable_numbers))
        print("\tPlayer's Open Numbers")
        print('\t\tRed:', self.open_numbers['red'])
        print('\t\tYellow:', self.open_numbers['yellow'])
        print('\t\tGreen:', self.open_numbers['green'])
        print('\t\tBlue:', self.open_numbers['blue'])
        print("\tPlayer's Playable Numbers")
        print('\t\tRed:', self.playable_numbers['red'])
        print('\t\tYellow:', self.playable_numbers['yellow'])
        print('\t\tGreen:', self.playable_numbers['green'])
        print('\t\tBlue:', self.playable_numbers['blue'])
        print("\tPlayer's Crossed Out Numbers and Locked Rows")
        print('\t\tRed:', self.crossed_out_numbers['red'])
        print('\t\tYellow:', self.crossed_out_numbers['yellow'])
        print('\t\tGreen:', self.crossed_out_numbers['green'])
        print('\t\tBlue:', self.crossed_out_numbers['blue'])
        print("\tPlayer's Number of Penalties")
        print('\t\t', self.amount_of_penalties)
        print("\tPlayer's Points")
        print('\t\tRed:', self.color_points['red'])
        print('\t\tYellow:', self.color_points['yellow'])
        print('\t\tGreen:', self.color_points['green'])
        print('\t\tBlue:', self.color_points['blue'])
        print('\t\tPenalties:', -5 * self.amount_of_penalties)
        print('\t\tTotal Points:', self.total_points, '\n')

    # Print out a player's score pad.
    def print_player_sheet(self):
        print('{:-^80}'.format("Player {}'s Score Pad".format(self.player_number)))
        print('{:<8}'.format('Red'), end='')
        for i in self.row_in_player_sheet('red'):
            print('[{:^4}]'.format(i), end='')
        print('')
        print('{:<8}'.format('Yellow'), end='')
        for i in self.row_in_player_sheet('yellow'):
            print('[{:^4}]'.format(i), end='')
        print('')
        print('{:<8}'.format('Green'), end='')
        for i in self.row_in_player_sheet('green'):
            print('[{:^4}]'.format(i), end='')
        print('')
        print('{:<8}'.format('Blue'), end='')
        for i in self.row_in_player_sheet('blue'):
            print('[{:^4}]'.format(i), end='')
        print('')
        penalties_string = 'Penalties [{}]'.format(self.amount_of_penalties)
        print('{:>80}'.format(penalties_string))
        print('\t\t{:^9} {:^9} {:^9} {:^9} {:^9} {:^9}'.format('Red', 'Yellow', 'Green', 'Blue', 'Penalties', 'Total'))
        print('{:^8} [{:^5}] + [{:^5}] + [{:^5}] + [{:^5}] - [{:^5}] = [{:^5}]'.format('Totals',
                                                                                       self.color_points['red'],
                                                                                       self.color_points['yellow'],
                                                                                       self.color_points['green'],
                                                                                       self.color_points['blue'],
                                                                                       5 * self.amount_of_penalties,
                                                                                       self.total_points))
        print('{:-^80}\n'.format('-'))

    # Finds the characters used to print a color's rows in player's score card.
    def row_in_player_sheet(self, color):
        colors_crossed_out_numbers = self.crossed_out_numbers[color]
        row = []
        if color == 'red' or color == 'yellow':
            for i in range(2, 14):
                if i in colors_crossed_out_numbers:
                    row.append('X')
                elif i == 13 and 'locked' not in colors_crossed_out_numbers:
                    row.append('\U0001f513')
                elif i == 13 and 'locked' in colors_crossed_out_numbers:
                    row.append('X\U0001f512')
                else:
                    row.append('{}'.format(str(i)))
        elif color == 'green' or color == 'blue':
            for i in range(12, 0, -1):
                if i in colors_crossed_out_numbers:
                    row.append('X')
                elif i == 1 and 'locked' not in colors_crossed_out_numbers:
                    row.append('\U0001f513')
                elif i == 1 and 'locked' in colors_crossed_out_numbers:
                    row.append('X\U0001f512')
                else:
                    row.append('{}'.format(str(i)))
        return row