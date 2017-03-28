import requests
from bs4 import BeautifulSoup
from api import correctexp
from fuzzywuzzy import fuzz
from pprint import pprint
def get_data_iitm(url, interest):
    url = str(url)
    interest = str(interest)
    print interest
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    contact_details = []
    names = []
    research = []
    emails = []
    links=[]
    for id in soup.find_all("a",href=True):
        if 'http://www.ee.iitm.ac.in/user/' in id['href']:
            print id['href']
            links.append(id['href'])

    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        names.append(tds[1].text.strip())
        contact_details.append(("+91 44 2257"+tds[2].text).strip())
        emails.append((tds[3].text+"@ee.iitm.ac.in").strip())
        research.append(tds[5].text)

    contact_details.pop(0)
    names.pop(0)
    research.pop(0)
    emails.pop(0)

    fields = []  # 2-d array which consists all research areas in a list on that index!
    pos = 0
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

    i = 0
    k = 0
    final_list = []
    for x in xrange(0,len(names)):
        count = 0
        for y in fields[i]:
            rat = fuzz.partial_ratio(interest.lower(), y.lower())
            if count == 1:
                break
            if rat >= 90:
                final_list.append({})
                final_list[k]['name'] = names[i]
                final_list[k]['email'] = emails[i]
                final_list[k]['link'] = links[i]
                final_list[k]['contact_detail'] = contact_details[i]
                final_list[k]['field'] = fields[i]
                count += 1
                k = k + 1
        i += 1
    pprint(final_list)
    return final_list

if __name__ == '__main__':
    data = raw_input("Enter Your Intern Interest(Topics):")
    tmp = correctexp(data)
    list=get_data_iitm("http://www.ee.iitm.ac.in/faculty-members/", tmp)
