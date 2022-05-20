def get_total_club_trophies(season_overview_df, event_day):
    if event_day == 'all':
        max_club_trophies = 1890
    elif event_day in ['1', '2']:
        max_club_trophies = 540
    else:
        max_club_trophies = 810
    total_club_trophies = season_overview_df['Club trophies'].sum()
    return f'{total_club_trophies}/{max_club_trophies}'
