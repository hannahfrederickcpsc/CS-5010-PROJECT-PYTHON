# find_all documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
# HTML table object documentation: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/tr
# how to load in a saved html file instead of requesting one: https://stackoverflow.com/questions/21570780/using-python-and-beautifulsoup-saved-webpage-source-codes-into-a-local-file

import csv
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('va_elections.html'), 'html.parser')

election_results = []

table_body = soup.find('tbody')     # grab the body of the table element                                     

# grab only the rows that are election items (tr = table row)                                                                        
for row in table_body.find_all('tr', class_="election_item"):       

    single_year = {}

    year = row.find("td", class_="year first")      # td = cell in table row
    office = year.find_next_sibling()
    district = office.find_next_sibling()
    winner_container = row.find("td", class_="candidates_container_cell")

    single_year["Year"] = year.text
    single_year["Office"] = office.text
    single_year["District"] = district.text
    single_year["Winner"] = winner_container.div.span.text

    election_results.append(single_year)


filename = 'elections_results.csv'
with open(filename, 'w', newline='') as f: 
    w = csv.DictWriter(f,['Year', 'Office', 'District', 'Winner']) 
    w.writeheader() 
    for year in election_results: 
        w.writerow(year)

