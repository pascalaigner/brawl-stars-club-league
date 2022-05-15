from decouple import config
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from auxiliary_functions import get_season, get_event_day

FIXIE_URL=config('FIXIE_URL')
API_TOKEN=config('API_TOKEN')
URI=config('URI')

proxies = {
    'http'  : os.environ.get('FIXIE_URL', ''),
    'https' : os.environ.get('FIXIE_URL', ''),
}
headers = {
    'Authorization' : f'Bearer {API_TOKEN}',
}

engine = create_engine(URI, poolclass=NullPool)
with engine.connect() as connection:
    club_members_df = pd.read_sql('club_members', engine, columns=['player_tag'])
    club_members_list = club_members_df['player_tag'].to_list()
    club_league_games_history_df = pd.read_sql('club_league_games', engine, columns=['game_timestamp'])
    club_league_games_history_list = club_league_games_history_df['game_timestamp'].to_list()

timestamps = []
seasons = []
event_days = []
modes = []
maps = []
results = []
trophy_changes = []
player1_tags = []
player1_names = []
player1_brawlers = []
player1_are_club_members = []
player2_tags = []
player2_names = []
player2_brawlers = []
player2_are_club_members = []
player3_tags = []
player3_names = []
player3_brawlers = []
player3_are_club_members = []
player4_tags = []
player4_names = []
player4_brawlers = []
player4_are_club_members = []
player5_tags = []
player5_names = []
player5_brawlers = []
player5_are_club_members = []
player6_tags = []
player6_names = []
player6_brawlers = []
player6_are_club_members= []

for member in club_members_list:

    response = requests.get(
        # the hashtag '#' is encoded as '%23' in the URL
        f'https://api.brawlstars.com/v1/players/%23{member[1:]}/battlelog',
        proxies=proxies,
        headers=headers,
    )
    battlelog = response.json()['items']

    for entry in battlelog:

        # identify if the entry is a club league game
        if 'trophyChange' in entry['battle'] and entry['battle']['type'] == 'teamRanked' and entry['battle']['trophyChange'] in [3, 5, 7, 9]:

            # only add the club league game if it has not been already added
            # up to 3 members can have the same entry in their battlelog if they played a club league game together
            if entry['battleTime'] not in timestamps and entry['battleTime'] not in club_league_games_history_list:

                timestamps.append(entry['battleTime'])
                seasons.append(get_season(entry['battleTime']))
                event_days.append(get_event_day(entry['battleTime']))
                modes.append(entry['event']['mode'])
                maps.append(entry['event']['map'])
                results.append(entry['battle']['result'])
                trophy_changes.append(entry['battle']['trophyChange'])

                player_number = 1
                for i in range(2): # there are 2 teams
                    for j in range(3): # there are 3 players per team
                        exec(f'player{player_number}_tags.append(entry["battle"]["teams"][{i}][{j}]["tag"])')
                        exec(f'player{player_number}_names.append(entry["battle"]["teams"][{i}][{j}]["name"])')
                        exec(f'player{player_number}_brawlers.append(entry["battle"]["teams"][{i}][{j}]["brawler"]["name"])')
                        if entry['battle']['teams'][i][j]['tag'] in club_members_list:
                            exec(f'player{player_number}_are_club_members.append(True)')
                        else:
                            exec(f'player{player_number}_are_club_members.append(False)')
                        player_number += 1

        else:
            continue

club_league_games_new_df = pd.DataFrame(
    {
        'game_timestamp'  : timestamps,
        'season' : seasons,
        'event_day' : event_days,
        'mode' : modes,
        'map' : maps,
        'result' : results,
        'trophy_change' : trophy_changes,
        'player1_tag' : player1_tags,
        'player1_name' : player1_names,
        'player1_brawler' : player1_brawlers,
        'player1_is_club_member' : player1_are_club_members,
        'player2_tag' : player2_tags,
        'player2_name' : player2_names,
        'player2_brawler' : player2_brawlers,
        'player2_is_club_member' : player2_are_club_members,
        'player3_tag' : player3_tags,
        'player3_name' : player3_names,
        'player3_brawler' : player3_brawlers,
        'player3_is_club_member' : player3_are_club_members,
        'player4_tag' : player4_tags,
        'player4_name' : player4_names,
        'player4_brawler' : player4_brawlers,
        'player4_is_club_member' : player4_are_club_members,
        'player5_tag' : player5_tags,
        'player5_name' : player5_names,
        'player5_brawler' : player5_brawlers,
        'player5_is_club_member' : player5_are_club_members,
        'player6_tag' : player6_tags,
        'player6_name' : player6_names,
        'player6_brawler' : player6_brawlers,
        'player6_is_club_member' : player6_are_club_members,
    },
)

with engine.connect() as connection:
    club_league_games_new_df.to_sql('club_league_games', connection, if_exists='append', index=False)

print("get_club_league_games.py executed successfully")
