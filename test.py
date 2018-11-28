from bs4 import BeautifulSoup
import urllib.request
import json

prefix = "https://scholar.google.com"
token = ''
category = 'health_economics'
data = {}

for i in range(5):
    if i==0:
        url="https://scholar.google.com/citations?view_op=search_authors&mauthors=label:"+category
    else:
        url=prefix+token
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    soup = BeautifulSoup(mybytes, 'html.parser')
    # print(soup.prettify())
    heads = soup.find_all("h3", class_="gsc_oai_name")
    links = [x.a['href'].split('&')[0] for x in heads]
    names = [x.text for x in heads]
    affiliations = [x.text for x in soup.find_all("div", class_="gsc_oai_aff")]
    citations = [x.text for x in soup.find_all("div", class_="gsc_oai_cby")]
    attr = list(zip(names, affiliations, citations))
    tmp = soup.find_all("button")[-1]['onclick']
    j = 0
    stack = []
    for i in range(len(tmp)):
        if tmp[i]=='/':
            j=i
        if j>0:
            stack+=tmp[i]
            if len(stack)>3 and stack[-4]=="\\":
                c = chr(int(stack[-2]+stack[-1],16))
                stack = stack[:-4]+[c]
    token = ''.join(stack)

    for i in range(len(links)):
        data[links[i]] = attr[i]
for k in data:
    print(k,data[k])
