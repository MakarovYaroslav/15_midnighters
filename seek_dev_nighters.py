from datetime import datetime
import pytz
import requests


def load_attempts():
    pages = 10
    all_data = []
    for page in range(pages):
        parameters = {"page": page+1}
        r = requests.get(
            'https://devman.org/api/challenges/solution_attempts/',
            params=parameters
        )
        if r.status_code == 200:
            all_data.append(r.json()['records'])
    return all_data


def print_midnighters(data):
    max_hour = 5
    for record in data:
        time = datetime.fromtimestamp(record['timestamp'])
        time_according_tz = pytz.timezone(record['timezone']).localize(time)
        if time_according_tz.hour < max_hour:
            print('%s - %s' % (
                record['username'],
                time_according_tz.strftime('%H:%M:%S'))
            )
    return True

if __name__ == '__main__':
    pages_data = []
    pages_data = load_attempts()
    print("Совы:")
    for records in pages_data:
        print_midnighters(records)

