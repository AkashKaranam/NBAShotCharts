from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# load team and player data from nba.com
teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)
# print(teams)
# print(players)


def get_team_id(teamName):
    '''
    Output team id from team name
    :param teamName: string representing a teamName
    :return: nba.com team id for the given teamName or -1 if the teamName is invalid
    '''
    for team in teams:
        if team['teamName'] == teamName:
            return team['teamId']
    return -1

def get_player_id(first,last):
    '''
    Output the player id from their first and last name
    :param first: string representing the first name of the player
    :param last: string representing the last name of the player
    :return: the nba.com player id of the given player name
    '''
    for player in players:
        if player['firstName'] == first and player['lastName'] == last:
            return player['playerId']
    return -1
def create_court(ax, color):
    '''
    Method to draw the court
    :param ax: axis object used to draw the court
    :param color: color of the lines and curves on the court
    :return: an axis object representing the court
    '''

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
# def find_lebron():
#     bin = []
#     for player in players:
#         if player['lastName'] == 'James' or player['firstName'] == 'James':
#             bin.append(player)
#     return bin
player_first_name = input("Enter the player's first name: ")
player_last_name = input("Enter the player's last name: ")
player_team = input("Enter the player's team's name: ")
context_measure_simple = input("Enter either PTS or FGA: ")
season_nullable = input("Enter the season: ")
season_type_all_start = input("Enter the season type: ")

team_id = get_team_id(player_team)
player_id = get_player_id(player_first_name, player_last_name)
note = player_first_name + " " + player_last_name + "\n" + season_nullable + " " + season_type_all_start
filename = "ShortChart_" + player_first_name + player_last_name + "_" + season_nullable + ".png"
shot_json = shotchartdetail.ShotChartDetail(
    team_id = team_id,
    player_id = player_id,
    context_measure_simple = context_measure_simple,
    season_nullable = season_nullable,
    season_type_all_star = season_type_all_start)

# print(get_team_id('New York Knicks'))
# print(find_lebron())
# print(get_player_id('LeBron', 'James'))

shot_data = json.loads(shot_json.get_json())
relevant_data = shot_data['resultSets'][0]

headers = relevant_data['headers']
rows = relevant_data['rowSet']

player_data = pd.DataFrame(rows)
player_data.columns = headers
# print(curry_data.columns)




mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])

ax = create_court(ax, 'black')
ax.hexbin(player_data['LOC_X'], player_data['LOC_Y'] + 60, gridsize=(30,30), extent=(-300,300,0,940), bins = 'log', cmap='Blues')

ax.text(0, 1.05, note, transform=ax.transAxes, ha = 'left', va = 'baseline')

plt.savefig(filename, dpi=300, bbox_inches='tight')
plt.show()

