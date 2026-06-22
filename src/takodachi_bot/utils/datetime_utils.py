from datetime import datetime
import pytz

def format_datetime_by_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def count_difference_by_timestamp(timestamp):
    time_difference = datetime.now() - datetime.fromtimestamp(timestamp)

    days, seconds = divmod(time_difference.total_seconds(), 86400)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}:{int(minutes)}:{int(seconds)}"

def format_hk_datetime_by_string(date_string, format):
    
    date_time = datetime.strptime(date_string, format)
    hk_timezone = pytz.timezone('Asia/Hong_Kong')

    print(date_time)

    if date_time.tzinfo is None:
        date_time = hk_timezone.localize(date_time)
    elif date_time.tzinfo == pytz.utc:
        date_time = date_time.replace(tzinfo=pytz.utc).astimezone(hk_timezone)

    print(date_time)
    return date_time