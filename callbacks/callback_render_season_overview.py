from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from stats_functions.calculate_progress_bar_value import calculate_progress_bar_value
from stats_functions.get_season_overview import get_season_overview
from stats_functions.get_total_club_trophies import get_total_club_trophies
from stats_functions.get_total_tickets_used import get_total_tickets_used

def callback_render_season_overview(app):
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
        season_overview_df = get_season_overview(
            pd.DataFrame.from_dict(club_members_df),
            pd.DataFrame.from_dict(club_league_games_df),
            selected_season,
            selected_event_day
        )
        total_club_trophies = get_total_club_trophies(season_overview_df, selected_event_day)
        total_tickets_used = get_total_tickets_used(season_overview_df, selected_event_day)
        return (
            total_club_trophies,
            calculate_progress_bar_value(total_club_trophies),
            total_tickets_used,
            calculate_progress_bar_value(total_tickets_used),
            dbc.Table.from_dataframe(season_overview_df)
        )
