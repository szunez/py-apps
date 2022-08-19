from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('colheader_justify', 'left')
def getdata(url, el) :
    global data
    if el == '' :
        el = 'td'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all(el)
def cleandata() :
    j = 0
    for d in data :
        data[j] = re.sub("<.*?>", "", str(d))
        data[j] = data[j].replace("\n", "")
        j = j + 1
def go(url, el, x0, xn, dx, z0, dz) :
    getdata(url, el)
    z1 = z0 + dz
    cleandata()
    for i in range(x0,xn) :
        print(data[z0+i*dx],data[z1+i*dx],"\n")
#go("https://www.reuters.com/business/energy/who-is-still-buying-russian-crude-oil-2022-03-21/", "p", 0, 32, 2, 10, 1)
#go("https://event.crowdcompass.com/psig2022/custom-list/RG93bmxvYWQgcGFwZXJz?title=Download%20papers", "li", 0, 1, 1, 1, 1)
getdata("https://event.crowdcompass.com/psig2022/custom-list/RG93bmxvYWQgcGFwZXJz?title=Download%20papers", "li")
print(data)