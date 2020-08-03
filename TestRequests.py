
import unittest
import requests

class TestRequests(unittest.TestCase):
    # test that the va department of elections registration page is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_voter_registration_scraper_request(self):
        url = "https://www.elections.virginia.gov/resultsreports/registrationturnout-statistics/"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        print("voter registration site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)

    
    # test that the va department of elections presidential results apge is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_presidential_election_scraper_request(self):
        url = "https://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2019/office_id:1/stage:General"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # accesses the website
        print("presidential election site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)


    # test that the va department of elections gubernatorial results page is responding
    # the HTTP 200 OK success status response code indicates that the request succeeded
    def test_gubernatorial_election_scraper_request(self):
        url = "https://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2017/office_id:3/stage:General"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # accesses the website
        print("gubernatorial election site status code:",response.status_code)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()