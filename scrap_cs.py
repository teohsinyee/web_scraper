"""
==========================================
Title:  Web scraping academic staff profile 
Site:  https://cs.usm.my/index.php/about/our-people/facultycs-member
Author: Teoh Sin Yee
Date:   11 Aug 2022
==========================================
"""
import requests
import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup, NavigableString, Tag


baseurl = "https://cs.usm.my"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36'
}

r = requests.get('https://cs.usm.my/index.php/about/our-people/facultycs-member')

soup = BeautifulSoup(r.content, 'lxml')

lecturer_list = soup.find_all('p')

lecturer_links = []

for item in lecturer_list:
    for link in item.find_all('a', href = True):
        lecturer_links.append(baseurl + link['href'])
        

lecturer_links = lecturer_links[16:]

lecturer_profile = []

for link in lecturer_links:
    r = requests.get(link, headers= headers)
    soup = BeautifulSoup(r.content, 'lxml')
    profile_description = OrderedDict()

    name = soup.find('h1',class_="uk-article-title").text.strip()
    title = soup.find('strong').text.strip()
    classname_research = "uk-grid uk-grid-divider uk-grid-width-1-1 uk-grid-width-medium-1-3 uk-grid-width-large-1-3"
   
   # email = soup.find('ul',class_=classname_research).findAll('p', class_=False)[0]
   # -- email can't be scraped because of spam protection --

    try:
        research_cluster = soup.find('ul',class_=classname_research).findAll('p', class_=False)[2].text
        research_interest = soup.find('ul',class_=classname_research).findAll('p', class_=False)[3].text
        specialization = soup.find('ul',class_= classname_research).findAll('p', class_=False)[4].text
    except:
        research_cluster, research_interest, specialization = "missing info"

    profile_description.update(
        {'Name': name,
        'Title': title,
        'Research Cluster':research_cluster,
        'Specialization':specialization

    })
    
    profile_details = soup.find('div',class_ = "tm-article-content")
    all_headers = ['h3','h5']

    for header in profile_details.find_all(all_headers)[0:2]:
        info_get = header.get_text().strip()
        nextNode = header
        profile_details_text = []
        while True:
            nextNode = nextNode.nextSibling
            # This writes out the last of the H3 & H5 tags and its following contents
            if not nextNode:
                profile_description[info_get] = "\n".join(profile_details_text)
                break
                # This adds non-H3 & non-H5 tags to the text to attach to the text of the H3 & H5
            elif isinstance(nextNode, NavigableString):
                if nextNode.strip():
                    profile_details_text.append(nextNode.strip())
                    pass
                # This detects the next H3 & H5 and writes the compiled text to the previous H3 & H5
            elif isinstance(nextNode, Tag):
                if nextNode.name in all_headers and len(nextNode.name) <30:
                    profile_description[info_get] = "\n".join(profile_details_text)
                    break
                profile_details_text.append(nextNode.get_text(strip=True))
   
    lecturer_profile.append(profile_description)
    print('saving: ',profile_description['Name'])
    print('keys: ',profile_description.keys())

df_profile = pd.DataFrame(lecturer_profile)
print(df_profile)

names = df_profile['Name'].tolist()
source_url = lecturer_links

#df_profile.to_csv('lecturer_profile.csv', index=None, header=True)

dir = pd.DataFrame(list(map(list, zip(names,source_url))))
dir.to_csv('directory.csv', index=None, header=True) 
