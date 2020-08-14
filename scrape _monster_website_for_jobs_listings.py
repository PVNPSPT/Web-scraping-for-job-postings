import requests
import pprint
import re
import argparse
import sys
from bs4 import BeautifulSoup

def get_title_location_from_cl():
    """
    The function takes title and location as command-line arguments and returns the same details for scraping the website.
    """
    parser = argparse.ArgumentParser(description="get job title and location details")
    parser.add_argument('title',type=str,help='Enter the preferred job title')
    parser.add_argument('location',type=str,help='Enter the preferred job location')
    args = parser.parse_args(sys.argv[1:])
    #filename = sys.argv[1]
    job_title = vars(args)['title']
    job_location = vars(args)['location']
    return job_title,job_location





def get_job_listings_from_website():
    """
    The function takes the title and location details from the "get_title_location_from_cl()" function and scrape the website and prints the search results(job listings) in a readable way.
    """
    title_location = get_title_location_from_cl()
    URL = "https://www.monster.ca/jobs/search/?q={}&where={}".format(title_location[0],title_location[1].capitalize())
    page = requests.get(URL)
    # content_bytes_to_string = (page.content).decode('utf-8')
    # with open("monster_site_content.txt",'w') as job_content:
    #     job_content.write(content_bytes_to_string)
    # pprint.pprint(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="ResultsContainer")                              #results variable is a 'bs4.element.Tag'
    job_elements = results.find_all('section',class_='card-content')        #job_elements variable is a 'bs4.element.ResultSet'
    for job_element in job_elements:
        element_title = job_element.find('h2', class_="title")
        element_company = job_element.find('div', class_="company")
        element_location = job_element.find('div', class_="location")
        if None in (element_title,element_company,element_location):
            continue
        formatted_element_company = (element_company.text).rstrip()
        formatted_element_title = (element_title.text).replace('\n',"")
        new_formatted_element_company = formatted_element_company.lstrip()
        formatted_element_location = (element_location.text).lstrip()
        print(formatted_element_title)
        print(new_formatted_element_company)
        print(formatted_element_location)
        print()
    return results



def display_job_listings_with_apply_link():
    """
    The function filters the job listings and displays only listings that has title starting with "Data Scien" and gives apply links for the listings.
    """
    result_elements = get_job_listings_from_website()
    relevant_jobs = result_elements.find_all('h2',string=re.compile("Data Scien*"))  
    # print(relevant_jobs)
    #print(results.prettify())
    for job in relevant_jobs:
        link = job.find('a')['href']
        print(job.text.strip())
        print(f"Apply here: {link}\n")




    
    