from decouple import config
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

URI=config('URI')

engine = create_engine(URI, poolclass=NullPool)
with engine.connect() as connection:
    club_league_games_df = pd.read_sql('club_league_games', connection)


def get_season_overview(club_league_games_df, season, event_day):
    if event_day == 'all':
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}"')
    else:
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}" & event_day == "{event_day}"')
    
    season_overview_dict = {}
    for row_index, row in club_league_games_df_filtered.iterrows():
        for n in range(1, 7):
            if row[f'player{n}_is_club_member'] == True:
                if row[f'player{n}_name'] not in season_overview_dict.keys():
                    season_overview_dict[row[f'player{n}_name']] = [row['trophy_change'], 2]
                else:
                    season_overview_dict[row[f'player{n}_name']][0] += row['trophy_change']
                    season_overview_dict[row[f'player{n}_name']][1] += 2

    season_overview_df = pd.DataFrame(
        {
            'player' : season_overview_dict.keys(),
            'club_trophies' : [season_overview_dict[player][0] for player in season_overview_dict],
            'tickets_used' : [season_overview_dict[player][1] for player in season_overview_dict],
        },
    )
    
    return season_overview_df

print(get_season_overview(club_league_games_df, "2022-19", "3"))
