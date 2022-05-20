from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from decouple import config
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from stats_functions.get_season_overview import get_season_overview

URI=config('URI')

BS = 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css'
app = Dash(__name__, external_stylesheets=[BS])
app.title = 'Brawl Attack'
server = app.server

def calculate_progress_bar_value(progress):
    return int(progress.split('/')[0]) / int(progress.split('/')[1])*100

def serve_layout():
    
    engine = create_engine(URI, poolclass=NullPool)
    with engine.connect() as connection:
        club_members_df = pd.read_sql('club_members', connection)
        club_league_games_df = pd.read_sql('club_league_games', connection)
        # job_log_df = pd.read_sql('job_log', connection)

    seasons = [{'label' : season, 'value': season} for season in club_members_df['season'].unique()]
    season_overview_df, total_club_trophies, total_tickets_used = get_season_overview(club_members_df, club_league_games_df, seasons[0]['value'], 'all')

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
                        ') Club League Stats',
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5('Seasons Overview'),
                                html.Span('Season', className='selector_label'),
                                dbc.Label(
                                    id='season_selector',
                                    options=seasons,
                                    value=seasons[0]['value'],
                                ),
                                dbc.Label('Event day', className='selector_label'),
                                dbc.Select(
                                    id='event_day_selector',
                                    options=[
                                        {'label' : 'All', 'value' : 'all'},
                                        {'label' : 'Event day 1', 'value' : '1'},
                                        {'label' : 'Event day 2', 'value' : '2'},
                                        {'label' : 'Event day 3', 'value' : '3'},
                                    ],
                                    value='all',
                                ),
                                html.Div(style={'height' : '15px'}),
                                dbc.Label('Total club trophies'),
                                dbc.Progress(
                                    id='total_club_trophies_progress_bar',
                                    label=total_club_trophies,
                                    value=calculate_progress_bar_value(total_club_trophies),
                                ),
                                html.Div(style={'height' : '15px'}),
                                dbc.Label('Total tickets used'),
                                dbc.Progress(
                                    id='total_tickets_used_progress_bar',
                                    label=total_tickets_used,
                                    value=calculate_progress_bar_value(total_tickets_used),
                                ),
                                html.Div(style={'height' : '15px'}),
                                html.Div(
                                    dbc.Table.from_dataframe(season_overview_df),
                                    id='season_overview_table',
                                ),
                            ],
                        ),
                        dbc.Col([html.H5('Win Rates (coming soon...)')]),
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

@app.callback(
    Output(component_id='total_club_trophies_progress_bar', component_property='label'),
    Output(component_id='total_club_trophies_progress_bar', component_property='value'),
    Output(component_id='total_tickets_used_progress_bar', component_property='label'),
    Output(component_id='total_tickets_used_progress_bar', component_property='value'),
    Output(component_id='season_overview_table', component_property='children'),
    Input(component_id='season_selector', component_property='value'),
    Input(component_id='event_day_selector', component_property='value'),
    Input(component_id='club_members_df_memory', component_property='data'),
    Input(component_id='club_league_games_df_memory', component_property='data'),
)
def render_season_overview(selected_season, selected_event_day, club_members_df, club_league_games_df):
    season_overview_df, total_club_trophies, total_tickets_used = get_season_overview(pd.DataFrame.from_dict(club_members_df), pd.DataFrame.from_dict(club_league_games_df), selected_season, selected_event_day)
    return (
        total_club_trophies,
        calculate_progress_bar_value(total_club_trophies),
        total_tickets_used,
        calculate_progress_bar_value(total_tickets_used),
        dbc.Table.from_dataframe(season_overview_df)
    )

if __name__ == '__main__':
    app.run_server(debug=False)
