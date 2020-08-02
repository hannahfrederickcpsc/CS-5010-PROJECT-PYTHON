# find_all documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
# HTML table object documentation: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr
# how to load in a saved html file instead of requesting one: https://stackoverflow.com/questions/21570780/using-python-and-beautifulsoup-saved-webpage-source-codes-into-a-local-file

import csv
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('presidential_election.html'), 'html.parser')

election_results = []

table_body = soup.find('tbody')     # grab the body of the table element                                     

# grab only the rows that are election items (tr = table row)                                                                        
for row in table_body.find_all('tr', class_="election_item"):       

    single_year = {}

    year = row.find("td", class_="year first")      # td = cell in table row
    office = year.find_next_sibling()
    district = office.find_next_sibling()
    sub_table_container = row.find("td", class_="candidates_container_cell")

    single_year["Year"] = year.text
    single_year["Office"] = office.text
    # single_year["District"] = district.text
    single_year["Winner (VA)"] = sub_table_container.div.span.text

    # enter the drop down tables in each row of the main table only for the winning candidate
    for sub_row in sub_table_container.find_all('tr', class_="is_winner"):

        # find_all('td, class_="number") returns a list containing candidate's total votes total votes represented as a percentage
        # pick total votes and percentage from list & remove commas and % from respective elements
        total_votes_str = sub_row.find_all('td', class_="number")[0].text.replace(",", "")
        votes_percentage_str = sub_row.find_all('td', class_="number")[1].text[:-1]

        # add party, total votes, and % of total votes to the dictionary for a single year's election
        single_year['Party'] = sub_row.td.find('div', class_="party").text
        single_year["Winner's Vote Count"] = int(total_votes_str)
        single_year["Winner's Percent of Total Votes"] = float(votes_percentage_str)/100

    # add results from each row to the main list
    election_results.append(single_year)

# convert election_results list of dictionaries into csv
filename = 'presidential_results.csv'
with open(filename, 'w', newline='') as f: 
    w = csv.DictWriter(f,['Year', 'Office', 'Winner (VA)', 'Party', "Winner's Vote Count", "Winner's Percent of Total Votes"]) 
    w.writeheader() 
    for year in election_results: 
        w.writerow(year)

