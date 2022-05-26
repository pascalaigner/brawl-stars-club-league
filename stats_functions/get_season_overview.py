import pandas as pd

def get_season_overview(club_members_df, club_league_games_df, season, event_day):
    club_members_df_filtered = club_members_df.query(f'season == "{season}"')
    if event_day == 'all':
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}"')
    else:
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}" & \
                                                                     event_day == "{event_day}"')
    
    season_overview_dict = {member['player_name'] : [0, 0, member['trophies']]
                            for member_index, member in club_members_df_filtered.iterrows()}

    for game_index, game in club_league_games_df_filtered.iterrows():
        for n in range(1, 7):
            if game[f'player{n}_is_club_member']:
                season_overview_dict[game[f'player{n}_name']][0] += game['trophy_change']
                season_overview_dict[game[f'player{n}_name']][1] += 2 if game['game_type'] == 'teamRanked' else 1

    season_overview_df = pd.DataFrame(
        {
            'Player' : season_overview_dict.keys(),
            'Club trophies' : [season_overview_dict[player][0] for player in season_overview_dict],
            'Tickets used' : [season_overview_dict[player][1] for player in season_overview_dict],
            'Trophies' : [season_overview_dict[player][2] for player in season_overview_dict],
        },
    )
    season_overview_df_sorted = season_overview_df.sort_values(['Club trophies', 'Trophies'], ascending=False)

    return season_overview_df_sorted[['Player', 'Club trophies', 'Tickets used']]
