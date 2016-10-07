from datetime import datetime
import pytz
import requests


def get_pages_count():
    parameters = {"page": 1}
    r = requests.get(
        'https://devman.org/api/challenges/solution_attempts/',
        params=parameters
    )
    count = r.json()['number_of_pages']
    return count


def load_attempts(pages_count):
    all_data = []
    for page in range(pages_count):
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
        timestamp = record['timestamp']
        if timestamp is not None:
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
    count_of_pages = get_pages_count()
    pages_data = load_attempts(count_of_pages)
    print("Совы:")
    for records in pages_data:
        print_midnighters(records)
