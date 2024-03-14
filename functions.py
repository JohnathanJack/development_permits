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


def get_list_of_urls(webpage,path):
    """
    Scrapes all the URLs of the development permits within the webpage

    Parameters:
        webpage (str): the url of the webpage
        path (str): the location of the user's chromedriver

    Returns:
        A list of strings which contains all of the development permits url 
    """
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(service = Service(path), options=chrome_options)
    driver.get(webpage)
    # The element is located within an iframe, required to locate the iframe and switch frames
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    url_list = []
    driver.switch_to.frame(iframe)
    page_num = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".chakra-button.ehq-paginationButton.css-i1louw")))
    last_page_num = int([item.text for item in page_num][-2])
    # Scrape all of the urls on each page
    for num in range(last_page_num+1):
        # Ensures that all the CSS elements are loaded before scraping
        urls = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.chakra-link.ehq-projectCoverImg.css-1eh7kaa')))
        for url in urls:
            url_list.append(url.get_attribute('href'))
        # After scraping all of the elements, click to the next page if not on the final page
        if num < last_page_num+1:
            click = driver.find_element(By.CSS_SELECTOR, ".chakra-button.ehq-paginationButton.ehq-paginationNextButton.css-i1louw")
            click.click()
        else:
            break
        time.sleep(5)
    driver.switch_to.default_content()
    driver.quit()
    return url_list



def get_list_of_applicant(list_of_description):
    """
    Utilizes regex to obtain the applicants name from the list of description

    Parameters:
        list_of_description (list of str): the description of the webpage derived from the get_description 

    Returns:
        A list of the applicant names 
    """
    
    regex = r'^[\s\S]*?(?=\s+has applied)'
    list_of_applicant = []
    for applicant in list_of_description:
        try:
            applicant_name = applicant[:re.search(regex, applicant).span()[1]]
        except:
            applicant_name = 'Unknown'
        list_of_applicant.append(applicant_name)
    return list_of_applicant



def application_status(driver):
    """
    Scrape webpage to obtain the Director of Planning decision

    Parameters:
        driver: the driver that opened the webpage

    Returns:
        The application status
    """  

    try:
        text_info = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME,'strong'))).text.split()
        if 'Director' in text_info:
            if 'approved' in text_info:
                return 'Approved'
            elif 'cancelled' in text_info:
                return 'Cancelled'
            elif 'withdrawn' in text_info:
                return 'Withdrawn'
            else:
                return 'Rejected'
        else:
            return 'In progress'
    except:
        return 'In progress'
    


def permit_status(driver, regex):
    """
    Scrapes webpage to obtain the development permit id

    Parameters:
        driver: the driver that opened the webpage
        regex: the regular expression required to isolate the permit id

    Returns:
        The development permit id 
    """
    
    try:
        head_text = driver.find_element(By.TAG_NAME, 'h1').text
        permit_id = re.search(regex, head_text)[1] 
    except:
        permit_id = 'Unknown'
    return permit_id



def scrape_description(driver):
    """
    Scrapes each webpage to obtain the description of each development permit application

    Parameters:
        driver: the driver that opened the webpage

    Returns:
        The description of the development permit application 
    """

    text = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'truncated-description'))).text
    return text



def scrape_info(list_of_urls, path):
    """
    Scrapes each webpage in the list of urls

    Parameters:
        list_of_urls (list of str): all the urls to be scraped
        path (str): the location of the user's chromedriver

    Returns:
        A tuple where the 0th element is the list status, the 1st element is the description list, and the 2nd element is the permit list
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    list_status = []
    description_list = []
    permit_list = []
    error_list = []
    regex_permit = r'\((DP.*?)\)'
    for url in list_of_urls:
        driver = webdriver.Chrome(service = Service(path), options = chrome_options)
        driver.get(url)
        try:
            list_status.append(application_status(driver))
            permit_list.append(permit_status(driver, regex_permit))
            description_list.append(scrape_description(driver))
            driver.quit()
            time.sleep(3)
        except:
            error_list.append(url)
            driver.quit()
            time.sleep(3)
    return list_status, description_list, permit_list, error_list



def create_df(scraped_info):
    """
    Creates a database out of the scraped information 

    Parameters:
        scraped_info (tuple): Information scraped from the function scrape_info

    Returns:
        A dataframe with the following columns: Applicant_Name, permit_id, applicant_status and description. 
    """

    applicant_names = get_list_of_applicant(scraped_info[1])
    df = pd.DataFrame({"Applicant_Name": applicant_names})
    df['permit_id'] = scraped_info[2]
    df['applicant_status'] = scraped_info[0]
    df['description'] = scraped_info[1]
    return df



def get_recent_urls(webpage, path, recent_url):
    """
    Scrapes all the recent URLs of the development permits within the webpage

    Parameters:
        webpage (str): the url of the webpage
        path (str): the location of the user's chromedriver
        recent_url (str): the most recent url from the saved list

    Returns:
        A list of strings which contains all of the development permits url 
    """
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(service = Service(path), options=chrome_options)
    driver.get(webpage)
    # The element is located within an iframe, required to locate the iframe and switch frames
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    url_list = []
    loop_check = True
    driver.switch_to.frame(iframe)
    while loop_check:
        urls = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.chakra-link.ehq-projectCoverImg.css-1eh7kaa')))
        for url in urls:
            if url.get_attribute('href') == recent_url:
                loop_check = False
                break
            url_list.append(url.get_attribute('href'))
        click = driver.find_element(By.CSS_SELECTOR, ".chakra-button.ehq-paginationButton.ehq-paginationNextButton.css-i1louw")
        click.click()
        time.sleep(5)
    driver.switch_to.default_content()
    driver.quit()
    return url_list



def combine_database(new_urls, old_df, path):
    """
    Creates a new dataframe and combine it with the old one

    Parameters:
        new_urls (list of str): the urls of the webpage
        old_df (DataFrame): the most recent dataframe
        path (str): the location of the user's chromedriver

    Returns:
        A new dataframe that combined the old with the new additions. 
    
    """
    
    if len(new_urls) == 0:
        return old_df
    else:
        scraped_info = scrape_info(new_urls, path)
        new_df = create_df(scraped_info)
        update_df = pd.concat([new_df, old_df])
        return update_df
    


def update_database(new_urls, old_urls, new_df):
    """
    Creates a new dataframe and combine it with the old one

    Parameters:
        new_urls (list of str): the urls of the webpage
        old_df (DataFrame): the most recent dataframe
        path (str): the location of the user's chromedriver

    Returns:
        Updates the pickle saved files for permit_urls and database  
    
    """

    if len(new_urls) == 0:
        print('Database not updated')
    else:
        new_urls.extend(old_urls)
        with open('permit_urls', 'wb') as f:
            pickle.dump(new_urls, f)
        with open('database', 'wb') as f:
            pickle.dump(new_df, f)
        print('Database updated')