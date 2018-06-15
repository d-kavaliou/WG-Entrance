import configparser
import os

from algoritm.generate_pairs import generate_pairs, TeamRating


def fetch_team_ratings(path_to_users_ds, path_to_teams_ds):
    players = {}
    with open(path_to_users_ds) as user_ds:
        for player_line in user_ds:
            player_id, player_score = player_line.split(' ')
            players[player_id] = player_score

    teams = []
    with open(path_to_teams_ds) as teams_ds:
        for team in teams_ds:
            team_id, *team_players = team.rstrip().split(' ')
            teams.append(TeamRating(int(team_id),
                                    sum(int(players[player_id]) for player_id in team_players)))
    return teams


def dump_pairs(pairs_list, output_folder, test_name):
    with open(os.path.join(output_folder, '{}_pairs.txt'.format(test_name)), 'w+') as dump_file:
        dump_file.write('\n'.join(map(lambda pair: '{} {}'.format(pair[0].id, pair[1].id), pairs_list)))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    root_folder_path = config.get('sources', 'Folder')
    output_folder_path = config.get('sources', 'OutputFolder')

    # create the output folder if doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # process all test files
    for folder in os.listdir(root_folder_path):
        if folder != '.' and 'test_' in folder:
            # upload team ratings
            ratings = fetch_team_ratings(
                os.path.join(root_folder_path, folder, config.get('sources', 'UsersFileName')),
                os.path.join(root_folder_path, folder, config.get('sources', 'TeamsFileName')))

            pairs = list(generate_pairs(ratings, key=lambda team: team.rating))

            dump_pairs(pairs, output_folder_path, folder)