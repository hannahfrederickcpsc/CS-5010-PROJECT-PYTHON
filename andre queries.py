# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 11:10:10 2020

@author: andre
"""

import pandas as pd
from scipy import stats
import unittest

# Some queries for election data

## Effect of presidential elections on mean turnout
data = pd.read_csv('complete_cleaned.csv')
pres_years = data.loc[data['Year']%4==0]
nonpres_years = data.loc[data['Year']%4!=0]


## Evaluate the mean turnouts in presidential and non-presidential years
pres_turnout_mean = pres_years['Turnout (% Voting of Total Registered)'].mean()
nonpres_turnout_mean = nonpres_years['Turnout (% Voting of Total Registered)'].mean()
diff_percent = round(abs((pres_turnout_mean - nonpres_turnout_mean))*100,3)
print(str(diff_percent)+'% difference')

## unit test
class turnoutDifferencetest(unittest.TestCase):
    def test_is_diff_of_means(self):
        pres_turnout_mean = pres_years['Turnout (% Voting of Total Registered)'].mean()
        nonpres_turnout_mean = nonpres_years['Turnout (% Voting of Total Registered)'].mean()
        self.assertEqual(diff_percent, 27.629)
        
        
# 2 tailed t-test to see if this is a significant difference in means
stats.ttest_ind(pres_years['Turnout (% Voting of Total Registered)'], nonpres_years['Turnout (% Voting of Total Registered)'], equal_var=False)


# =======================================================================================================

# Did VA elect the winning candidate in any given year?
## establish dict of presidential election years and winners
pres_winners = {'1976':'Jimmy Carter', '1980':'Ronald W. Reagan', '1984':'Ronald W. Reagan',
                '1988':'George H. Bush', '1992': 'Bill Clinton', '1996': 'Bill Clinton',
                '2000': 'Bush and Cheney', '2004':'Bush and Cheney', '2008': 'Barack Obama',
                '2012': 'Barack Obama', '2016': 'Donald Trump'}

## define function to:
## take an election year
## check data against pres_winners dict
## return a boolean
def va_elect(year):
    return pres_winners[year] == pres_years.loc[pres_years.Year == int(year), 'Winner (VA)'].values[0]

check_year = input('Please enter a presidential election year: ')
print('Did Virginia results align with the nation in this election? ' + str(va_elect(check_year)))

class electChecktest(unittest.TestCase):
    def test_va_elect(self):
        check_year = '1980'
        self.assertTrue(va_elect(check_year))



if __name__ == '__main__':
    unittest.main()

