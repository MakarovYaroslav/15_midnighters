from datetime import datetime
import pytz
import requests


def request_to_devman(page_number):
    parameters = {"page": page_number}
    returned_data = requests.get(
        'https://devman.org/api/challenges/solution_attempts/',
        params=parameters
    )
    return returned_data


def load_attempts():
    all_data = []
    first_page = 1
    first_page_data = request_to_devman(first_page)
    pages_count = first_page_data.json()['number_of_pages']
    all_data.append(first_page_data.json()['records'])
    for page in range(first_page, pages_count):
        page_data = request_to_devman(page+1)
        if page_data.status_code == 200:
            all_data.append(page_data.json()['records'])
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
    pages_data = load_attempts()
    print("Совы:")
    for records in pages_data:
        print_midnighters(records)
