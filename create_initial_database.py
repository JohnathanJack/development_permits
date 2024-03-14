import functions
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pickle
import re

url = 'https://www.shapeyourcity.ca/development'
PATH = "C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

all_permit_urls = functions.get_list_of_urls(url, PATH)
# save the urls to a pickle file that can be opened at any time without re-running the code. 
with open('permit_urls', 'wb') as f:
    pickle.dump(all_permit_urls, f)

# Scrape all of the information required from the list of urls
all_information = functions.scrape_info(all_permit_urls, PATH)

# Create a dataframe with all the information
df = functions.create_df(all_information)

# save the database
with open('database', 'wb') as f:
    pickle.dump(df, f)

