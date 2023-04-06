from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
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
    job_type = ''
    company_rating = ''

    def __init__(self, index, job_title, company_name, location, salary, job_posting_url,  description, remote, datePosted, status, job_type, company_rating):
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
        self.job_type = job_type
        self.company_rating = company_rating


def make_job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status, job_type, company_rating):
    return Job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status, job_type, company_rating)


# ============================
# Start Scraping
# ============================

# Load up the website in Chrome
with webdriver.Chrome("./chromedriver_win32_chrome111.0.5563.64/chromedriver.exe") as driver:
    wait = WebDriverWait(driver, 10)
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

        remote = "No"
        if location is not None:
            if "Hybrid" in location:
                remote = "Hybrid"
            elif "Remote" in location:
                remote = "Remote"

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

        # Grab information from details panel
        description = None
        job_type = None
        job.click()
        # Wait for panel with description to appear
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#jobsearch-ViewjobPaneWrapper")))
        description = driver.find_element_by_css_selector(
            '#jobDescriptionText').text
        try:
            job_type_parent = driver.find_element_by_css_selector(
                'div:contains("Job Type")')
            job_type = job_type_parent.find_element_by_xpath(
                'following-sibling::div')
        except NoSuchElementException:
            pass

        # Grab the rating
        company_rating = None
        try:
            ratingContainer = driver.find_element_by_css_selector(
                '#companyRatings')
            if ratingContainer is not None:
                company_rating = ratingContainer.get_attribute(
                    'aria-label').split("stars", 1)[0] + "stars"  # discard 2nd half of sentence
        except NoSuchElementException:
            pass
        print('SAND @ ', index, 'rating:', company_rating)

        # Add to master list of jobs
        scrapedJobs.append(
            (make_job(index, job_title, company_name, location, salary, job_posting_url, description, remote, datePosted, status, job_type, company_rating)))

        # TODO - REMOVE THIS
        if index == 10:
            break

    # Convert list of objects to JSON
    json1 = json.dumps(scrapedJobs[0].__dict__)
    data2convert = [obj.__dict__ for obj in scrapedJobs]
    json2 = json.dumps(data2convert)
    # Write JSON to file
    with open(fileName, 'w', encoding='utf-8') as file:
        json.dump(data2convert, file, ensure_ascii=False, indent=4)
