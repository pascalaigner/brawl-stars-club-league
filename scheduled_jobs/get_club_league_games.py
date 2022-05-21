from decouple import config
from datetime import datetime
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from auxiliary_functions import get_season, get_event_day

API_TOKEN=config('API_TOKEN')
FIXIE_URL=config('FIXIE_URL')
URI=config('URI')

date = datetime.utcnow()

if date.weekday() in [3, 5, 0]:

    headers = {
        'Authorization' : f'Bearer {API_TOKEN}',
    }
    proxies = {
        'http'  : os.environ.get('FIXIE_URL', ''),
        'https' : os.environ.get('FIXIE_URL', ''),
    }

    engine = create_engine(URI, poolclass=NullPool)
    with engine.connect() as connection:
        club_members_df = pd.read_sql('club_members', connection)
        club_members_list = club_members_df['player_tag'].to_list()
        club_league_games_df = pd.read_sql('club_league_games', connection)
        club_league_games_list = club_league_games_df['game_timestamp'].to_list()
        
    mode_pool = ['gemGrab', 'heist', 'bounty', 'brawlBall', 'hotZone', 'knockout']

    game_timestamps = []
    seasons = []
    event_days = []
    modes = []
    maps = []
    game_types = []
    results = []
    trophy_changes = []

    players1_tags = []
    players1_names = []
    players1_brawlers = []
    players1_are_club_members = []

    players2_tags = []
    players2_names = []
    players2_brawlers = []
    players2_are_club_members = []

    players3_tags = []
    players3_names = []
    players3_brawlers = []
    players3_are_club_members = []

    players4_tags = []
    players4_names = []
    players4_brawlers = []
    players4_are_club_members = []

    players5_tags = []
    players5_names = []
    players5_brawlers = []
    players5_are_club_members = []

    players6_tags = []
    players6_names = []
    players6_brawlers = []
    players6_are_club_members= []

    for member in club_members_list:

        response = requests.get(
            # the hashtag '#' is encoded as '%23' in the URL
            f'https://api.brawlstars.com/v1/players/%23{member[1:]}/battlelog',
            headers=headers,
            proxies=proxies,
        )
        battlelog = response.json()['items']

        for entry in battlelog:
        
            # identify if the entry is a club league game
            if ('trophyChange' in entry['battle'] and
                    (entry['battle']['type'] == 'teamRanked' and
                     entry['battle']['trophyChange'] in [3, 5, 7, 9] or
                     entry['battle']['type'] == 'ranked' and
                     entry['event']['mode'] in mode_pool and
                     entry['battle']['trophyChange'] in [1, 2, 3, 4])):

                # only add the club league game if it has not been added already
                if (entry['battleTime'] not in game_timestamps and
                        entry['battleTime'] not in club_league_games_list):

                    game_timestamps.append(entry['battleTime'])
                    seasons.append(get_season(entry['battleTime']))
                    event_days.append(get_event_day(entry['battleTime']))
                    modes.append(entry['event']['mode'])
                    maps.append(entry['event']['map'])
                    game_types.append(entry['battle']['type'])
                    results.append(entry['battle']['result'])
                    trophy_changes.append(entry['battle']['trophyChange'])

                    players1_tags.append(entry['battle']['teams'][0][0]['tag'])
                    players1_names.append(entry['battle']['teams'][0][0]['name'])
                    players1_brawlers.append(entry['battle']['teams'][0][0]['brawler']['name'])
                    players1_are_club_members.append(True if players1_tags[-1] in club_members_list else False)

                    players2_tags.append(entry['battle']['teams'][0][1]['tag'])
                    players2_names.append(entry['battle']['teams'][0][1]['name'])
                    players2_brawlers.append(entry['battle']['teams'][0][1]['brawler']['name'])
                    players2_are_club_members.append(True if players2_tags[-1] in club_members_list else False)

                    players3_tags.append(entry['battle']['teams'][0][2]['tag'])
                    players3_names.append(entry['battle']['teams'][0][2]['name'])
                    players3_brawlers.append(entry['battle']['teams'][0][2]['brawler']['name'])
                    players3_are_club_members.append(True if players3_tags[-1] in club_members_list else False)

                    players4_tags.append(entry['battle']['teams'][1][0]['tag'])
                    players4_names.append(entry['battle']['teams'][1][0]['name'])
                    players4_brawlers.append(entry['battle']['teams'][1][0]['brawler']['name'])
                    players4_are_club_members.append(True if players4_tags[-1] in club_members_list else False)

                    players5_tags.append(entry['battle']['teams'][1][1]['tag'])
                    players5_names.append(entry['battle']['teams'][1][1]['name'])
                    players5_brawlers.append(entry['battle']['teams'][1][1]['brawler']['name'])
                    players5_are_club_members.append(True if players5_tags[-1] in club_members_list else False)

                    players6_tags.append(entry['battle']['teams'][1][2]['tag'])
                    players6_names.append(entry['battle']['teams'][1][2]['name'])
                    players6_brawlers.append(entry['battle']['teams'][1][2]['brawler']['name'])
                    players6_are_club_members.append(True if players6_tags[-1] in club_members_list else False)

            else:
                continue

    club_league_games_new_df = pd.DataFrame(
        {
            'game_timestamp' : game_timestamps,
            'season' : seasons,
            'event_day' : event_days,
            'mode' : modes,
            'map' : maps,
            'game_type' : game_types,
            'result' : results,
            'trophy_change' : trophy_changes,

            'player1_tag' : players1_tags,
            'player1_name' : players1_names,
            'player1_brawler' : players1_brawlers,
            'player1_is_club_member' : players1_are_club_members,

            'player2_tag' : players2_tags,
            'player2_name' : players2_names,
            'player2_brawler' : players2_brawlers,
            'player2_is_club_member' : players2_are_club_members,

            'player3_tag' : players3_tags,
            'player3_name' : players3_names,
            'player3_brawler' : players3_brawlers,
            'player3_is_club_member' : players3_are_club_members,

            'player4_tag' : players4_tags,
            'player4_name' : players4_names,
            'player4_brawler' : players4_brawlers,
            'player4_is_club_member' : players4_are_club_members,

            'player5_tag' : players5_tags,
            'player5_name' : players5_names,
            'player5_brawler' : players5_brawlers,
            'player5_is_club_member' : players5_are_club_members,
            
            'player6_tag' : players6_tags,
            'player6_name' : players6_names,
            'player6_brawler' : players6_brawlers,
            'player6_is_club_member' : players6_are_club_members,
        },
    )

    with engine.connect() as connection:
        club_league_games_new_df.to_sql(
            'club_league_games',
            connection,
            if_exists='append',
            index=False
        )
        connection.execute(
            f''' INSERT INTO job_log (job_timestamp, job)
                 VALUES('{date}', 'get_club_league_games.py'); '''
        )

    print('Script get_club_league_games.py executed successfully.')

else:
    print('Today is not Thursday, Saturday or Monday.')
