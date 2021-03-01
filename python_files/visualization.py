from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
print(type(players))
def read_data(filename):
    made = []
    total = []
    file = open(filename, 'r')
    for i in range(0,501):
        str = file.readline()
        # print(str)
        curr = [int(s) for s in str.split() if s.isdigit()]
        made.append(curr[0])
        total.append(curr[1])
    return made, total

def compute_average(filename):
    made_sum = 0
    total_sum = 0;
    made,total = filename
    for m in made:
        made_sum = made_sum + m
    for t in total:
        total_sum = total_sum + t


def name_to_index(first, last):
    for i in range(len(players)):
        if(players[i]['firstName'] == first and players[i]['lastName'] == last):
            return i

def draw(first, last, filename):
    made, total = read_data(filename)
    i = name_to_index(first,last)
    curr_player_makes = made[i]
    curr_player_total_shots = total[i]


print(read_data('midrangeleft.txt'))
print(name_to_index('Precious', 'Achiuwa'))

