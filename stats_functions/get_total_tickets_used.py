def get_total_tickets_used(season_overview_df, event_day):
    if event_day == 'all':
        max_tickets_used = 420
    elif event_day in ['1', '2']:
        max_tickets_used = 120
    else:
        max_tickets_used = 180
    total_tickets_used = season_overview_df['Tickets used'].sum()
    return f'{total_tickets_used}/{max_tickets_used}'
