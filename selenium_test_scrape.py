from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException
import json
import os

start_url = 'https://www.indeed.com/jobs?q=customer+success+manager&start=30'

# First delete the old JSON output file
fileName = "indeed_JSON.json"
if os.path.exists(fileName):
    os.remove(fileName)

# Create objects and methods to store scraped data


class Job(object):
    index = 0
    title = ''
    company = ''
    location = ''
    salary = ''
    job_posting_url = ''
    description = ''
    remote = ''
    datePosted = ''
    status = ''

    def __init__(self, index, job_title, company_name, location, salary, job_posting_url,  description, remote, datePosted, status):
        self.index = index
        self.title = job_title
        self.company = company_name
        self.location = location
        self.salary = salary
        self.job_posting_url = job_posting_url
        self.description = description
        self.remote = remote
        self.datePosted = datePosted
        self.status = status


def make_job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status):
    return Job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status)


# ============================
# Start Scraping
# ============================

# Load up the website in Chrome
with webdriver.Chrome("./chromedriver_win32_chrome111.0.5563.64/chromedriver.exe") as driver:
    # wait = WebDriverWait(driver, 10)
    driver.get(start_url)
    time.sleep(5)
    jobs = driver.find_elements_by_css_selector('div.job_seen_beacon')

    scrapedJobs = list()
    for index in range(len(jobs)):
        sourcedFrom = 'indeed'
        job = jobs[index]
        job_title = job.find_element_by_css_selector('h2.jobTitle').text
        try:
            job_posting_url = job.find_element_by_css_selector(
                '.jobTitle a').get_attribute('href')
        except NoSuchElementException:
            pass
        print('SAND @ ', index, 'job_posting_url:', job_posting_url)
        print('SAND @ ', index, 'title:', job_title)

        company_name = None
        try:
            company_name = job.find_element_by_css_selector(
                'span.companyName').text
        except NoSuchElementException:
            pass
        print('SAND @ ', index, 'company:', company_name)

        location = None
        try:
            location = job.find_element_by_css_selector(
                'div.companyLocation').text
        except NoSuchElementException:
            pass
        print('SAND @ ', index, 'location:', location)

        remote = None
        if "Hybrid" in location:
            remote = "Hybrid"
        elif "Remote" in location:
            remote = "Remote"
        else:
            remote = "Office"
        print('SAND @ ', index, 'remote:', remote)

        # Try to find the salary, otherwise pass
        salary = None
        try:
            salary = job.find_element_by_css_selector(
                'div.salary-snippet-container').text
        except NoSuchElementException:
            try:
                salary = job.find_element_by_css_selector(
                    '.estimated-salary').text
            except NoSuchElementException:
                pass

        datePosted = None
        try:
            datePosted = job.find_element_by_css_selector(
                '.date').text
        except NoSuchElementException:
            pass
        print('SAND @ ', index, 'datePosted:', datePosted)

        status = None

        description = None

        # Add to master list of jobs
        scrapedJobs.append(
            (make_job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status)))

    # Convert list of objects to JSON
    json1 = json.dumps(scrapedJobs[0].__dict__)
    data2convert = [obj.__dict__ for obj in scrapedJobs]
    json2 = json.dumps(data2convert)
    # Write JSON to file
    with open(fileName, 'w') as file:
        json.dump(data2convert, file, ensure_ascii=False, indent=4)
