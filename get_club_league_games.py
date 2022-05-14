from decouple import config
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import json

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

club_league_games_timestamps = []
club_league_games_jsons = []

for member in club_members_list:

    response = requests.get(
        # the hashtag '#' is encoded as '%23' in the URL
        f'https://api.brawlstars.com/v1/players/%23{member[1:]}/battlelog',
        proxies=proxies,
        headers=headers,
    )
    battlelog = response.json()['items']

    for entry in battlelog:
        # not all entries have the key 'trophyChange', therefore the exception handling
        try:
            # identify if the entry is a club league game
            if entry['battle']['type'] == 'teamRanked' and entry['battle']['trophyChange'] in [3, 5, 7, 9]:
                # only add the club league game if it has not been already added
                # up to 3 members can have the same entry in their battlelog if they played a club league game together
                if entry['battleTime'] not in club_league_games_timestamps and entry['battleTime'] not in club_league_games_history_list:
                    club_league_games_timestamps.append(entry['battleTime'])
                    club_league_games_jsons.append(json.dumps(entry))
        except:
            continue

club_league_games_new_df = pd.DataFrame(
    {
        'game_timestamp'  : club_league_games_timestamps,
        'game_json' : club_league_games_jsons,
    },
)

with engine.connect() as connection:
    club_league_games_new_df.to_sql('club_league_games', connection, if_exists='append', index=False)

print("get_club_league_games.py executed successfully")
