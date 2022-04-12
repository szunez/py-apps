from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
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
    url="https://www.formula1.com/en/teams/"+teams[i]+".html"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find_all('td')
    j = 0
    for d in data :
        data[j] = re.sub("<.*?>", "", str(d))
        j = j + 1
    print(teams[i])
    print('World Championships=',data[7])
    print('Pole Postions =',data[9])
    print('Fastest Laps =',data[10],'\n')
    i = i + 1