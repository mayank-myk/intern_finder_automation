import requests
from bs4 import BeautifulSoup
from pprint import pprint
import urllib2


def get_data(url):
    url=str(url)
    url=url+"100001313875181"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')

    names=[]    #Names of all the proffessors
    print url
    for link in soup.findAll('span',{'class':"alternate-name"}):
        names.append(link.text)
        print link.text
        print '1'

    print '1'
if __name__ == '__main__':
    get_data("https://www.facebook.com/profile.php?id=")
