from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException
import json

start_url = 'https://www.indeed.com/jobs?q=customer+success+manager&start=30'

with webdriver.Chrome("./chromedriver_win32_chrome105.0.5195/chromedriver.exe") as driver :
    # wait = WebDriverWait(driver, 10)
    driver.get(start_url) 
    time.sleep(5)
    jobs = driver.find_elements_by_css_selector('div.job_seen_beacon')

    class Job(object):
        index = 0
        job_title = '' 
        company_name = ''
        location = ''
        salary = ''
        job_posting_url=''

        def __init__(self, index, job_title, company_name, location, salary, job_posting_url):
            self.index = index
            self.job_title = job_title
            self.company_name = company_name
            self.location = location
            self.salary = salary
            self.job_posting_url = job_posting_url

    def make_job(index, job_title, company_name, location, salary, job_posting_url):
        return Job(index, job_title, company_name, location, salary, job_posting_url)

    scrapedJobs = list()
    for index in range(len(jobs)):
        sourcedFrom = 'indeed'
        job = jobs[index]
        job_title = job.find_element_by_css_selector('h2.jobTitle').text
        company_name = job.find_element_by_css_selector('span.companyName').text
        location = job.find_element_by_css_selector('div.companyLocation').text
        salary = ''
        job_posting_url = job.find_element_by_css_selector('.jobTitle a').get_attribute('href')
        try:
            salary = job.find_element_by_css_selector('div.salary-snippet-container').text
        except NoSuchElementException:
            salary = job.find_element_by_css_selector('.estimated-salary').text
        except NoSuchElementException:
            pass
        scrapedJobs.append((make_job(index, job_title, company_name, location, salary, job_posting_url)))
    
    print(scrapedJobs[0].company_name)
    print(scrapedJobs[2].company_name)
    print(scrapedJobs[5].company_name)
    print(scrapedJobs[7].company_name)

    # Convert list of objects to JSON
    json1 = json.dumps(scrapedJobs[0].__dict__)
    print(json1)
    data2convert = [obj.__dict__ for obj in scrapedJobs]
    json2 = json.dumps(data2convert)
    print(json2)
    # Write JSON to file
    with open('indeed_JSON.json', 'w') as file:
        json.dump(data2convert, file, ensure_ascii=False, indent=4)