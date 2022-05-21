from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from decouple import config
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from callbacks.callback_render_season_overview import callback_render_season_overview
from layout.serve_column_season_overview import serve_column_season_overview

URI=config('URI')

BS = 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css'
app = Dash(
    __name__,
    external_stylesheets=[BS],
    meta_tags=[
        {
            'name' : 'viewport',
            'content' : 'width=device-width, initial-scale=1',
        },
    ],
)
app.title = 'Brawl Attack'
server = app.server

def serve_layout():
    
    engine = create_engine(URI, poolclass=NullPool)
    with engine.connect() as connection:
        club_members_df = pd.read_sql('club_members', connection)
        club_league_games_df = pd.read_sql('club_league_games', connection)
        # job_log_df = pd.read_sql('job_log', connection)


    table_header = [
        html.Thead(html.Tr(
            [
                html.Th("Season"),
                html.Th("Event day"),
                html.Th("Result"),
                html.Th("Mode"),
                html.Th("Club team names"),
                html.Th("Club team brawlers"),
                html.Th("Opponents brawlers"),
            ]
        ))
    ]

    rows = []

    for game_index, game in club_league_games_df.sort_values('game_timestamp', ascending=False).iterrows():

        team1_names = []
        team1_brawlers = []
        team1_are_club_members = False
        team2_names = []
        team2_brawlers = []

        for n in range(1, 4):
            team1_names.append(game[f'player{n}_name'])
            team1_brawlers.append(game[f'player{n}_brawler'])
            if game[f'player{n}_is_club_member']:
                team1_are_club_members = True
        
        for n in range(4, 7):
            team2_names.append(game[f'player{n}_name'])
            team2_brawlers.append(game[f'player{n}_brawler'])

        if team1_are_club_members:
            club_team_names = team1_names
            club_team_brawlers = team1_brawlers
            opponents_brawlers = team2_brawlers
        else:
            club_team_names = team2_names
            club_team_brawlers = team2_brawlers
            opponents_brawlers = team1_brawlers


        rows.append(
            html.Tr(
                [
                    html.Td(game['season']),
                    html.Td(game['event_day']),
                    html.Td(game['result'], style={'color' : f'{"green" if game["result"] == "victory" else "red"}'}),
                    html.Td(
                        html.Img(src=app.get_asset_url(f'modes/{game["mode"]}.webp'), height='30px'),
                    ),
                    html.Td(
                        [
                            html.Div(club_team_names[0]),
                            html.Div(club_team_names[1]),
                            html.Div(club_team_names[2]),
                        ], 
                    ),
                    html.Td(
                        [
                            html.Img(src=app.get_asset_url(f'brawler_icons/{club_team_brawlers[0]}.webp'), height='30px'),
                            html.Img(src=app.get_asset_url(f'brawler_icons/{club_team_brawlers[1]}.webp'), height='30px'),
                            html.Img(src=app.get_asset_url(f'brawler_icons/{club_team_brawlers[2]}.webp'), height='30px'),
                        ], 
                    ),
                    html.Td(
                        [
                            html.Img(src=app.get_asset_url(f'brawler_icons/{opponents_brawlers[0]}.webp'), height='30px'),
                            html.Img(src=app.get_asset_url(f'brawler_icons/{opponents_brawlers[1]}.webp'), height='30px'),
                            html.Img(src=app.get_asset_url(f'brawler_icons/{opponents_brawlers[2]}.webp'), height='30px'),
                        ], 
                    ),
                ],
            )
        )

    table_body = [html.Tbody(rows)]

    table = dbc.Table(table_header + table_body, bordered=True)


    return (
        dbc.Container(
            [
                html.H1(
                    [
                        'Brawl Attack (',
                        html.A(
                            '#2YPY9LVV9',
                            href='https://brawlify.com/stats/club/2YPY9LVV9',
                            target='_blank',
                        ),
                        ')',
                    ],
                ),
                dbc.Row(
                    [
                        serve_column_season_overview(
                            club_members_df,
                            club_league_games_df,
                        ),
                        dbc.Col(
                            [
                                html.H5('Matchups'),
                                table,
                            ],
                            width=8,
                        ),
                    ],
                ),
                dcc.Store(
                    id='club_members_df_memory',
                    data=club_members_df.to_dict(),
                ),
                dcc.Store(
                    id='club_league_games_df_memory',
                    data=club_league_games_df.to_dict(),
                ),
                # dcc.Store(
                #     id='job_log_df_memory',
                #     data=job_log_df.to_dict(),
                # ),
            ],
            fluid=True,
        )
    )

app.layout = serve_layout

callback_render_season_overview(app)

if __name__ == '__main__':
    app.run_server(debug=True)
