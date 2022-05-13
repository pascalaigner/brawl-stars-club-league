from decouple import config
import os
import requests
import pandas as pd
import sqlalchemy as db

FIXIE_URL=config('FIXIE_URL')
API_TOKEN=config('API_TOKEN')
URI=config('URI')

club_tag = '#2YPY9LVV9'
proxies = {
    # https://devcenter.heroku.com/articles/fixie
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
        'player_tag'  : [club_members_list[i]['tag']  for i in range(len(club_members_list))],
        'player_name' : [club_members_list[i]['name'] for i in range(len(club_members_list))],
    },
)

# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
engine = db.create_engine(URI)
connection = engine.connect()
metadata = db.MetaData()
club_members_table = db.Table('club_members', metadata, autoload=True, autoload_with=engine)

connection.execute('TRUNCATE TABLE club_members')
query = db.insert(club_members_table)
connection.execute(query, club_members_df.to_dict('records'))

# https://stackoverflow.com/questions/21738944/how-to-close-a-sqlalchemy-session
connection.close()
engine.dispose()

print("Script run successfully")
