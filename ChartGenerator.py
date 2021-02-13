from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
# print(teams)
# print(players)
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
# def find_lebron():
#     bin = []
#     for player in players:
#         if player['lastName'] == 'James' or player['firstName'] == 'James':
#             bin.append(player)
#     return bin

shot_json = shotchartdetail.ShotChartDetail(
    team_id = get_team_id('Golden State Warriors'),
    player_id = get_player_id('Stephen', 'Curry'),
    context_measure_simple = 'FGA',
    season_nullable = '2015-16',
    season_type_all_star = 'Regular Season')

# print(get_team_id('New York Knicks'))
# print(find_lebron())
# print(get_player_id('LeBron', 'James'))

shot_data = json.loads(shot_json.get_json())
relevant_data = shot_data['resultSets'][0]

headers = relevant_data['headers']
rows = relevant_data['rowSet']

curry_data = pd.DataFrame(rows)
curry_data.columns = headers
# print(curry_data.columns)

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


mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])

ax = create_court(ax, 'black')
ax.hexbin(curry_data['LOC_X'], curry_data['LOC_Y'] + 60, gridsize=(30,30), extent=(-300,300,0,940), bins = 'log', cmap='Blues')

ax.text(0,1.05, 'Stephen Curry\n2015-2016 Regular Season', transform=ax.transAxes, ha = 'left', va = 'baseline')

plt.savefig('ShotCart_FGA_StephCurry_15-16.png', dpi=300, bbox_inches='tight')
plt.show()

