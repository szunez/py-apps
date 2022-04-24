from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('colheader_justify', 'left')
def help() :
    print('\nRetrieve, process and summarise data published on www.formula1.com')
    print('Available functions include:\n    getteammetrics()\n    getdriverstanding()\n    getteamstanding()\n    getreacedata()')
    print('\nUsage example:\n>>>python -c \'import formula1 as f1; f1.getdriverstanding()\'')
def getdata(url) :
    global data
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all('td')
def cleandata() :
    j = 0
    for d in data :
        data[j] = re.sub("<.*?>", "", str(d))
        data[j] = data[j].replace("\n", "")
        j = j + 1
def getteammetrics() :
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
    i = 0
    for t in teams :
        getdata("https://www.formula1.com/en/teams/"+teams[i]+".html")
        cleandata()
        j = 0
        for d in data :
            data[j] = re.sub("<.*?>", "", str(d))
            j = j + 1
        print(teams[i])
        print('World Championships =',data[7])
        print('Pole Postions =',data[9])
        print('Fastest Laps =',data[10],'\n')
        i = i + 1
    quit()
def getdriverstanding() :
    getdata("https://www.formula1.com/en/results.html/2022/drivers.html")
    cleandata()
    i = 0
    pos = []
    driver = []
    car = []
    pts = []
    n=7
    for i in range(0,int(len(data)/n)) :
        pos.append(data[1+i*n])
        driver.append(data[2+i*n])
        car.append(data[4+i*n])
        pts.append(data[5+i*n])
    s1 = pd.Series(pos)
    s2 = pd.Series(driver)
    s3 = pd.Series(car)
    s4 = pd.Series(pts)
    driver_standing = pd.DataFrame(list(zip(s1,s2,s3,s4)), columns=['POS','Driver','Car','PTS']).set_index('POS')
    print(driver_standing,'\n')
    quit()
def getteamstanding() :
    getdata("https://www.formula1.com/en/results.html/2022/team.html")
    cleandata()
    i = 0
    pos = []
    team = []
    pts = []
    n=5
    for i in range(0,int(len(data)/n)) :
        pos.append(data[1+i*n])
        team.append(data[2+i*n])
        pts.append(data[3+i*n])
    s1 = pd.Series(pos)
    s2 = pd.Series(team)
    s3 = pd.Series(pts)
    driver_standing = pd.DataFrame(list(zip(s1,s2,s3)), columns=['POS','Team','PTS']).set_index('POS')
    print(driver_standing,'\n')
    quit()
def getracedata() :
    getdata("https://www.formula1.com/en/results.html/2022/races.html")
    races = int(len(data)/8)
    racedata = np.empty([races,9,20], dtype='O')
    for r in range(0,races) :
        getdata("https://www.formula1.com/en/results.html/2022/races.html")
        start = str(data[1+r*8]).find("href") + len("href") + 2
        final = str(data[1+r*8]).find('.html">')+len(".html")
        getdata(str("https://www.formula1.com") + str(data[1+r*8])[start:final])
        cleandata()
        p = 0
        x = 0
        for d in data :
            racedata[r, x, p] = d
            x = x + 1
            if x > 8 :
                x = 0
                p = p + 1
    print(np.delete(racedata,[0,8],1))
    quit()