from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from tkinter import *


teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
# print(players)
def list_first_names():
    first_names = set()
    for player in players:
        first_names.add(player['firstName'])
    first_names_list = list(first_names)
    first_names_list.sort()
    return first_names_list

def list_last_names():
    last_names = set()
    for player in players:
        last_names.add(player['lastName'])
    last_names_list = list(last_names)
    last_names_list.sort()
    return last_names_list

def list_team_abrevs():
    team_abrevs = []
    for team in teams:
        team_abrevs.append(team['abbreviation'])
    return team_abrevs

def list_season_numbers():
    seasons = []
    seasons.append('2016-17')
    seasons.append('2017-18')
    seasons.append('2018-19')
    seasons.append('2019-20')
    seasons.append('2020-21')
    return seasons

def list_season_types():
    types = []
    types.append('Regular Season')
    types.append('Playoffs')
    return types

def get_team_id(teamName):
    for team in teams:
        if team['teamName'] == teamName:
            return team['teamId']
    return -1

def get_player_id(first,last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1

def get_player_team(first,last):
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            team_id = player['teamId']
            for team in teams:
                if team_id == team['teamId']:
                    return team['teamName']
    return 'Nonexistent team'

def get_team_name(teamAbr):
    for team in teams:
        if(team['abbreviation'] == teamAbr):
            return team['teamName']
    return 'Nonexistent team'

def user_interface():
    root = Tk()
    root.title("Dropdown Menu for NBA Shot Chart")
    root.geometry("400x400")

    # first name block
    firstname_T = Text(root, height=2, width=30)
    firstname_T.pack()
    firstname_T.insert(END, "Choose Player's First Name")

    first_name_list = list_first_names()
    first_name_choice = StringVar()
    first_name_choice.set(first_name_list[0])
    firstname_drop = OptionMenu(root, first_name_choice, *first_name_list)
    firstname_drop.pack()
    # -----------------------------------------------------------------------------

    # last name block
    lastname_T = Text(root, height=2, width=30)
    lastname_T.pack()
    lastname_T.insert(END, "Choose Player's Last Name")

    last_name_list = list_last_names()
    last_name_choice = StringVar()
    last_name_choice.set(last_name_list[0])
    lastname_drop = OptionMenu(root, last_name_choice, *last_name_list)
    lastname_drop.pack()
    # -----------------------------------------------------------------------------

    # season block
    season_T = Text(root, height=2, width=30)
    season_T.pack()
    season_T.insert(END, "Choose a season")

    season_list = list_season_numbers()
    season_number_choice = StringVar()
    season_number_choice.set(season_list[0])
    season_drop = OptionMenu(root, season_number_choice, *season_list)
    season_drop.pack()
    # -----------------------------------------------------------------------------

    # team name(two cases)
    abbrev_T = Text(root, height=2, width=30)
    abbrev_T.pack()
    abbrev_T.insert(END, "Choose a team abbreviation")

    abbrev_list = list_team_abrevs()
    abbrev_choice = StringVar()
    abbrev_choice.set(abbrev_list[0])
    abbrev_drop = OptionMenu(root, abbrev_choice, *abbrev_list)
    abbrev_drop.pack()
    # -------------------------------------------------------------------------------

    # team type block
    type_T = Text(root, height=2, width=30)
    type_T.pack()
    type_T.insert(END, "Choose a season type")

    type_list = list_season_types()
    type_choice = StringVar()
    type_choice.set(type_list[0])
    type_drop = OptionMenu(root, type_choice, *type_list)
    type_drop.pack()

    exit_button = Button(root, text = "Submit", command = root.quit)
    exit_button.pack(pady=20)

    root.mainloop()

    return first_name_choice.get(), last_name_choice.get(), season_number_choice.get(), abbrev_choice.get(), type_choice.get()



def create_court(ax, color):
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220,220], [0,140], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Arc((0,140), 440, 315, theta1 = 0,
        theta2 = 180, facecolor = 'none', edgecolor=color, lw=2))

    ax.plot([-80,-80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0,190], linewidth=2, color=color)
    ax.plot([60,60], [0,190], linewidth=2, color=color)
    ax.plot([-80,80], [190,190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0,190), 60, facecolor='none', edgecolor=color, lw=2))

    ax.add_artist(mpl.patches.Circle((0,60), 15, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-30,30], [40,40], linewidth=2, color=color)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_xlim(-250,250)
    ax.set_ylim(0, 470)

    return ax


inputs = user_interface()
print(inputs)
player_first_name = inputs[0]
player_last_name = inputs[1]
season_nullable = inputs[2]
player_team = get_team_name(inputs[3])
context_measure_simple = 'FGA'

season_type_all_start = inputs[4]

team_id = get_team_id(player_team)
player_id = get_player_id(player_first_name, player_last_name)
note = player_first_name + " " + player_last_name + "\n" + season_nullable + " " + season_type_all_start
filename = "Images/MakesMisses_" + player_first_name + player_last_name + "_" + season_nullable + ".png"

shot_json = shotchartdetail.ShotChartDetail(
    team_id = team_id,
    player_id = player_id,
    context_measure_simple = context_measure_simple,
    season_nullable = season_nullable,
    season_type_all_star = season_type_all_start)

shot_data = json.loads(shot_json.get_json())
relevant_data = shot_data['resultSets'][0]

headers = relevant_data['headers']
rows = relevant_data['rowSet']

player_data = pd.DataFrame(rows)
player_data.columns = headers

# player_data.to_csv('data.csv', index=False)


player_makes = player_data.loc[player_data['SHOT_MADE_FLAG'] == 1]
player_misses = player_data.loc[player_data['SHOT_MADE_FLAG'] == 0]

mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])

ax = create_court(ax, 'black')

ax.plot(player_misses['LOC_X'], player_misses['LOC_Y'] + 60, 'ro')
ax.plot(player_makes['LOC_X'], player_makes['LOC_Y'] + 60, 'go')


ax.text(0, 1.05, note, transform=ax.transAxes, ha = 'left', va = 'baseline')

plt.savefig(filename, dpi=300, orientation = 'landscape', bbox_inches='tight')
plt.show()