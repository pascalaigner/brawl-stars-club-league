import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from decouple import config
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from datetime import datetime

URI=config('URI')

BS = 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/yeti/bootstrap.min.css'
app = dash.Dash(__name__, external_stylesheets=[BS])
app.title = 'Brawl Attack Club League'
server = app.server

engine = create_engine(URI, poolclass=NullPool)
with engine.connect() as connection:
    club_league_games_history_df = pd.read_sql('club_league_games', engine)

prettier_timestamps = []
for date_str in club_league_games_history_df['game_timestamp']:
    prettier_timestamps.append(datetime.strptime(date_str, '%Y%m%dT%H%M%S.%f%z'))

players = []
brawlers = []
for i, row in club_league_games_history_df.iterrows():
    players_str = ''
    brawlers_str = ''
    for i in range(1, 7):
        if row[f'player{i}_is_club_member'] == True:
            players_str += row[f'player{i}_name'] + ', '
            brawlers_str += row[f'player{i}_brawler'] + ', '
    players.append(players_str[:-2])
    brawlers.append(brawlers_str[:-2])

club_league_games_summary = pd.DataFrame(
    {
        'Timestamp'  : prettier_timestamps,
        'Season'  : club_league_games_history_df['season'],
        'Event day' : club_league_games_history_df['event_day'],
        'Mode' : club_league_games_history_df['mode'],
        'Map' : club_league_games_history_df['map'],
        'Result' : club_league_games_history_df['result'],
        'Trophies' : club_league_games_history_df['trophy_change'],
        'Players' : players,
        'Brawlers' : brawlers,
    },
)
club_league_games_summary.sort_values('Timestamp', ascending=False, inplace=True)

app.layout = dbc.Container(
    [
        html.H1('Brawl Attack Club League - Recent Games'),
        dbc.Table.from_dataframe(club_league_games_summary, striped=True),
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=False)
