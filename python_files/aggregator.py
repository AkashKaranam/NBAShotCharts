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

    filenames = {('Right Corner 3', 'Right Side(R)') : 'rightcorner3.txt',
                 ('Left Corner 3', 'Left Side(L)') : 'leftcorner3.txt',
                 ('Mid-Range', 'Left Side(L)') : 'midrangeleft.txt',
                 ('Mid-Range', 'Left Side Center(LC)') : 'midrangeleftcenter.txt',
                 ('Mid-Range', 'Center(C)') :'midrangecenter.txt',
                 ('Mid-Range', 'Right Side Center(RC)') : 'midrangerightcenter.txt',
                 ('Mid-Range', 'Right Side(R)'): 'midrangeright.txt',
                 ('Above the Break 3', 'Left Side Center(LC)'): 'abovethebreak3leftcenter.txt',
                 ('Above the Break 3', 'Center(C)') : 'abovethebreak3center.txt',
                 ('Above the Break 3', 'Right Side Center(RC)'): 'abovethebreak3rightcenter.txt',
                 ('Restricted Area', 'Center(C)') : 'restrictedareacenter.txt',
                 ('In The Paint (Non-RA)', 'Right Side(R)') : 'inthepaintright.txt',
                 ('In The Paint (Non-RA)', 'Center(C)') : 'inthepaintcenter.txt',
                 ('In The Paint (Non-RA)', 'Left Side(L)') : 'inthepaintleft.txt'
                 }
    input_list = [area, side]
    filename = filenames[tuple(input_list)]
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

    file = open(filename, 'a')
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



location = ["Right Corner 3 (R)", "Left Corner 3 (L)", "Mid-Range (L)", "Mid-Range (C)",
            "Mid-Range (R)", "Mid-Range (RC)", "Mid-Range (LC)", "Above the Break 3 (LC)",
            "Above the Break 3 (C)", "Above the Break 3 (RC)", "Restricted Area (C)",
            "In The Paint (Non-RA) (R)", "In The Paint (Non-RA) (C)",
            "In The Paint (Non-RA) (L)"]

start = sys.argv[1]
curr_loc = location[int(sys.argv[2])]

print(compute_league_averages(split_string(curr_loc), int(start)))
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
