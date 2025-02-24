from datetime import datetime, timedelta
import pytz

def get_formatted_date():
    pacific_tz = pytz.timezone('US/Pacific')

    now_pacific = datetime.now(pacific_tz) + timedelta(days=1)

    day_suffix = get_day_suffix(now_pacific.day)

    formatted_date = now_pacific.strftime(f"%A, %B {now_pacific.day}{day_suffix}, %I:%M%p Pacific Time")

    return formatted_date

def get_day_suffix(day):
    if 11 <= day <= 13:
        return "th"
    
    last_digit = day % 10

    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    else:
        return "th"
    

def replace_time(text):
    formated_time = get_formatted_date()
    return text.replace("{time}", formated_time)