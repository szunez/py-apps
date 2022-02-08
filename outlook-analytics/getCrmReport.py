import win32com.client
import os
from pathlib import Path
from datetime import datetime, timedelta
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
outbox = mapi.GetDefaultFolder(4)
sent = mapi.GetDefaultFolder(5).Items
inbox = mapi.GetDefaultFolder(6)
support = mapi.Folders(1).Folders(7).Folders(1).Items
accounts = mapi.Folders(1).Folders(27).Folders(3).Folders
#Folder enums
e = 1
for f in list(mapi.Folders(1).Folders) :
    print(e,f)
    e = e + 1
# 1 Deleted Items
# 2 Inbox
# 3 Outbox
# 4 Sent Items
# 5 ExternalContacts
# 6 HR
# 7 IT
# 8 Journal
# 9 Notes
#10 PersonMetadata
#11 Quick Step Settings
#12 RSS Feeds
#13 Social Activity Notifications
#14 Sync Issues
#15 updates
#16 Yammer Root
#17 Files
#18 Snoozed
#19 Conversation History
#20 Drafts
#21 Junk Email
#22 Tasks
#23 Contacts
#24 Conversation Action Settings
#25 Calendar
#26 Archive
#27 BD | 27.3 accounts
#28 News
#reportFolder = Path(os.path.expanduser('~')+'/src/py-apps/reports/')
os.chdir('C:\src\py-apps\outlook-analytics')
reportFile = open('./reports/report.csv','w')
reportFile.write('Client,Date sent,To,From\n')
for i in range(1, len(accounts)) :
    reportFile.write(str(accounts(i))+'\n')
    for msg in list(mapi.Folders(1).Folders(27).Folders(3).Folders(i).Items) :
        try : 
            reportFile.write(','+str(msg.ReceivedTime.strftime("%Y-%m-%d"))+',"'+str(msg.To)+'","'+str(msg.SenderName)+'"\n')
        except :
            reportFile.write(',,message details are not available\n')
reportFile.close()
quit()