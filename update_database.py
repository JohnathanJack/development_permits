import functions
import pandas as pd


url = 'https://www.shapeyourcity.ca/development'
PATH = "C:/Program Files (x86)/chromedriver-win64/chromedriver.exe"

# Load the saved pickle with all the URLs.
all_permit_urls_saved = pd.read_pickle('C:/Users/John/Documents/ml_projects/development_permits/permit_urls')

# Load the old database
old_df = pd.read_pickle('C:/Users/John/Documents/ml_projects/development_permits/database')

# Get the most recent url from the saved list
most_recent_url = all_permit_urls_saved[0]

# Grab the new urls
new_urls = functions.get_recent_urls(url, PATH, most_recent_url)

# Create a df for new_urls and combine with the old database
new_df = functions.combine_database(new_urls, old_df, PATH)

# Now update the database with the new url and dataframe
functions.update_database(new_urls, all_permit_urls_saved, new_df)