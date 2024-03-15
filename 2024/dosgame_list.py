import json
import os
import inspect
import urllib.request, urllib.parse
import requests

root = os.path.abspath('.')

# print(root)

PREFIX = 'https://dos-bin.zczc.cz/'
DESTINATION_DIR = os.path.join(root, 'bin')
print(DESTINATION_DIR)
BUF_SIZE = 65536
THREAD_SIZE = 10

with open(os.path.join(root, 'games_all.json'), encoding='utf-8') as f:
    game_infos = json.load(f)
    # print(game_infos)

with open(os.path.join(root, 'gamesList.txt'), 'w', encoding='utf-8') as e:
    for value in game_infos['games'].keys():
        file = value + '.zip'
        print(file)
        absolute_path = DESTINATION_DIR + '\\' + file
        print(absolute_path)
        url = PREFIX + file
        e.write(url + '\n')
