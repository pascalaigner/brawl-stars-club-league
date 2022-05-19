import pandas as pd

def get_season_overview(club_members_df, club_league_games_df, season, event_day):
    club_members_df_filtered = club_members_df.query(f'season == "{season}"')
    if event_day == 'all':
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}"')
    else:
        club_league_games_df_filtered = club_league_games_df.query(f'season == "{season}" & event_day == "{event_day}"')

    season_overview_dict = {member['player_name'] : [0, 0, member['trophies']] for member_index, member in club_members_df_filtered.iterrows()}
    for game_index, game in club_league_games_df_filtered.iterrows():
        for n in range(1, 7):
            if game[f'player{n}_is_club_member'] == True:
                season_overview_dict[game[f'player{n}_name']][0] += game['trophy_change']
                season_overview_dict[game[f'player{n}_name']][1] += 2

    season_overview_df = pd.DataFrame(
        {
            'Player' : season_overview_dict.keys(),
            'Club trophies' : [season_overview_dict[player][0] for player in season_overview_dict],
            'Tickets used' : [season_overview_dict[player][1] for player in season_overview_dict],
            'Trophies' : [season_overview_dict[player][2] for player in season_overview_dict],
        },
    )
    season_overview_df_sorted = season_overview_df.sort_values(['Club trophies', 'Trophies'], ascending=False)[['Player', 'Club trophies', 'Tickets used']]

    if event_day == 'all':
        max_club_trophies = 1890
        max_tickets_used = 420
    elif event_day in ['1', '2']:
        max_club_trophies = 540
        max_tickets_used = 120
    else:
        max_club_trophies = 810
        max_tickets_used = 180

    total_club_trophies = season_overview_df_sorted['Club trophies'].sum()
    total_club_trophies_str = f'{total_club_trophies}/{max_club_trophies}'
    total_tickets_used = season_overview_df_sorted['Tickets used'].sum()
    total_tickets_used_str = f'{total_tickets_used}/{max_tickets_used}'

    return season_overview_df_sorted, total_club_trophies_str, total_tickets_used_str
