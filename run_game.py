import random
from player import Player


class GameLogicError(Exception):
    '''Raise for errors found within the gaming logic'''


class PlayerInputError(Exception):
    '''Raise for errors in the input of the player list while running a game'''


# Rolls 6 dice randomly.
# According to the game, the first two dice are white, the third is red, the fourth is yellow, the fifth is green, and
# the sixth is blue.
def roll_dice():
    return tuple(random.randint(1, 6) for i in range(6))


# Takes the outcome of the white dice and decides for a player which number in which row they are going to cross out
# by choosing one of the left most number of numbers they are willing to take.
# This decision is based on the simplest of strategies.
# Different decision functions could be used for non-basic players.
def player_decision_white_outcome(player, white_dice_outcome, print_player_decision_making):
    playable_options = []
    if white_dice_outcome in player.playable_numbers['red']:
        playable_options.append(['red', white_dice_outcome, white_dice_outcome - 1])
    if white_dice_outcome in player.playable_numbers['yellow']:
        playable_options.append(['yellow', white_dice_outcome, white_dice_outcome - 1])
    if white_dice_outcome in player.playable_numbers['green']:
        playable_options.append(['green', white_dice_outcome, 13 - white_dice_outcome])
    if white_dice_outcome in player.playable_numbers['blue']:
        playable_options.append(['blue', white_dice_outcome, 13 - white_dice_outcome])
    if print_player_decision_making != False:
        print('\tPlayable Options:', playable_options)
    left_numbers = []
    for possible_option in playable_options:
        left_numbers.append(possible_option[2])
    best_playable_options = []
    for possible_option in playable_options:
        if possible_option[2] == min(left_numbers):
            best_playable_options.append(possible_option)
    if print_player_decision_making != False:
        print('\tBest Playable Options:', best_playable_options)
    if len(best_playable_options) > 1:
        final_choice = random.choice(best_playable_options)
    elif len(best_playable_options) == 1:
        final_choice = best_playable_options[0]
    else:
        final_choice = None
    if print_player_decision_making != False:
        print('\tFinal Choice:', final_choice)
    return final_choice


# Takes the color and number decided by a player to cross out and adds that number to their list of numbers crossed out.
# The players open numbers list is updated based upon the color and number crossed out.
# If the player locked out a row this turn, that information is added to the players information and the
# row_closed_info is returned and updated with the information of which row was locked.
def cross_out_number(player, color, number, row_closed_info):
    red_row_closed_out = row_closed_info['red_row_closed_out']
    yellow_row_closed_out = row_closed_info['yellow_row_closed_out']
    green_row_closed_out = row_closed_info['green_row_closed_out']
    blue_row_closed_out = row_closed_info['blue_row_closed_out']
    row_closed_this_turn = row_closed_info['row_closed_this_turn']
    player.crossed_out_numbers[color].append(number)
    if color == 'red' or color == 'yellow':
        if len(player.crossed_out_numbers[color]) < 5:
            if number < 11:
                player.open_numbers[color] = [i for i in range(number + 1, 12)]
            else:
                player.open_numbers[color] = []
        else:
            if number < 12:
                player.open_numbers[color] = [i for i in range(number + 1, 13)]
            else:
                player.open_numbers[color] = []
                player.crossed_out_numbers[color].append('locked')
                if color == 'red':
                    red_row_closed_out = True
                    row_closed_this_turn = 'red'
                elif color == 'yellow':
                    yellow_row_closed_out = True
                    row_closed_this_turn = 'yellow'
    elif color == 'green' or color == 'blue':
        if len(player.crossed_out_numbers[color]) < 5:
            if number > 3:
                player.open_numbers[color] = [i for i in range(number - 1, 2, -1)]
            else:
                player.open_numbers[color] = []
        else:
            if number > 2:
                player.open_numbers[color] = [i for i in range(number - 1, 1, -1)]
            else:
                player.open_numbers[color] = []
                player.crossed_out_numbers[color].append('locked')
                if color == 'green':
                    green_row_closed_out = True
                    row_closed_this_turn = 'green'
                elif color == 'blue':
                    blue_row_closed_out = True
                    row_closed_this_turn = 'blue'

    return {'red_row_closed_out': red_row_closed_out, 'yellow_row_closed_out': yellow_row_closed_out,
            'green_row_closed_out': green_row_closed_out, 'blue_row_closed_out': blue_row_closed_out,
            'row_closed_this_turn': row_closed_this_turn}


# Takes the outcome of all the dice rolled this turn and
def get_colored_dice_options(dice_rolls, print_players_decision_making):
    options = []
    options.append(['red', dice_rolls[0] + dice_rolls[2], (dice_rolls[0] + dice_rolls[2]) - 1])
    options.append(['yellow', dice_rolls[0] + dice_rolls[3], (dice_rolls[0] + dice_rolls[3]) - 1])
    options.append(['green', dice_rolls[0] + dice_rolls[4], 13 - (dice_rolls[0] + dice_rolls[4])])
    options.append(['blue', dice_rolls[0] + dice_rolls[5], 13 - (dice_rolls[0] + dice_rolls[5])])
    if dice_rolls[0] != dice_rolls[1]:
        options.append(['red', dice_rolls[1] + dice_rolls[2], (dice_rolls[1] + dice_rolls[2]) - 1])
        options.append(['yellow', dice_rolls[1] + dice_rolls[3], (dice_rolls[1] + dice_rolls[3]) - 1])
        options.append(['green', dice_rolls[1] + dice_rolls[4], 13 - (dice_rolls[1] + dice_rolls[4])])
        options.append(['blue', dice_rolls[1] + dice_rolls[5], 13 - (dice_rolls[1] + dice_rolls[5])])
    if print_players_decision_making != False:
        print('\tAll Colored Dice Options:', options)
    return options


# gealkjlakjs
def get_colored_dice_decision(player, colored_dice_options, print_players_decision_making):
    playable_options = []
    for option in colored_dice_options:
        if option[1] in player.playable_numbers[option[0]] and option not in playable_options:
            playable_options.append(option)
    if print_players_decision_making != False:
        print('\tPlayable Options:', playable_options)
    left_numbers = []
    for option in playable_options:
        left_numbers.append(option[2])
    best_playable_options = []
    for option in playable_options:
        if option[2] == min(left_numbers):
            best_playable_options.append(option)
    if print_players_decision_making != False:
        print('\tBest Playable Options:', best_playable_options)
    if len(best_playable_options) > 1:
        final_choice = random.choice(best_playable_options)
    elif len(best_playable_options) == 1:
        final_choice = best_playable_options[0]
    else:
        final_choice = None
    if print_players_decision_making != False:
        print('\tFinal Choice:', final_choice)
    return final_choice


# run a Game
def run_game(player_list, print_game_info=False, print_player_sheets=False, print_all_player_info=False,
             print_players_decision_making=False):
    if type(player_list) != type([]):
        raise PlayerInputError('Player list is not a list')
    if len(player_list) < 2:
        raise PlayerInputError('Player list is less than 2 players')
    list_of_all_players = []
    assigned_player_number = 0
    for player_strategy in player_list:
        assigned_player_number += 1
        list_of_all_players.append(Player(assigned_player_number, player_strategy))
    number_of_players = len(list_of_all_players)
    starting_player = random.choice(list_of_all_players)
    active_player = starting_player
    row_closed_info = {'red_row_closed_out': False, 'yellow_row_closed_out': False, 'green_row_closed_out': False,
                       'blue_row_closed_out': False, 'row_closed_this_turn': False}
    number_of_rows_closed_to_end_game = 2
    number_of_rows_closed = 0
    turn_count = 1
    end_game = False
    game_ended_on_white_dice_lock = False
    if print_game_info != False:
        print('{:-^80}'.format('New Game'))
        print('Players are:', list_of_all_players)
        print('Player {} starts first\n'.format(starting_player.player_number))
    if print_all_player_info != False:
        print('Starting Player Information')
        for player in list_of_all_players:
            player.print_player_info()
        print('')
    if print_player_sheets != False:
        for player in list_of_all_players:
            player.print_player_sheet()
        print('')
    while end_game == False:
        if print_game_info != False:
            print('{:20}{:-^40}{:20}'.format(' ', 'Turn ' + str(turn_count), ' '))
            print('Active Player is Player ', active_player.player_number)
        row_closed_info['row_closed_this_turn'] = False
        rows_closed_this_round = []
        player_index = list_of_all_players.index(active_player)
        active_player_take_white = False
        dice_roll = roll_dice()
        if print_game_info != False:
            print('Dice Roll Outcome')
            print(' W  W  R  Y  G  B')
            print(dice_roll)
        white_dice_outcome = dice_roll[0] + dice_roll[1]
        if print_players_decision_making != False:
            print('White Dice Outcome: ', white_dice_outcome)
        for i in range(number_of_players):
            player_deciding = list_of_all_players[player_index]
            if print_players_decision_making != False:
                print('Player {} is deciding on the white dice outcome'.format(player_deciding.player_number))
            white_dice_decision = player_decision_white_outcome(player_deciding, white_dice_outcome,
                                                                print_players_decision_making)
            if white_dice_decision != None:
                row_closed_info = cross_out_number(player_deciding, white_dice_decision[0], white_dice_decision[1],
                                                   row_closed_info)
                if print_game_info != False:
                    print('Player {} crossed out {} {}'.format(player_deciding.player_number,
                                                               str(white_dice_decision[0]),
                                                               white_dice_decision[1]))
                if row_closed_info['row_closed_this_turn'] != False:
                    if row_closed_info['row_closed_this_turn'] not in rows_closed_this_round:
                        rows_closed_this_round.append(row_closed_info['row_closed_this_turn'])
                    if print_game_info != False:
                        for row in rows_closed_this_round:
                            if 'locked' in player_deciding.crossed_out_numbers[row]:
                                print('Player {} locked the {} row'.format(player_deciding.player_number, row))
                if active_player == player_deciding:
                    active_player_take_white = True
            player_index += 1
            if player_index == number_of_players:
                player_index = 0
        if rows_closed_this_round != []:
            for player in list_of_all_players:
                for row in rows_closed_this_round:
                    player.open_numbers[row] = []
            if len(rows_closed_this_round) + number_of_rows_closed >= number_of_rows_closed_to_end_game:
                if print_game_info != False:
                    print('{} rows have been closed this game'.format(
                        len(rows_closed_this_round) + number_of_rows_closed))
                game_ended_on_white_dice_lock = True
                break
        if print_players_decision_making != False:
            print('Player {} is deciding on the colored dice outcome'.format(active_player.player_number))
        colored_dice_options = get_colored_dice_options(dice_roll, print_players_decision_making)
        colored_dice_decision = get_colored_dice_decision(active_player, colored_dice_options,
                                                          print_players_decision_making)
        if colored_dice_decision != None:
            row_closed_info = cross_out_number(active_player, colored_dice_decision[0], colored_dice_decision[1],
                                               row_closed_info)
            if print_game_info != False:
                print('Player {} crossed out {} {}'.format(active_player.player_number, colored_dice_decision[0],
                                                           colored_dice_decision[1]))
            if row_closed_info['row_closed_this_turn'] != False:
                if row_closed_info['row_closed_this_turn'] not in rows_closed_this_round:
                    rows_closed_this_round.append(row_closed_info['row_closed_this_turn'])
                    if print_game_info != False:
                        print('Player {} locked out row {}'.format(active_player.player_number,
                                                                   row_closed_info['row_closed_this_turn']))
        if active_player_take_white == False and colored_dice_decision == None:
            active_player.amount_of_penalties += 1
            if print_game_info != False:
                if active_player.amount_of_penalties == 1:
                    print('Player {} took a penalty. They now have {} penalty'.format(active_player.player_number,
                                                                                      active_player.amount_of_penalties))
                else:
                    print('Player {} took a penalty. They now have {} penalties'.format(active_player.player_number,
                                                                                        active_player.amount_of_penalties))
        if list_of_all_players.index(active_player) + 1 == number_of_players:
            active_player = list_of_all_players[0]
        else:
            active_player = list_of_all_players[list_of_all_players.index(active_player) + 1]
        if rows_closed_this_round != []:
            number_of_rows_closed += len(rows_closed_this_round)
            for player in list_of_all_players:
                for row in rows_closed_this_round:
                    player.open_numbers[row] = []
            if print_game_info != False:
                print('{} rows have been closed this game'.format(number_of_rows_closed))
        for player in list_of_all_players:
            if player.amount_of_penalties >= 4:
                end_game = True
        if number_of_rows_closed >= number_of_rows_closed_to_end_game:
            end_game = True
        turn_count += 1
        if turn_count >= 100:
            end_game = True
        if print_all_player_info != False:
            for player in list_of_all_players:
                player.print_player_info()
        if print_player_sheets != False:
            for player in list_of_all_players:
                player.print_player_sheet()
    if game_ended_on_white_dice_lock == True:
        if print_all_player_info != False:
            for player in list_of_all_players:
                player.print_player_info()
        if print_player_sheets != False:
            for player in list_of_all_players:
                player.print_player_sheet()
    if print_game_info != False:
        print('{:-^80}'.format('Game Over'))
    final_scores = []
    winning_player = None
    for player in list_of_all_players:
        final_scores.append(player.total_points)
    for player in list_of_all_players:
        if player.total_points == max(final_scores):
            winning_player = player
    return [list_of_all_players, final_scores, winning_player]


if __name__ == '__main__':
    player_list = [2, 3, 3, 4]
    run_game(player_list, print_game_info=True, print_player_sheets=True, print_all_player_info=True,
             print_players_decision_making=True)
