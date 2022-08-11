import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import csv
from collections import OrderedDict

baseurl = "https://cs.usm.my"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36'
}

r = requests.get('https://cs.usm.my/index.php/about/our-people/facultycs-member')

soup = BeautifulSoup(r.content, 'lxml')

productlist = soup.find_all('p')
#print(productlist)
productlinks = []

for item in productlist:
    for link in item.find_all('a', href = True):
        productlinks.append(baseurl + link['href'])
        
#print(productlinks)

testlink = 'https://cs.usm.my/index.php/faculty-member/174-chew-xin-ying-dr'
productlinks = productlinks[16:]
print(productlinks)
lec_list = []

for link in productlinks:
    r = requests.get(link, headers= headers)
    soup = BeautifulSoup(r.content, 'lxml')
    jobDescription = OrderedDict()

    
    name = soup.find('h1',class_="uk-article-title").text.strip()
    title = soup.find('strong').text.strip()
    classname_research = "uk-grid uk-grid-divider uk-grid-width-1-1 uk-grid-width-medium-1-3 uk-grid-width-large-1-3"
    
    
   # email = soup.find('ul',class_=classname_research).findAll('p', class_=False)[0]
    try:
        research_cluster = soup.find('ul',class_=classname_research).findAll('p', class_=False)[2].text
        research_interest = soup.find('ul',class_=classname_research).findAll('p', class_=False)[3].text
        specialization = soup.find('ul',class_= classname_research).findAll('p', class_=False)[4].text
    except:
        research_cluster = "missing info"
        research_interest = "missing info"
        specialization = "missing info"

    jobDescription.update(
        {'Name': name,
        'Title': title,
        'Research Cluster':research_cluster,
        'Specialization':specialization

    })

    ##############################################################
    
    jobDetails = soup.find('div',class_="tm-article-content")
    all_headers = ['h3','h5']

    for header in jobDetails.find_all(all_headers)[0:2]:
        jobDetail = header.get_text().strip()
        nextNode = header
        jobDetailText = []
        while True:
            nextNode = nextNode.nextSibling
                # This writes out the last of the H3 tags and its following contents
            if not nextNode:
                jobDescription[jobDetail] = "\n".join(jobDetailText)
                break
                # This adds non-H3 tags to the text to attach to the text of the H3
            elif isinstance(nextNode, NavigableString):
                if nextNode.strip():
                    jobDetailText.append(nextNode.strip())
                    pass
                # This detects the next H2 and writes the compiled text to the previous H2
            elif isinstance(nextNode, Tag):
                if nextNode.name in all_headers and len(nextNode.name) <30:
                    jobDescription[jobDetail] = "\n".join(jobDetailText)
                    break
                jobDetailText.append(nextNode.get_text(strip=True))

    
    #jobDescription.move_to_end('Name', last=False)
    lec_list.append(jobDescription)
    print('saving: ',jobDescription['Name'])
    print('keys: ',jobDescription.keys())


df = pd.DataFrame(lec_list)
print(df)
df.to_csv('test5.csv',index=None,header=True)