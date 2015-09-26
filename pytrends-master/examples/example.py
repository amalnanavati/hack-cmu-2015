from pytrends.pyGTrends import pyGTrends
import time
from random import randint
from parsecsv import *


google_username = "hackcmu2015"
google_password = "hack2015"
path = "/Users/AnnaGupta/hack-cmu-2015/pytrends-master/examples/"

# connect to Google
connector = pyGTrends(google_username, google_password)

# make request
connector.request_report("Selena Gomez", hl='en-US', cat=None, geo='US', date=None)

# wait a random amount of time between requests to avoid bot detection
time.sleep(randint(5, 10))

# download file
connector.save_csv(path, "selenagomez")

# get suggestions for keywords
keyword = "selena gomez"
data = connector.get_suggestions(keyword)
print(data)

obj = Data("selenagomez.csv", "selena gomez")
print obj.getData()
