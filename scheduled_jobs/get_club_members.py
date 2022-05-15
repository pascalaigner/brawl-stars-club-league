from decouple import config
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

FIXIE_URL=config('FIXIE_URL')
API_TOKEN=config('API_TOKEN')
URI=config('URI')

club_tag = '#2YPY9LVV9'
proxies = {
    'http'  : os.environ.get('FIXIE_URL', ''),
    'https' : os.environ.get('FIXIE_URL', ''),
}
headers = {
    'Authorization' : f'Bearer {API_TOKEN}',
}
response = requests.get(
    # the hashtag '#' is encoded as '%23' in the URL
    f'https://api.brawlstars.com/v1/clubs/%23{club_tag[1:]}/members',
    proxies=proxies,
    headers=headers,
)

club_members_list = response.json()['items']
club_members_df = pd.DataFrame(
    {
        'player_tag'  : [member['tag'] for member in club_members_list],
        'player_name' : [member['name'] for member in club_members_list],
    },
)

engine = create_engine(URI, poolclass=NullPool)
with engine.connect() as connection:
    # the database table should only contain the latest list of members
    # therefore, clear (truncate) the table before inserting the latest list of members
    connection.execute('TRUNCATE TABLE club_members')
    club_members_df.to_sql('club_members', connection, if_exists='append', index=False)

print("get_club_members.py executed successfully")
