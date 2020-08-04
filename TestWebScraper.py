
import sys
sys.path.append('scrapers/')
import unittest
import requests
from voter_registration import *

class TestWebScraper(unittest.TestCase):
    #test to see if the only_numerics function converts and returns a string of only numbers to a float of that number
    def test_does_only_numerics_work_with_numeric_strings(self):
        #does only_numerics successfully convert the string of numbers to a float of that number?

        #set-up
        string_num = '1,000,000' #declare the string of numbers to convert to a float of that number
        print("Is " + string_num + " converted to and returned as " + str(only_numerics(string_num)) + "?")
        
        #test
        #is only_numerics('1,000,000) = 1000000.0
        self.assertEqual(only_numerics(string_num), 1000000.0)
        
    #test to see if the only_numerics function converts and returns a string of not only numbers to a float of that number
    def test_does_only_numerics_work_with_nonnumeric_strings(self):
        #does only_numerics successfully convert the string of numbers and characters to a float of that number?

        #set-up
        string_num = '1,000,000***' #declare the string of numbers and characters to convert to a float of that number
        print("Is " + string_num + " converted to and returned as " + str(only_numerics(string_num)) + "?")
        
        #test
        #is only_numerics('1,000,000***') = 1000000.0
        self.assertEqual(only_numerics(string_num), 1000000.0)
        
    #test to see if the percentages function converts and returns a string of a positive number to a float of that percent
    def test_does_percentages_work_with_positive_numeric_strings(self):
        #does percentages successfully convert the string of a positive number to a float of that percent?

        #set-up
        string_num = '10.0%' #declare the string of numbers to convert to a float of that percent
        print("Is " + string_num + " converted to and returned as " + str(percentages(string_num)) + "?")
        
        #test
        #is only_numerics('10.0%') = 0.1
        self.assertEqual(percentages(string_num), 0.1)
        
    #test to see if the percentages function converts and returns a string of a negative number to a float of that percent
    def test_does_percentages_work_with_negative_numeric_strings(self):
        #does percentages successfully convert the string of a negative number to a float of that percent?

        #set-up
        string_num = '-10.0%' #declare the string of numbers to convert to a float of that percent
        print("Is " + string_num + " converted to and returned as " + str(percentages(string_num)) + "?")
        
        #test
        #is only_numerics('-10.0%') = -0.1
        self.assertEqual(percentages(string_num), -0.1)
        
    #test to see if the percentages function converts and returns a string of a positive number with characters to a float of that percent
    def test_does_percentages_work_with_positive_nonnumeric_strings(self):
        #does percentages successfully convert the string of a positive number with characters to a float of that percent?

        #set-up
        string_num = '10.0%**' #declare the string of numbers and characters to convert to a float of that percent
        print("Is " + string_num + " converted to and returned as " + str(percentages(string_num)) + "?")
        
        #test
        #is only_numerics('10.0%**') = 0.1
        self.assertEqual(percentages(string_num), 0.1)
        
    #test to see if the percentages function converts and returns a string of a negative number with characters to a float of that percent
    def test_does_percentages_work_with_negative_nonnumeric_strings(self):
        #does percentages successfully convert the string of a negative number with characters to a float of that percent?

        #set-up
        string_num = '-10.0%**' #declare the string of numbers and characters to convert to a float of that percent
        print("Is " + string_num + " converted to and returned as " + str(percentages(string_num)) + "?")
        
        #test
        #is only_numerics('-10.0%**') = -0.1
        self.assertEqual(percentages(string_num), -0.1)
        
    # test that the va department of elections registration page is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_voter_registration_scraper_request(self):
        url = "https://www.elections.virginia.gov/resultsreports/registrationturnout-statistics/"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print("Voter registration site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)

    
    # test that the va department of elections presidential results apge is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_presidential_election_scraper_request(self):
        url = "https://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2019/office_id:1/stage:General"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # accesses the website
        print("Presidential election site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)


    # test that the va department of elections gubernatorial results page is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_gubernatorial_election_scraper_request(self):
        url = "https://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2017/office_id:3/stage:General"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # accesses the website
        print("Gubernatorial election site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()  