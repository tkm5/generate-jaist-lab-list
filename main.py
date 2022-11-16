from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# %%
URL = 'https://www.jaist.ac.jp/areas/information-science.html'
html = requests.get(URL)

# %%
soup = BeautifulSoup(html.content, "lxml")
li_list = soup.find_all('li', {'class': 'iBtxt'})

lab_list = [x.text for x in li_list]
url_list = [x.find('a').get('href') for x in li_list]

# %%
lab_name = []
lab_course = []
for lab in lab_list:
    lab_name.append(re.split('[（）]', lab)[0])
    lab_course.append(re.split('[（）]', lab)[1])

lab_df = pd.DataFrame({'lab_name': lab_name,
                       'lab_course': lab_course,
                       'url': url_list})


# %%
def add_jaist_domain(url):
    if str(url).startswith('/laboratory'):
        full_url = 'https://www.jaist.ac.jp' + url
        return full_url
    else:
        return url


lab_df['url'] = lab_df['url'].apply(add_jaist_domain)

# %%
h1_list = []
for url in lab_df['url']:
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "lxml")
    header = soup.find('h1')
    try:
        header = header.text
    except AttributeError:
        pass
    finally:
        h1_list.append(header)

lab_df['title'] = h1_list

lab_df.to_csv('jaist_lab_info.csv')
