import pandas as pd, numpy as np, streamlit as st, matplotlib.pyplot as plt, plotly.express as px, plotly.graph_objects as go
from analysis import GetData as GD, PlayerAnalysis as PA, TeamAnalysis as TA, OverAll as OA, teams

# showing title on top
st.title('PKL S01 - S07 Analysis')

st.error("*Due to limited and incomplete data, stats might not be 100% correct as per the time you are checking.")

# getting name of all the teams
team_names = GD.get_team_names()

# creating a sidebar so selection process can be done 
# it can also be hidden whenever required
st.sidebar.title('Selection Bar')

# giving user different type of analysis type
analysis_type_button = st.sidebar.selectbox('Select Type of Analysis', ['Based On Raiders', 'On A Team', 'Over All'])

# if user want to see stats by raider name
if analysis_type_button == 'Based On Raiders':
    # getting and showing name of all the raiders
    raider_name_button = st.sidebar.selectbox('Select Raider', GD.get_raider_names())

    # if raider's name is selected
    if raider_name_button:

        # showing raider's name when raider is selected
        st.header('Raider Name : ' + raider_name_button)

        # getting and showing total no of raid
        st.write("Total No of Raids Done : {} ".format(PA(raider_name_button).total_raids))

        # getting and showing total points score by raider
        st.write("Total Points : {} ".format(PA(raider_name_button).total_points))
        
        # super raids 
        st.write("No of Super Raids: {}".format(PA(raider_name_button).number_of_superraids))

        # number of super tens
        st.write("No of Super Tens: {}".format(PA(raider_name_button).number_of_supertens))


        # highest points scored by raider in single match
        st.write(raider_name_button + " Scored {} Points, Highest in one match on {}  ".format(PA(raider_name_button).highest_score, PA(raider_name_button).date))


        # getting raider's raiding results and showing raider's performance as graph based on those results
        st.plotly_chart(PA(raider_name_button).graph1)

        # getting raider's match by match total points and showing as graph

        st.plotly_chart(PA(raider_name_button).graph2)

# if user want to see over all stats
elif analysis_type_button == 'Over All':

     # showing different type of analysis
    achievements_button = st.sidebar.selectbox('Over All Of', ['Teams', 'Raiders'])

    # if raider's name is selected
    if achievements_button == 'Teams':
        # showing raider's name when raider is selected
        st.header('Over All Teams Analysis')
        st.plotly_chart(OA().team_matches)
        st.plotly_chart(OA().team_wins)
        st.plotly_chart(OA().team_ties)
        st.plotly_chart(OA().team_highest)
        st.plotly_chart(OA().team_avg)
        st.plotly_chart(OA().team_contro)
    
    else:
        st.header('Over All Raider Analysis')



        
        #total raids

        st.plotly_chart(OA().total_raids)
        
    #successful raids

        st.plotly_chart(OA().successful_raids)

    #empty raids

        st.plotly_chart(OA().empty_raids)

    #unsccessful raids

        st.plotly_chart(OA().unsuccessful_raids)


        
        # super raids
        st.plotly_chart(OA().super_raids)


    # top 10 players with most no of do or die raids

        st.plotly_chart(OA().dod_raids)


    # top 10 players with most no of successful do or die raids
        st.plotly_chart(OA().successful_dod_raids)


    # top 10 players with most no of unsuccessful do or die raids
        st.plotly_chart(OA().unsuccessful_dod_raids)


# if user want to see stats by team name
else:
    team_name_button = st.sidebar.selectbox('Select Team', team_names)
    if team_name_button:
        # showing team's name when team is selected
        st.header('Team Name : ' + team_name_button)


        # getting and showing total no of matches played
        st.write("Total No of Matches Played : {} ".format(TA(team_name_button).played))

        # getting and showing no of won matches
        st.write("Total Wins : {} ".format(TA(team_name_button).won))

        # getting and showing no of lost matches
        st.write("Total Losses : {} ".format(TA(team_name_button).lost))

        # getting and showing no of draw matches
        st.write("Total Draws : {} ".format(TA(team_name_button).draw))

        # highest points scored by team in single match
        st.write('Highest Score in Single Match: ' +  str(TA(team_name_button).highest_score))

        # avg points scored by team in every match
        st.write("On Avg Score in One Mmatch: {}".format(TA(team_name_button).avg_score))

        # getting team's match results and showing team's performance as graph based on those results
        st.plotly_chart(TA(team_name_button).graph1)


        # getting team's match by match total points and showing as graph
        st.plotly_chart(TA(team_name_button).graph2)



