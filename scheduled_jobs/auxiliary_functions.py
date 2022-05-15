from datetime import datetime

# club league event days start on Wednesday, Friday and Sunday on 14:00 UTC each week (season)

def get_season(date_str):
    date = datetime.strptime(date_str, '%Y%m%dT%H%M%S.%f%z')
    if date.weekday() in [*range(2, 7)]:
        return f'{date.year}-{date.isocalendar().week}'
    elif date.weekday() == 0:
        return f'{date.year}-{date.isocalendar().week-1}'
    else:
        raise ValueError('Date is no event day.')

def get_event_day(date_str):
    date = datetime.strptime(date_str, '%Y%m%dT%H%M%S.%f%z')
    if date.weekday() in [2, 3]:
        return '1'
    elif date.weekday() in [4, 5]:
        return '2'
    elif date.weekday() in [6, 0]:
        return '3'
    else:
        raise ValueError('Date is no event day.')
