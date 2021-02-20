from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *
# from tkinter import *
# root = Tk()
#
# a = StringVar()
# a.set("default")
#
# oc = StringVar(root)
# oc.set("Select")
#
# def function(x):
#
#   if x == "yes":
#       a.set("hello")
#       print(a.get())
#
#   else:
#       a.set("bye")
#       print(a.get())
#
# o = OptionMenu(root, oc, "yes", "no", command=function)
# o.pack()
#
#
# z = a.get()
# print(z)
#
# root.mainloop()

players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
def split_string(location):
    index = -1
    for i in range(len(location)):
        if location[i] == ' ':
            index = i
    return location[:index], location[index+1:]


def compute_league_averages(zone,x):
    area = zone[0]
    # print("The area is " + area)
    dict = {'(R)': 'Right Side(R)', '(C)': 'Center(C)', '(L)': 'Left Side(L)', '(RC)': 'Right Side Center(RC)',
            '(LC)': 'Left Side Center(LC)'}
    side = dict[zone[1]]

    # print("The side is " + side)
    total_makes = 0
    total_shots = 0
    for player in players[x:x+1]:
        # print(player[''])
        team_id = player['teamId']
        player_id = player['playerId']
        context_measure_simple = 'FGA'
        season_nullable = '2020-21'
        season_type_all_start = 'Regular Season'
        # print("TEAM ID: " + str(team_id))
        # print("PLAYER ID: " + str(player_id))
        # print("CONTEXT MEASURE SIMPLE: " + context_measure_simple)
        # print("SEASON NUMBER: " + season_nullable)
        # print("SEASON TYPE: " + season_type_all_start)
        player_shot_json = shotchartdetail.ShotChartDetail(
            team_id=team_id,
            player_id=player_id,
            context_measure_simple=context_measure_simple,
            season_nullable=season_nullable,
            season_type_all_star=season_type_all_start)
        player_shot_data = json.loads(player_shot_json.get_json())
        player_relevant_data = player_shot_data['resultSets'][0]
        headers = player_relevant_data['headers']
        rows = player_relevant_data['rowSet']

        player_data = pd.DataFrame(rows)
        # print(player_data.head())
        # print(player_data.columns)
        if(player_data.shape[0] != 0):
            player_data.columns = headers
            # print(player_data.head())
            # print(player_data.columns)
            #player_data.to_csv('lameloballbefore.csv', index=False)
            player_data = player_data.loc[(player_data['SHOT_ZONE_BASIC'] == area) & (player_data['SHOT_ZONE_AREA'] == side)]
            #player_data.to_csv('lameloball.csv', index=False)
            total_shots += player_data.shape[0]
            total_makes += player_data["SHOT_MADE_FLAG"].sum()

    file = open('leftcorner3.txt', 'a')
    res = str(total_makes) + ' ' + str(total_shots) + '\n'
    file.write(res)
    file.close()

    # return total_makes, total_shots

def driver(zone):
    made_shots = 0
    total_shots = 0
    for i in range(0, 100):
        block = compute_league_averages(zone, 5 * i)
        made_shots += block[0]
        total_shots += block[1]

    return made_shots, total_shots, made_shots / total_shots

location1 = "Right Corner 3 (R)"
location2 = "Left Corner 3 (L)"
location3 = "Mid-range (L)"
location4 = "Mid-range (C)"
location5 = "Mid-range (R)"
location6 = "Mid-range (RC)"

zone1 = split_string(location1)
zone2 = split_string(location2)
zone3 = split_string(location3)
zone4 = split_string(location4)
zone5 = split_string(location5)
zone6 = split_string(location6)
start = sys.argv[1]
print(compute_league_averages(zone2, int(start)))
# print(driver(zone))
# def driver(zone):
#     made_shots = 0
#     total_shots = 0
#     for i in range(0,100):
#         block = compute_league_averages(zone, 5*i)
#         made_shots+=block[0]
#         total_shots+=block[1]
#
#     return made_shots, total_shots, made_shots/total_shots
