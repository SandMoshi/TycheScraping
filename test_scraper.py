from requests_html import HTMLSession

session = HTMLSession()
headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,ar;q=0.8,es;q=0.7',
'cache-control': 'max-age=0',
'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
'dnt': '1',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "Windows",
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
# start_url = 'http://www.indeed.com/jobs'
start_url = 'https://www.indeed.com/jobs?q=customer+success+manager'
# start_url = 'https://www.indeed.com/jobs?q=customer+success+manager&start=30&vjk=54af555a35903fd4'
# start_url = 'https://blog.finxter.com/solved-error-after-upgrading-pip-cannot-import-name-main/'
response = session.get(start_url, headers=headers)

print(response.status_code)
# print(response)