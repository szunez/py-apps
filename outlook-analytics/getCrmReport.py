import win32com.client
import os
from pathlib import Path
from datetime import datetime, timedelta
def debug() :
    outlook = win32com.client.Dispatch('outlook.application')
    mapi = outlook.GetNamespace("MAPI")
    accounts = outlook.Session.Accounts
    for account in accounts:
        print("Account:", account.DisplayName)
        for folder in account.DeliveryStore.GetRootFolder().Folders:
            print("Folder:", folder.Name)
    quit()
def enums(n_mailbox, fldr, subfldr) :
    e = 1
    if fldr == "":
        for f in list(mapi.Folders(n_mailbox).Folders) :
            print(e,f)
            e = e + 1
    elif subfldr == "":
        for f in list(mapi.Folders(n_mailbox).Folders(fldr).Folders) :
            print(e,f)
            e = e + 1
    else:
        for f in list(mapi.Folders(n_mailbox).Folders(fldr).Folders(subfldr).Folders) :
            print(e,f)
            e = e + 1
    return
n_mailbox = 3 #set this if to the mailbox of interest, if there are multiple mailboxes for the account
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
customers = mapi.Folders(n_mailbox).Folders(27).Folders(3).Folders
reportFolder = Path(os.path.expanduser('~')+'/src/py-apps/reports/')
os.chdir('C:\src\py-apps\outlook-analytics')
reportFile = open('./reports/report.csv','w')
reportFile.write('Client,Date sent,To,From\n')
for i in range(1, len(customers)) :
    reportFile.write(str(customers(i))+'\n')
    for msg in list(mapi.Folders(n_mailbox).Folders(27).Folders(3).Folders(i).Items) :
        try : 
            reportFile.write(','+str(msg.ReceivedTime.strftime("%Y-%m-%d"))+',"'+str(msg.To)+'","'+str(msg.SenderName)+'"\n')
        except :
            reportFile.write(',,message details are not available\n')
reportFile.close()
print('email scan is completed.')
quit()