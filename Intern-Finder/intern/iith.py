
import requests
from bs4 import BeautifulSoup
from api import correctexp
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def get_data_iith(url,interest):
    url = str(url)
    interest= str(interest)
    print interest
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    contact_details=[]
    names=[]
    research=[]
    emails=[]
    links=[]
    projects = []

    for id in soup.find_all("a",href=True):
        if "iith.ac.in/" in id['href']:
            links.append(id['href'])
        if "/joomla/" == id['href']:
            links.append("http://ee.iith.ac.in/joomla/index.php/en/")
        if "joomla/.." in id['href']:
            tmp=id['href']
            links.append("http://ee.iith.ac.in"+tmp[10:])
    links.pop(0)

    for id1 in soup.find_all("font",{'color':"#990000"}):
        names.append(id1.text)

    names.pop()
    names.pop()
    names.pop()
    links.pop()
    links.pop()
    links.pop()

    for x in soup.find_all("td"):
        id3=x.text
        a=id3.find("Micro")
        b=id3.find("PEPS")
        c=id3.find("SysCon")
        d=id3.find("CSP")
        if a!= -1:
            projects.append(id3[a+7:])
            continue
        if b!= -1:
            projects.append(id3[b+6:])
            continue
        if c!= -1:
            projects.append(id3[c+8:])
            continue
        if d!= -1:
            projects.append(id3[d+5:])
            continue

    i=1
    y=len(projects)/2
    for j in xrange(0,y):
        pr=projects[i]
        research.append(pr)
        i=i+2

    fields = []  # 2-d array which consists all research areas in a list on that index!
    i = 0
    for data in research:
        pos = 0
        fields.append([])
        j = 0
        x = 0
        for a in data:
            if a == '(':
                x += 1
            if a == ')':
                x -= 1
            if a == ',':
                if x == 0:
                    fields[i].append(data[pos:j])
                    if data[j + 1] == " ":
                        pos = j + 2
                    else:
                        pos = j + 1
            if j == len(data) - 1:
                fields[i].append(data[pos:j])
            j += 1
        i += 1

    list = []
    for i in xrange(0, len(names)):
        list.append([])
        list[i].append(names[i])
        list[i].append('-------')
        list[i].append(links[i])
        list[i].append('------------')
        list[i].append(fields[i])

    i = 0
    k = 0
    final_list = []
    for x in list:
        count = 0
        for y in x[4]:
            rat = fuzz.partial_ratio(interest.lower(), y.lower())
            if count == 1:
                break
            if rat >= 90:
                final_list.append({})
                final_list[k]['name'] = names[i]
                final_list[k]['email'] = '--------'
                final_list[k]['link'] = links[i]
                final_list[k]['contact_detail'] = '------------'
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
    get_data_iith("http://ee.iith.ac.in/joomla/index.php/en/people",tmp)
