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
        html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
    ]

    row1 = html.Tr([html.Td(html.Img(src=app.get_asset_url('brawler_images/Shelly_Skin-Default.webp'), height='50px'),), html.Td(html.Img(src=app.get_asset_url('brawler_images/Amber_Skin-Default.webp'), width='50px'),)])
    row2 = html.Tr([html.Td([html.Img(src=app.get_asset_url('brawler_images/Jessie_Skin-Default.webp'), height='50px'),html.Img(src=app.get_asset_url('brawler_images/Shelly_Skin-Default.webp'), height='50px')]), html.Td(html.Img(src=app.get_asset_url('brawler_images/Amber_Skin-Default.webp'), width='30px'),)])
    row3 = html.Tr([html.Td([html.Img(src=app.get_asset_url('brawler_images/Rosa_Skin-Default.webp'), height='50px'),html.Img(src=app.get_asset_url('brawler_images/Shelly_Skin-Default.webp'), height='50px')]), html.Td(html.Img(src=app.get_asset_url('brawler_images/Amber_Skin-Default.webp'), width='30px'),)])

    table_body = [html.Tbody([row1, row2, row3])]

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
                                html.H5('Win Rates (coming soon...)'),
                                html.Span('aegiman'),
                                html.Img(src=app.get_asset_url('brawler_images/Shelly_Skin-Default.webp'), width='30px'),
                                table,
                            ]
                        ),
                        dbc.Col([html.H5('More fancy stuff...')]),
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
