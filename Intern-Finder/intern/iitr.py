# IIT-ROORKEE
from api import correctexp
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def get_data_iitr(url,interest):
    url = str(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    interest = str(interest)

    names = []  # Names of all the proffessors
    links = []  # links of all the proffessors
    research = []  # research areas
    emails = []
    fields = []  # 2-d array which consists all research areas in a list on that index!
    final_list=[]

    for link in soup.findAll('div',{'class':'interest'}):
        research.append(link.text.replace("Interests : ","").strip().lower())

    research.pop(29)

    for email in soup.findAll('span'):
        if "iitr.ac.in" in email.text:
            emails.append(email.text.replace("[at]","@"))

    emails.pop(29)

    for a in soup.find_all('a', href=True):
        if "departments/EE/pages/People+" in a['href']:
            if "http://www.iitr.ac.in/departments/EE/pages/People+" not in a['href']:
                url1 = 'http://www.iitr.ac.in'+a['href']
                links.append(url1.replace(" ", ""))

        if "departments/AH/pages/People+" in a['href']:
            url1 = 'http://www.iitr.ac.in/'+a['href']
            links.append(url1.replace(" ", ""))

    links=links[3:]
    links.pop(22)

    for link in links:
        responses = requests.get(link)
        soups = BeautifulSoup(responses.content, 'html.parser')
        i = 0
        for x in soups.findAll('div', {'class': 'title pageTitle'}):
            if "Spotlight" not in x.text:
                names.append(x.text.strip())

    names.insert(13,'Dheeraj Khatod')

    i=0
    for data in research:
        fields.append([])
        j=0
        x=0
        pos=0
        for a in data:
            if a=='(':
                x+=1
            if a==')':
                x-=1
            if a==',' :
                if x==0:
                    fields[i].append(data[pos:j])
                    if  data[j+1]==" ":
                        pos=j+2
                    else:
                        pos=j+1
            if j == len(data) - 1:
                fields[i].append(data[pos:j])
            j+=1
        i+=1
    list=[]
    for i in xrange(0, len(names)):
        list.append([])
        list[i].append(names[i])
        list[i].append(emails[i])
        list[i].append(links[i])
        list[i].append('------------')
        list[i].append(fields[i])

    i = 0
    k = 0
    for x in list:
        count = 0
        for y in x[4]:
            rat = fuzz.partial_ratio(interest.lower(), y.lower())
            if count == 1:
                break
            if rat >= 90:
                final_list.append({})
                final_list[k]['name'] = names[i].strip()
                final_list[k]['email'] = emails[i].strip()
                final_list[k]['link'] = links[i].strip()
                final_list[k]['contact_detail'] = '-------'
                final_list[k]['field'] = fields[i]
                count += 1
                k = k + 1
        i += 1

    for i in xrange(0, k):
        print final_list[i]
    return final_list

if __name__ == '__main__':
    data = raw_input("Enter Your Intern Interest(Topics):")
    tmp=correctexp(data)
    get_data_iitr("http://www.iitr.ac.in/departments/EE/pages/Faculty_List.html",tmp)
