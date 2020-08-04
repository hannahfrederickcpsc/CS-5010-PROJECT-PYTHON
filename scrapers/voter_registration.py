
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
virginia_results = pd.DataFrame(columns=columns)
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
    virginia_results = pd.concat([virginia_results, temp_df], ignore_index=True)

#convert our data frame to a csv file
virginia_results.to_csv(r"voter_registration.csv", index = False, sep=',')
