import requests
import os
import urllib.request

#webUrl = urllib.request.urlopen('https://www.hcdistrictclerk.com/eDocs/Public/Search.aspx')
webUrl = urllib.request.urlopen('https://www.youtube.com/user/guru99com')
print("reqsut code: " + str(webUrl.getcode()))