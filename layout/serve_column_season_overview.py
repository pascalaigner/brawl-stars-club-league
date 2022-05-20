from dash import html
import dash_bootstrap_components as dbc

from stats_functions.calculate_progress_bar_value import calculate_progress_bar_value
from stats_functions.get_season_overview import get_season_overview
from stats_functions.get_total_club_trophies import get_total_club_trophies
from stats_functions.get_total_tickets_used import get_total_tickets_used

def serve_column_season_overview(club_members_df, club_league_games_df):
    seasons = [{'label' : season, 'value': season} for season in club_members_df['season'].unique()]
    season_overview_df = get_season_overview(club_members_df, club_league_games_df, seasons[0]['value'], 'all')
    total_club_trophies = get_total_club_trophies(season_overview_df, 'all')
    total_tickets_used = get_total_tickets_used(season_overview_df, 'all')
    return (
        dbc.Col(
            [
                html.H5('Seasons Overview'),
                html.Div(
                    [
                        dbc.Label('Season', class_name='selector_label'),
                        dbc.Select(
                            id='season_selector',
                            class_name='selector',
                            options=seasons,
                            value=seasons[0]['value'],
                        ),
                    ],
                ),
                html.Div(
                    [
                        dbc.Label('Event day', class_name='selector_label'),
                        dbc.Select(
                            id='event_day_selector',
                            class_name='selector',
                            options=[
                                {'label' : 'All', 'value' : 'all'},
                                {'label' : 'Event day 1', 'value' : '1'},
                                {'label' : 'Event day 2', 'value' : '2'},
                                {'label' : 'Event day 3', 'value' : '3'},
                            ],
                            value='all',
                        ),
                    ],
                ),
                html.Div(style={'height' : '15px'}),
                dbc.Label('Total club trophies'),
                dbc.Progress(
                    id='total_club_trophies_progress_bar',
                    label=total_club_trophies,
                    value=calculate_progress_bar_value(total_club_trophies),
                ),
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
        )
    )
