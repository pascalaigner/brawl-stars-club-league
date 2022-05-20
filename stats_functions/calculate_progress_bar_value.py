def calculate_progress_bar_value(progress_str):
    return int(progress_str.split('/')[0]) / int(progress_str.split('/')[1])*100
