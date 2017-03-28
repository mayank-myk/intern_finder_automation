#IIT-Kharagpur!
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from api import correctexp
from pprint import pprint

def get_data_iisc(url,interest):
    url=str(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    names=[]    #Names of all the proffessors
    links=[]    #links of all the proffessors
    fields = []  # 2-d array which consists all research areas in a list on that index!
    research=[]
    list=[]

    for link in soup.findAll('a',href=True):
        names.append(link.text.strip())
        links.append("http://www.ee.iisc.ac.in/"+ link['href'])

    for b in soup.find_all('span', {'class': 'smalltxt'}):
        research.append(b.text.strip())

    for i in xrange(0,9):
        names.pop()
        links.pop()

    names.pop(0)
    links.pop(0)
    names.pop(0)
    links.pop(0)
    names.pop(0)
    links.pop(0)
    names.pop(14)
    links.pop(14)
    research.insert(5, "Image Processing, Algorithms, Convex Optimization")

    i = 0
    for data in research:
        fields.append([])
        pos = 0
        j = 0
        for a in data:
            if a == ',':
                fields[i].append(data[pos:j].strip())
                pos=j
            if j == len(data) - 1:
                fields[i].append(data[pos:j].strip())
            j += 1
        i += 1

    for i in xrange(0,len(names)):
        list.append([])
        list[i].append(names[i])
        list[i].append('-------')
        list[i].append(links[i])
        list[i].append("-------")
        list[i].append(fields[i])

    i = 0
    k = 0
    final_list = []
    for x in list:
        count = 0
        for y in x[4]:
            rat = fuzz.partial_ratio(interest.lower(), y.lower())
            if count >= 1:
                break
            if rat >= 90:
                final_list.append({})
                final_list[k]['name'] = names[i]
                final_list[k]['email'] ='--------'
                final_list[k]['link'] = links[i]
                final_list[k]['contact_detail'] = '-------'
                final_list[k]['field'] = fields[i]
                count += 1
                k = k + 1
        i += 1

    return final_list

if __name__ == '__main__':
    data = raw_input("Enter Your Intern Interest(Topics):")
    tmp = correctexp(data)
    get_data_iisc("http://www.ee.iisc.ac.in/people-faculty.php",tmp)
