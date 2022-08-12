# web_scraper

Title:  Scrap academic staff profile from static site <br>
Site:  https://cs.usm.my/index.php/about/our-people/facultycs-member <br>
Tech Stack: [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) <br>
Purpose: To 🔎 potential FYP supervisors easily using filter function. <br>
Data file: https://bit.ly/cslecturer
## Data description

| column_name | description |
| ------------- | ------------- |
| name  | lecturer's name + title  |
| email  | lecturer's usm email  |
| title  | lecturer's title  |
| research cluster | 3 clusters available: Data To Knowledge, Service Computing, Enabling Technologies & Infrastructures   |
| specialization  | describe one's research expertise  |
| interest | describe one's research interest  |
| qualification | describe one's education background  |
| source_url | directory to official site  |

## How to use?
<img src="/images/filter_security.gif" width="480" height="350"/>

1. Open [file](https://bit.ly/cslecturer) *You may download the file as xlsx
2. Create filter views
3. Select 'Filter by condition' 
4. Key in desired value E.g. security, software engineering


#### Disclaimer
Feel free to create pull request if you are interested to enhance the data quality.
This repo is for educational purposes only. 🤗🤗

Future works: Will demo web scraping for dynamic JS site.
