import requests
from datetime import datetime
import pytz

URL_DEVMAN = 'https://devman.org/api/challenges/solution_attempts/'
TIME_START = '00:00:00'
TIME_END = '05:00:00'


def time_decoder(timestamp, timezone):
    timezone = pytz.timezone(timezone)
    time = datetime.fromtimestamp(timestamp, timezone)
    return time.strftime("%H:%M:%S")


def load_attempts():
    pages = 1
    response = requests.get(URL_DEVMAN, params={'page': pages})
    while response.status_code == requests.codes.ok:
        for item in response.json()['records']:
            yield {
                'username': item['username'],
                'timestamp': item['timestamp'],
                'timezone': item['timezone'],
            }
        pages += 1
        response = requests.get(URL_DEVMAN, params={'page': pages})


def check_time(item):
    item_time = time_decoder(item['timestamp'], item['timezone'])
    if TIME_START < item_time <= TIME_END:
        return True
    else:
        return False


def get_midnighters():
    midnighters = set()
    for item in load_attempts():
        if item['timestamp'] is not None:
            if check_time(item):
                midnighters.add(item['username'])
    return midnighters

if __name__ == '__main__':
    for user in get_midnighters():
        print(user)
