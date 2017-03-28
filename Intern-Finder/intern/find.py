import requests
from bs4 import BeautifulSoup
from api import correctexp
from fuzzywuzzy import fuzz
from pprint import pprint


def get_data_iitd(url, interest):
    url = str(url)
    interest = str(interest)
    print interest
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    details = []
    contact_details = []
    names = []
    research = []
    emails = []
    links = []

    for id in soup.find_all("a", href=True):
        if "./" in id['href']:
            if "Dr." in id.text:
                links.append("http://ee.iitd.ernet.in/people" + id['href'].replace("./", "/"))
                names.append(id.text.replace("\n", ""))

    for name in soup.find_all("td", {'width': '70%'}):
        details.append(name.text)
        tmp = name.text
        a = tmp.find("Area")
        p = tmp.find("Phone")
        e = tmp.find("Email")
        research.append(tmp[a + 5:])
        contact_details.append(tmp[p:e].replace("\n", ""))
        emails.append(tmp[e:a - 9].replace("\n", ""))

    research.pop(0)
    emails.pop(0)
    contact_details.pop(0)

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

    list = []
    for i in xrange(0, len(names)):
        list.append([])
        list[i].append(names[i].strip())
        list[i].append(emails[i].strip())
        list[i].append(links[i].strip())
        list[i].append(contact_details[i].strip())
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
            if rat >= 80:
                final_list.append({})
                final_list[k]['name'] = names[i]
                final_list[k]['email'] = emails[i]
                final_list[k]['link'] = links[i]
                final_list[k]['contact_detail'] = contact_details[i]
                final_list[k]['field'] = fields[i]
                count += 1
                k = k + 1
        i += 1
    #pprint(final_list)
    return final_list


if __name__ == '__main__':
    data = raw_input("Enter Your Intern Interest(Topics):")
    tmp = correctexp(data)
    list=get_data_iitd("http://ee.iitd.ernet.in/people/faculty.html", tmp)
