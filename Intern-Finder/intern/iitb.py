#iitbombay
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from api import correctexp

def get_data_iitb(url,interest):
    url = str(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    interest = str(interest)

    links=[]
    names=[]
    emails = []
    research=[]
    final_list=[]
    contact_details=[]
    list = []
    fields = []  # 2-d array which consists all research areas in a list on that index!

    for b in soup.find_all('a',{'class':'fac_name'}):
        names.append(b.text)

    for c in soup.find_all('td',{'colspan':'2'}):
        tmp=c.text
        z=tmp.find("Research Interests:")
        if z == -1:
            research.append("NULL")
        else:
            research.append(tmp[z+20:])
        x=tmp.find("Email:")
        if x==-1:
            emails.append("NULL")
        else:
            emails.append(tmp[x+7:z].strip().replace("[AT]",""))
        y=tmp.find("+")
        if y==-1:
            contact_details.append("NULL")
        else:
            contact_details.append(tmp[y:x-3])

    for a in soup.find_all('a', href=True):
        if "faculty/homepage" in a['href']:
            links.append(a['href'])

    i=0
    for data in research:
        pos=0
        fields.append([])
        j=0
        x=0
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

    for i in xrange(0, len(names)):
        list.append([])
        list[i].append(names[i].strip())
        list[i].append(emails[i].strip())
        list[i].append(links[i].strip())
        list[i].append(contact_details[i].strip())
        list[i].append(fields[i])

    i = 0
    k = 0
    for x in list:
        count = 0
        for y in x[4]:
            rat = fuzz.partial_ratio(interest.lower(), y.lower())
            if count >= 1:
                break
            if rat >= 90:
                final_list.append({})
                final_list[k]['name']=names[i]
                final_list[k]['email']=emails[i]
                final_list[k]['link']=links[i]
                final_list[k]['contact_detail'] =contact_details[i]
                final_list[k]['field']=fields[i]
                count += 1
                k = k + 1
        i += 1

    return final_list

if __name__ == '__main__':
    data = raw_input("Enter Your Intern Interest(Topics):")
    tmp = correctexp(data)
    get_data_iitb("https://www.ee.iitb.ac.in/web/people/faculty/",tmp)
