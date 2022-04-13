from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('colheader_justify', 'left')
def getdata(url) :
    global data
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all('td')
    j = 0
    for d in data :
        data[j] = re.sub("<.*?>", "", str(d))
        data[j] = data[j].replace("\n", "")
        j = j + 1
teams=["Ferrari", \
    "Mercedes", \
    "Red-Bull-Racing", \
    "McLaren", \
    "Alpine", \
    "Alfa-Romeo-Racing", \
    "Haas-F1-Team", \
    "AlphaTauri", \
    "Williams", \
    "Aston-Martin", \
]
getdata("https://www.formula1.com/en/results.html/2022/drivers.html")
i = 0
pos = []
driver = []
car = []
pts = []
for i in range(0,20) :
    pos.append(data[1+i*7])
    driver.append(data[2+i*7])
    car.append(data[4+i*7])
    pts.append(data[5+i*7])
i = 0
s1 = pd.Series(pos)
s2 = pd.Series(driver)
s3 = pd.Series(car)
s4 = pd.Series(pts)
driver_standing = pd.DataFrame(list(zip(s1,s2,s3,s4)), columns=['POS','Driver','Car','PTS']).set_index('POS')
print(driver_standing,'\n')
for t in teams :
    getdata("https://www.formula1.com/en/teams/"+teams[i]+".html")
    j = 0
    for d in data :
        data[j] = re.sub("<.*?>", "", str(d))
        j = j + 1
    print(teams[i])
    print('World Championships =',data[7])
    print('Pole Postions =',data[9])
    print('Fastest Laps =',data[10],'\n')
    i = i + 1