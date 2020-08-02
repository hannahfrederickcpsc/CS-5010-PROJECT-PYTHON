#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 09:03:11 2020

@author: seangrace
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.elections.virginia.gov/resultsreports/registrationturnout-statistics/"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) #accesses the website

# turning the response from the website into an html object that we can turn into a soup object
html = response.content

# making the html possible to sort through
soup = BeautifulSoup(html, 'html.parser') 
# take a look at the data to try to find what we need to extract
#print(soup.prettify())

# table object to extract different data types from
table = soup.find("table", attrs = {'class': "statistics_table"})
#print(table)
# iterate over the table soup item to create a list containing column names
columns = [col.get_text() for col in table.find_all("th")] # table headers are stored in "th" objects
#print(columns)

#create df which the data will be concated onto
final_df = pd.DataFrame(columns=columns)
#print(final_df)

#each row is in a 'tr' element
rows = table.find_all('tr')
#print(rows)
#print(len(rows))
#delete pointless row
del rows[0]

#function to return numeric strings converted to floats
def only_numerics(seq):
    seq_type= type(seq)
    return float(seq_type().join(filter(seq_type.isdigit, seq)))

#function to return percent strings converted to floats
def percentages(seq):
    clean_seq = seq.replace(' ', '')
    clean_seq = clean_seq.strip('*')
    return float(clean_seq.strip('%'))/100

### web scraping section ###

#iterate over the rows to extract table data stored in 'td' elements
for row in rows:
    row1 = [row1.get_text() for row1 in row.find_all('td')]
    
    row_list = list()
    for text in row1:
        if '%' in text:
            row_list.append(percentages(text)) #convert a percent string to a float 
        elif '%' not in text and ('***' != text or '' != text):
            try:
                row_list.append(only_numerics(text)) #convert a numeric string to a float
            except ValueError:
                row_list.append(None) #append none if string is not a percent or a number
    
    # place each row in a temporary data frame to add onto our final dataframe
    temp_df = pd.DataFrame(row_list).transpose()
    temp_df.columns = columns
    
    # concat temporary dataframe (row) onto final datafram
    final_df = pd.concat([final_df, temp_df], ignore_index=True)


final_df.head()
final_df.columns
final_df['Percentage Change from Previous Year'].head()

final_df.to_csv(r"voter_registration.csv", index = False, sep=',')

### data cleaning/merging section ###

voting_data = pd.read_csv("Virginia_Voting_Data.csv")
election_results = pd.read_csv("elections_results.csv")
# cast year to integer in both dataframes
voting_data["Year"] = voting_data["Year"].astype(int)
election_results["Year"] = election_results["Year"].astype(int)
# specify outer join with how='outer'
df_final = pd.merge(voting_data, election_results,  on='Year', how='outer')
df_final = df_final.loc[:43,]
df_final = df_final.rename(columns={"Winner" : "Winner (VA)"})
# index=False hides index column, sep="," separates at commas
df_final.to_csv("completed_cleaned.csv", index=False, sep=",")

#%%
### hannah's query asking section ###

summ_stats = df_final.describe()

party_summ_stats = df_final.groupby('Party').describe()

democratic_df = df_final.loc[df_final['Party'] == 'Democratic']

republican_df = df_final.loc[df_final['Party'] == 'Republican']

pre_motor_voter = df_final.loc[df_final['Year'] < 1996]

post_motor_voter = df_final.loc[df_final['Year'] >= 1996]

pre_motor_voter_stats = pre_motor_voter.describe()

post_motor_voter_stats = post_motor_voter.describe()
#%%
### sean's query asking section ###

pres_years = df_final.loc[df_final['Year']%4==0]

pres_years.columns

pres_years["Change in Total Voting"] = (pres_years["Total Voting"] / pres_years["Total Voting"].shift(-1)) -1

least_perc_change = abs(pres_years["Change in Total Voting"]).min()
voting_decrease = pres_years["Change in Total Voting"].min()
most_perc_change = abs(pres_years["Change in Total Voting"]).max()

least_perc_change_years = pres_years[pres_years["Change in Total Voting"] == least_perc_change] #1988
voting_decrease_years = pres_years[pres_years["Change in Total Voting"] == voting_decrease] #1996
most_perc_change_years = pres_years[pres_years["Change in Total Voting"] == most_perc_change] #2004

#%%
### data graphing section ###
import seaborn as sns
import matplotlib.pyplot as plt

pres_years = df_final.loc[df_final['Year']%4==0]

year_total_registered = sns.scatterplot(x="Year", y="Total Registered", data=df_final).set_title('Virginia Voters Registered Through the Years')
plt.savefig('year_total_registered.pdf')
year_total_registered_pres = sns.scatterplot(x="Year", y="Total Registered", data=pres_years).set_title('Virginia Voters Registered with Highlighted Presidential Years')
plt.savefig('year_total_registered_pres.pdf')
plt.clf()

year_total_voted = sns.scatterplot(x="Year", y="Total Voting", data=df_final).set_title('Virginia Voters Voting Through the Years')
plt.savefig('year_total_voted.pdf')
year_total_voted_pres = sns.scatterplot(x="Year", y="Total Voting", data=pres_years).set_title('Virginia Voters Voting with Highlighted Presidential Years')
plt.savefig('year_total_voted_pres.pdf')
plt.clf()

year_total_absentee = sns.scatterplot(x="Year", y="Voting Absentee (Included in Total Voting)", data=df_final).set_title('Virginia Voters Voting Absentee Through the Years')
plt.savefig('year_total_absentee.pdf')
year_total_absentee_pres = sns.scatterplot(x="Year", y="Voting Absentee (Included in Total Voting)", data=pres_years).set_title('Virginia Voters Voting Absentee with Highlighted Presidential Years')
plt.savefig('year_total_absentee_pres.pdf')
plt.clf()

year_voter_turnout = sns.scatterplot(x="Year", y="Turnout (% Voting of Total Registered)", data=df_final).set_title('Virginia Voter Turnout Through the Years')
plt.savefig('year_voter_turnout.pdf')
year_voter_turnout_pres = sns.scatterplot(x="Year", y="Turnout (% Voting of Total Registered)", data=pres_years).set_title('Virginia Voter Turnout with Highlighted Presidential Years')
plt.savefig('year_voter_turnout_pres.pdf')
plt.clf()

year_total_registered_party = sns.scatterplot(x="Year", y="Total Registered", hue="Party", data=df_final).set_title('Total Registered Virginia Voters Through the Years By Winning Party')
plt.savefig('year_total_registered_party.pdf')
plt.clf()

#%%

post_motor_voter = df_final.loc[df_final['Year'] >= 1996]

year_total_registered = sns.scatterplot(x="Year", y="Total Registered", data=df_final).set_title('Virginia Voters Registered Through the Years')
plt.savefig('year_total_registered.pdf')
year_total_registered_post = sns.scatterplot(x="Year", y="Total Registered", data=post_motor_voter).set_title('Virginia Voters Registered with Highlighted Motor Voter Years')
plt.savefig('year_total_registered_post.pdf')
plt.clf()

year_total_voted = sns.scatterplot(x="Year", y="Total Voting", data=df_final).set_title('Virginia Voters Voting Through the Years')
plt.savefig('year_total_voted.pdf')
year_total_voted_post = sns.scatterplot(x="Year", y="Total Voting", data=post_motor_voter).set_title('Virginia Voters Voting with Highlighted Motor Voter Years')
plt.savefig('year_total_voted_post.pdf')
plt.clf()

year_total_absentee = sns.scatterplot(x="Year", y="Voting Absentee (Included in Total Voting)", data=df_final).set_title('Virginia Voters Voting Absentee Through the Years')
plt.savefig('year_total_absentee.pdf')
year_total_absentee_post = sns.scatterplot(x="Year", y="Voting Absentee (Included in Total Voting)", data=post_motor_voter).set_title('Virginia Voters Voting Absentee with Highlighted Motor Voter Years')
plt.savefig('year_total_absentee_post.pdf')
plt.clf()

year_voter_turnout = sns.scatterplot(x="Year", y="Turnout (% Voting of Total Registered)", data=df_final).set_title('Virginia Voter Turnout Through the Years')
plt.savefig('year_voter_turnout.pdf')
year_voter_turnout_post = sns.scatterplot(x="Year", y="Turnout (% Voting of Total Registered)", data=post_motor_voter).set_title('Virginia Voter Turnout with Highlighted Motor Voter Years')
plt.savefig('year_voter_turnout_post.pdf')
plt.clf()




