from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

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

player_first_name = input("Enter the player's first name: ")
player_last_name = input("Enter the player's last name: ")
player_team = input("Enter the player's team's name: ")
context_measure_simple = 'FGA'
season_nullable = input("Enter the season: ")
season_type_all_start = input("Enter the season type: ")

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

player_data.to_csv('data.csv', index=False)


# player_makes = player_data.loc[player_data['SHOT_MADE_FLAG'] == 1]
# player_misses = player_data.loc[player_data['SHOT_MADE_FLAG'] == 0]
#
# mpl.rcParams['font.family'] = 'Avenir'
# mpl.rcParams['font.size'] = 18
# mpl.rcParams['axes.linewidth'] = 2
#
# fig = plt.figure(figsize=(4, 3.76))
# ax = fig.add_axes([0, 0, 1, 1])
#
# ax = create_court(ax, 'black')
#
# ax.plot(player_misses['LOC_X'], player_misses['LOC_Y'] + 60, 'ro')
# ax.plot(player_makes['LOC_X'], player_makes['LOC_Y'] + 60, 'go')
#
#
# ax.text(0, 1.05, note, transform=ax.transAxes, ha = 'left', va = 'baseline')
#
# plt.savefig(filename, dpi=300, bbox_inches='tight')
# plt.show()