import matplotlib.pyplot as pyplot
import numpy
import time
from run_game import run_game

def run_multiple_games(number_of_games,player_list,print_info=False):
    number_of_players = len(player_list)
    game_outcomes = []
    for i in range(number_of_games):
        game_outcomes.append(run_game(player_list))
    if print_info != False:
        print('Number of games ran:', number_of_games)
        print('List of all players:', game_outcomes[0][0])
    players_info = []
    for i in range(number_of_players):
        player_dict = {'player_number': i + 1, 'player_strategy': player_list[i]}
        players_info.append(player_dict)
    for player_dictionary in players_info:
        number_of_wins = 0
        list_of_player_scores = []
        for game_outcome in game_outcomes:
            if player_dictionary['player_number'] == game_outcome[2].player_number:
                number_of_wins += 1
            list_of_player_scores.append(game_outcome[1][player_dictionary['player_number'] - 1])
        player_dictionary['number_of_total_wins'] = number_of_wins
        player_dictionary['list_of_player_scores'] = list_of_player_scores
        player_dictionary['average_score'] = numpy.mean(list_of_player_scores)
        player_dictionary['min_score'] = min(list_of_player_scores)
        player_dictionary['max_score'] = max(list_of_player_scores)
    for player_dictionary in players_info:
        player_dictionary['win_percentage'] = 100 * player_dictionary['number_of_total_wins'] / number_of_games
    if print_info != False:
        for player_info in players_info:
            print('Player {} Information'.format(player_info['player_number']))
            print('\tPlayer Strategy:', player_info['player_strategy'])
            print('\tTotal Number of Wins:', player_info['number_of_total_wins'])
            print('\tWin Percentage:', player_info['win_percentage'])
            print('\tAverage Score:', player_info['average_score'])
            print('\tMinimum Score:', player_info['min_score'])
            print('\tMaximum Score:', player_info['max_score'])
    return players_info


def plot_hist(player_info):
    pyplot.hist(player_info['list_of_player_scores'], 25)
    pyplot.title('Player {} Scores'.format(player_info['player_number']))
    pyplot.show()


if __name__ == '__main__':
    start_time = time.time()
    players_info = run_multiple_games(100,[2,2,3,3],print_info=True)
    for player_info in players_info:
        print (player_info)
    plot_hist(players_info[0])
    print('Run Time: {} Seconds'.format(time.time() - start_time))
