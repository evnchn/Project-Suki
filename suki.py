import requests
from pprint import pprint

def get_unavail_dishes():

    url = 'https://aigensstoreapp.appspot.com/api/v1/menu/store/102829.json'

    response = requests.get(url)

    all_dishes = []

    unavailable_dishes_name = []

    if response.status_code == 200:
        data = response.json()
        # do something with the JSON data here
        for eachgroup in data['data']['menu']['groups']:
            all_dishes += eachgroup['items']
        for each_dish in all_dishes:
            if each_dish['inventory'] == 0:
                unavailable_dishes_name.append(each_dish['printName'])
        unavailable_dishes_name = list(set(unavailable_dishes_name))
        unavailable_dishes_name.sort()
        return unavailable_dishes_name
    else:
        raise Exception("Status code {}".format(response.status_code))
