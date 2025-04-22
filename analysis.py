files_path = 'files/'
import pandas as pd, numpy as np, matplotlib.pyplot as plt, plotly.express as px, plotly.graph_objects as go

matches= pd.read_csv(files_path + 'matches4.csv')
players = pd.read_csv(files_path + 'OFFICIAL_PKL_players.csv')
teams = pd.read_csv(files_path + 'teams.csv')
raids = pd.read_csv(files_path + 'raids2.0.csv')

class GetData:

    def get_raider_names():
        return raids['raider_name'].sort_values().unique()

    def get_team_names():
        return teams['name'].unique()


class PlayerAnalysis:

    def __init__(self, player_name):

        id = self.get_id(player_name)

        self.total_raids = self.get_info(id)[0]
        self.total_points = self.get_info(id)[1]
        self.successful_raids = self.get_info(id)[2]
        self.highest_score, self.date = self.get_highest_score(player_name)

        self.graph1 = self.get_events(player_name)
        self.graph2 = self.get_match_by_match(player_name)

        self.number_of_superraids = self.get_no_supers(player_name)[0]
        self.number_of_supertens = self.get_no_supers(player_name)[1]

    def get_id(self, player_name):
        return raids[raids['raider_name'] == player_name]['raider_id'].unique()[0]
    
    def get_info(self, id):
        return (
            raids[raids['raider_id'] == id]['event'].count(),
            raids[raids['raider_id'] == id]['event'][raids[raids['raider_id'] == id]['event']=='Successful Raid'].count(),
            raids[raids['raider_id'] == id]['raid_points'].sum()
            )
    
    def get_highest_score(self, name):
        highest_score_match =  raids[raids['raider_name'] == name ].groupby('match_id')['raid_points'].sum().sort_values(ascending=False).head(1)
        
        match_id, points = highest_score_match.index[0], highest_score_match.values[0]

        date = matches[matches['match_id'] == match_id]['date'].values[0]
        return points, date

    def get_events(self, name):
        
        event = raids[raids['raider_name'] == name]['event'].value_counts().sort_index(ascending=False)

        c = ['red', 'green', 'grey', 'orange']

        labels = event.index.to_list()
        values = event.values

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker = dict(colors = c[:len(values)]))])

        return fig
    
    def get_match_by_match(self, name):
        y_data = raids[raids['raider_name'] == name].groupby('match_id')['raid_points'].sum().sort_index(ascending=True)
        x_data= np.linspace(1, len(y_data), len(y_data))

        trace1 = go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(color='blue', width=2, dash='solid'), marker=dict(size=6, symbol='circle'))

        data = [trace1]
        layout = go.Layout(title= name +' Match by Match Performance', xaxis={'title':'Match No'}, yaxis={'title':'Points'})

        fig = go.Figure(data, layout)
        return fig

    def get_no_supers(self, name):

        # no of super raids for the specific player
        no_of_super_raids_by_raider = raids[(raids['raid_points'] >= 3) & (raids['raider_name'] == name)].index.__len__()


        # raider_match_points
        
        raider_match_points = raids[raids['raider_name'] == name].groupby('match_id')['raid_points'].sum().reset_index()

        raider_match_points = raids[raids['raider_name'] == name].groupby('match_id')['raid_points'].sum().reset_index()

        no_of_super_tens_by_raider = raider_match_points[raider_match_points['raid_points'] >= 10].index.__len__()   
        
        return (no_of_super_raids_by_raider, no_of_super_tens_by_raider)


class TeamAnalysis:
    
    def __init__(self, name):

        id = self.get_id(name)

        self.played = self.get_info(name)[0]
        self.won = self.get_info(name)[1]
        self.draw = self.get_info(name)[2]
        self.lost = self.get_info(name)[3]

        self.graph1 = self.get_events(name)
        self.graph2 = self.get_match_by_match(name)

        points = pd.concat([matches[matches['Team1'] == name]['Score1'], matches[matches['Team2'] == name]['Score2']], axis=0).sort_index()

        self.avg_score = "{:.2f}".format(points.values.mean())
        self.highest_score = points.values.max()
    
    def get_id(self, name):    
        teams = {
         'Jaipur Pink Panthers' :3,
         'U Mumba' :5,
         'Dabang Delhi K.C.' :2,
         'Bengal Warriors' :4,
         'Patna Pirates' :6,
         'Puneri Paltan' :7,
         'Telugu Titans' :8,
         'Bengaluru Bulls' :1,
         'Haryana Steelers' :28,
         'U.P. Yoddha' :30,
         'Tamil Thalaivas' :29,
         'Gujarat Fortunegiants ':31
        }
        if name in teams.keys():
            return teams[name]
        else:
            return np.nan

    def get_info(self, name):
        # matches_by_team = new_team_df[(new_team_df['Team1'] == name) | (new_team_df['Team2'] == name)]

        total_matches = matches[(matches['Team1'] == name) | (matches['Team2'] == name)].index.__len__()

        matches_won = matches[(matches['Team1'] == name) & (matches['Score1'] > matches['Score2'])].index.__len__() + matches[(matches['Team2'] == name) & (matches['Score1'] < matches['Score2'])].index.__len__()

        matches_lost = matches[(matches['Team1'] == name) & (matches['Score1'] < matches['Score2'])].index.__len__() + matches[(matches['Team2'] == name) & (matches['Score1'] > matches['Score2'])].index.__len__()

        matches_tie = matches[(matches['Team1'] == name) & (matches['Score1'] == matches['Score2'])].index.__len__() + matches[(matches['Team2'] == name) & (matches['Score1'] == matches['Score2'])].index.__len__()

        return (total_matches, matches_won, matches_tie, matches_lost)

    def get_events(self, name):
        
        results = self.get_info(name)[1:]

        c = ['green', 'grey', 'red']

        labels = ['Number of Matches Won', 'Number of Draws', 'Number Matches Lost']
        values = results

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker = dict(colors = c[:len(values)]))])

        return fig
    
    def get_match_by_match(self, name):

        points_match_by_match = pd.concat([matches[matches['Team1'] == name]['Score1'], matches[matches['Team2'] == name]['Score2']], axis=0).sort_index()

        y_data = points_match_by_match
        x_data= np.linspace(1, len(y_data), len(y_data))

        trace1 = go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(color='blue', width=2, dash='solid'), marker=dict(size=6, symbol='circle'))

        data = [trace1]
        layout = go.Layout(title= ' Match by Match Performance of ' + name, xaxis={'title':'Match No'}, yaxis={'title':'Points'})

        fig = go.Figure(data, layout)
        return fig

 
class OverAll:
    
    def __init__(self):
        
        #team stats
        self.team_matches = self.get_team_graphs()[0]
        self.team_wins = self.get_team_graphs()[1]
        self.team_ties = self.get_team_graphs()[2]
        self.team_avg = self.get_team_graphs()[3]
        self.team_contro = self.get_team_graphs()[4]
        self.team_highest = self.get_team_graphs()[5]    

        # player card stats
        self.red = self.get_card_info()[0]
        self.yellow = self.get_card_info()[1]
        self.green = self.get_card_info()[2]

        # player raids stats
        self.total_raids = self.get_raider_raid_info()[0]
        self.successful_raids = self.get_raider_raid_info()[1]
        self.empty_raids = self.get_raider_raid_info()[2]
        self.unsuccessful_raids = self.get_raider_raid_info()[3]
        self.super_raids = self.get_raider_raid_info()[4]

        # player do or die stats
        self.dod_raids = self.get_raider_dod_info()[0]
        self.successful_dod_raids = self.get_raider_dod_info()[1]
        self.unsuccessful_dod_raids = self.get_raider_dod_info()[2]
        
    def get_team_graphs(self):


        # 1. most no of matches played
        number_of_matches_by_teams = pd.Series(matches['Team1'].value_counts().sort_index(ascending=False).add(matches['Team2'].value_counts().sort_index(ascending=False), fill_value=0)).sort_values(ascending=False)

        # 2. most no of matches won
        number_of_matches_won_by_team = pd.Series(matches['winner_team'].value_counts().sort_values(ascending=False).values, index=matches['winner_team'].value_counts().sort_values(ascending=False).index.sort_values(ascending=False))

        # 3. most no of matches tie
        t1 = matches[matches['Score1'] == matches['Score2']]['Team2'].value_counts().sort_index(ascending=False)
        t2 = matches[matches['Score1'] == matches['Score2']]['Team1'].value_counts().sort_index(ascending=False)
        number_of_matches_tie_by_team = t1.add(t2, fill_value=0)


        # 4. most no of avg points per match by every team ( show in bar chart, low to high)
        a1 = matches.groupby('Team1')['Score1'].mean()
        a2 = matches.groupby('Team1')['Score2'].mean()
        a3 = matches.groupby('Team2')['Score1'].mean()
        a4 = matches.groupby('Team2')['Score2'].mean()
        avg_points_by_every_team =  a1.add(a2, fill_value=0).add(a3, fill_value=0).add(a4, fill_value=0).sort_values(ascending=False)/4


        # 5. points contribution ( pie chart of it)
        a1 = matches.groupby('Team1')['Score1'].sum()
        a2 = matches.groupby('Team1')['Score2'].sum()
        a3 = matches.groupby('Team2')['Score1'].sum()
        a4 = matches.groupby('Team2')['Score2'].sum()
        total_points = a1.add(a2, fill_value=0).add(a3, fill_value=0).add(a4, fill_value=0).sort_values(ascending=False)


        # 6. highest score in single matches by every team ( show it by bar chart, low to high)
        highest_scores = pd.DataFrame()
        teams = np.hstack([np.array(matches.groupby(['Team1'])['Score1'].max().index),np.array(matches.groupby(['Team1'])['Score2'].max().index), np.array(matches.groupby(['Team2'])['Score1'].max().index), np.array(matches.groupby(['Team2'])['Score2'].max().index)])
        scores = np.hstack([np.array(matches.groupby(['Team1'])['Score1'].max().values),np.array(matches.groupby(['Team1'])['Score2'].max().values), np.array(matches.groupby(['Team2'])['Score1'].max().values), np.array(matches.groupby(['Team2'])['Score2'].max().values)])

        highest_scores['Team'] = teams
        highest_scores['Score'] =  scores
        highest_scores = highest_scores.groupby('Team')['Score'].max()


        xax = [number_of_matches_by_teams.index.tolist(),number_of_matches_won_by_team.index.tolist(),number_of_matches_tie_by_team.index.tolist(),avg_points_by_every_team.index.tolist(),total_points.index.tolist(), highest_scores.index.tolist()]

        yax = [number_of_matches_by_teams.values, number_of_matches_won_by_team.values, number_of_matches_tie_by_team.values, avg_points_by_every_team.values, total_points.values, highest_scores.values]


        trace1 = go.Bar(x=xax[0], y=yax[0], marker={'color':'Silver'})
        trace2 = go.Bar(x=xax[1], y=yax[1] , marker={'color':'Green'})
        trace3 = go.Bar(x=xax[2], y=yax[2], marker={'color':'Grey'})
        trace4 = go.Bar(x=xax[3], y=yax[3], marker={'color':'Blue'})
        trace5 = go.Pie(labels=xax[4], values=yax[4], marker={'colors': ['Blue','Green', 'Red', 'Purple', 'Orange', 'Yellow', 'Pink', 'Brown', 'White', 'Black', 'Grey', 'Silver']})
        trace6 = go.Bar(x=xax[5], y=yax[5], marker={'color':'Purple'})


        all_matches_fig = go.Figure(data=[trace1], layout=go.Layout(title='Number of matches played', xaxis_title='Team Name', yaxis_title='Number of matches played'))

        wins_fig = go.Figure(data=[trace2], layout=go.Layout(title='Number of matches played and won', xaxis_title='Team Name', yaxis_title='Number of matches won'))

        tie_fig = go.Figure(data=[trace3], layout=go.Layout(title='Number of matches played and tie', xaxis_title='Team Name', yaxis_title='Number of matches tie'))

        avg_points_fig = go.Figure(data=[trace4], layout=go.Layout(title='Avg points per match by every team', xaxis_title='Team Name', yaxis_title='Avg Points per match'))

        total_points_fig = go.Figure(data=[trace5], layout=go.Layout(title='Total points contribution by every team'))

        highest_score_fig = go.Figure(data=[trace6], layout=go.Layout(title= 'Highest score of every team', xaxis_title='Team Name', yaxis_title='Y'))

        return (all_matches_fig, wins_fig, tie_fig, avg_points_fig, total_points_fig, highest_score_fig)
    
    def get_card_info(self):
        # Cards to Players
        # total no of red card
        red_cards = players[players['player_red_card'] == True]['player_name'].value_counts().head(10)

        # total no of yellow card
        yellow_cards = players[players['player_yellow_card'] == True]['player_name'].value_counts().head(10)

        # total no of green card
        green_cards = players[players['player_green_card'] == True]['player_name'].value_counts().head(10)



        xax = [red_cards.index.tolist(), yellow_cards.index.tolist(), green_cards.index.tolist()]
        yax = [red_cards.values.tolist(), yellow_cards.values.tolist(), green_cards.values.tolist()]

        trace1 = go.Bar(x=xax[0], y=yax[0], marker={'color':'Red'})
        trace2 = go.Bar(x=xax[1], y=yax[1] , marker={'color':'Yellow'})
        trace3 = go.Bar(x=xax[2], y=yax[2], marker={'color':'Green'})

        red_cards_fig = go.Figure(data=[trace1], layout=go.Layout(title='Number Red Cards', xaxis_title='Player Name', yaxis_title='Number of Cards'))

        yellow_cards_fig = go.Figure(data=[trace2], layout=go.Layout(title='Number of Yellow Cards', xaxis_title='Player Name', yaxis_title='Number of Cards'))

        green_cards_fig = go.Figure(data=[trace3], layout=go.Layout(title='Number of Green Cards', xaxis_title='Player Name', yaxis_title='Number of Cards'))

        return (red_cards_fig, yellow_cards_fig, green_cards_fig)

    def get_raider_raid_info(self):
        # player total raid points
        total_raids = players.groupby('player_name')['player_raids_total'].sum().sort_values(ascending=False).head(10)

        # player successful raids
        players_successful_raids = players.groupby('player_name')['player_raids_successful'].sum().sort_values(ascending=False).head(10)

        # player empty raids
        players_empty_raids = players.groupby('player_name')['player_raids_Empty'].sum().sort_values(ascending=False).head(10)

        # player unsuccessful raids
        players_unsuccessful_raids = players.groupby('player_name')['player_raids_unsuccessful'].sum().sort_values(ascending=False).head(10)

                # most no of super raids
        super_raids = raids[raids['super_raid'] == True].groupby('raider_name')['super_raid'].count().sort_values(ascending=False).head(10)



        xax = [total_raids.index.tolist(),players_successful_raids.index.tolist(),players_empty_raids.index.tolist(),players_unsuccessful_raids.index.tolist(), super_raids.index.tolist()]

        yax = [total_raids.values.tolist(),players_successful_raids.values.tolist(),players_empty_raids.values.tolist(),players_unsuccessful_raids.values.tolist(), super_raids.values.tolist()]

        trace1 = go.Bar(x=xax[0], y=yax[0], marker={'color':'Blue'})
        trace2 = go.Bar(x=xax[1], y=yax[1] , marker={'color':'Green'})
        trace3 = go.Bar(x=xax[2], y=yax[2], marker={'color':'Grey'})
        trace4 = go.Bar(x=xax[3], y=yax[3], marker={'color':'Red'})
        trace5 = go.Bar(x=xax[4], y=yax[4], marker={'color':'Goldenrod '})

        total_fig = go.Figure(data=[trace1], layout=go.Layout(title='Top 10 Raiders with Most Number of Raids Done', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        success_fig = go.Figure(data=[trace2], layout=go.Layout(title='Top 10 Raiders with Most Number of Successful Raids Done', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        empty_fig = go.Figure(data=[trace3], layout=go.Layout(title='Top 10 Raiders with Most Number of Empty Raids Done', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        unsuccess_fig = go.Figure(data=[trace4], layout=go.Layout(title='Top 10 Raiders with Most Number of Unsuccessful Raids Done', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        super_fig = go.Figure(data=[trace5], layout=go.Layout(title='Top 10 Raiders with Most Number of Super Raids Done', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        return (total_fig, success_fig, empty_fig, unsuccess_fig, super_fig)

    def get_raider_dod_info(self):
        no_of_do_or_die = raids[raids['do_or_die'] == True].groupby('raider_name')['do_or_die'].count().sort_values(ascending=False).head(10)

        # do or die raids successful, unsuccessful
        successful_do_or_die = raids[(raids['do_or_die'] == True) & (raids['event'] == 'Successful Raid')].groupby('raider_name')['do_or_die'].count().sort_values(ascending=False).head(10)

        unsuccessful_do_or_die = raids[(raids['do_or_die'] == True) & (raids['event'] == 'Unsuccessful Raid')].groupby('raider_name')['do_or_die'].count().sort_values(ascending=False).head(10)


        xax = [no_of_do_or_die.index.tolist(),successful_do_or_die.index.tolist(),unsuccessful_do_or_die.index.tolist()]

        yax = [no_of_do_or_die.values.tolist(),successful_do_or_die.values.tolist(),unsuccessful_do_or_die.values.tolist()]


        trace1 = go.Bar(x=xax[0], y=yax[0], marker={'color':'Blue'})
        trace2 = go.Bar(x=xax[1], y=yax[1] , marker={'color':'Green'})
        trace3 = go.Bar(x=xax[2], y=yax[2], marker={'color':'Red'})


        dod_fig = go.Figure(data=[trace1], layout=go.Layout(title='Top 10 Total Number of Do or Die Raids Done By Raiders', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        dod_success_fig = go.Figure(data=[trace2], layout=go.Layout(title='Top 10 Number of Successful Do or Die Raids Done By Raiders', xaxis_title='Player Name', yaxis_title='Number of Raids'))

        dod_unsuccess_fig = go.Figure(data=[trace3], layout=go.Layout(title='Top 10 Number of Unsuccessful Do or Die Raids Done By Raiders', yaxis_title='Number of Raids'))

        return (dod_fig, dod_success_fig, dod_unsuccess_fig)


    #end