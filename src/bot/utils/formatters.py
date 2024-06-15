import pytz
from datetime import datetime


def price_formatter(num: int):
    formatted = '{:,}'.format(num).replace(',', '.')

    return formatted


def date_formatter(date: str):
    try:
        original_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        original_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    original_datetime_utc = original_datetime.replace(tzinfo=pytz.UTC)

    # Convert to Asia/Tashkent time zone
    tashkent_timezone = pytz.timezone('Asia/Tashkent')
    converted_datetime = original_datetime_utc.astimezone(tashkent_timezone)

    # Format the converted datetime
    formatted_datetime = converted_datetime.strftime('%Y-%m-%d %H:%M')

    return formatted_datetime