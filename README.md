# Development Permit for Vancouver

The goal of this project is to create an algorithm that can scrape the development permits off of the [Vancouver Development Webpage](https://www.shapeyourcity.ca/development) and have a process that can update the new additions daily. The data that will be scraped from the webpage are as follows:  

-Permit ID   
-Applicant Name   
-Description   
-Approval Status 


# Overall Method 
1) Determine the elements and location of the necessary data that is required (url at this step)
2) Compile a list of all the urls of each development permit listing
3) Determine the elements from each webpage to scrape the necessary data
4) Create the initial database with all the information and save it
5) Check for any new updates on the webpage and update the old database if necessary


# Results
Sucessfully able to scrape the data with very few edge cases. Utilized the python notebook to create and test all code. Pyfiles were created after the testing was completed in the notebook. There are no issues with running the code in the notebook, but there are some certificate issues when ran through the command line. Does not impact the overall result of the code and still works as intended. 

# Improvements for the Future
Currently, the webscraping algorithm expects that the format of the webpage will be consistent for every single development permit. It has no issues for the majority of the data, but this is not the case with all of the information. The affected values are: applicant status and applicant name. 

# Type of files in the repository
-notebook.ipynb is where the code was written and tested  
-functions.py is where all of the functions are located  
-create_initial_database.py is where the baseline of the database is created  
-update_database.py is where future updates to the database can be made  
-database, permit_urls, and scraped_data are pickle files that are used to save the necessary information.  

# Running the code from scratch
To run the create_database.py file will take about ~2hours. It can scrape around 300 urls every hour at this moment. At the time of scraping, there was a little more than 600 development permits to scrape. 


