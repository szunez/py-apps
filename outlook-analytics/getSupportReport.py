import win32com.client
import os
from pathlib import Path
from datetime import datetime, timedelta
os.chdir('C:\src\py-apps\outlook-analytics')
with open('supportReport.ignore') as f :
    ignorefile = f.readlines()
    ignorelist = []
    for val in list(ignorefile) :
        ignorelist.append(val.strip())
f.close()
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
#this is code to print out folder names in a given root folder
# #for idx, folder in enumerate(mapi.Folders(1).Folders(7).Folders(1).Folders): 
#    print(idx+1, folder)
outbox = mapi.GetDefaultFolder(4)
#sent = mapi.GetDefaultFolder(5).Items
#27.1.3 : BD/verticals/midstream
sent = mapi.Folders(1).Folders(27).Folders(1).Folders(3).Items
inbox = mapi.GetDefaultFolder(6)
messages = mapi.Folders(1).Folders(7).Folders(1).Items
#received_dt = datetime.now() - timedelta(days=1)
#received_dt = received_dt.strftime('%m/%d/%Y %H:%M %p')
#messages = messages.Restrict("[ReceivedTime] >= '" + received_dt + "'")
#messages = messages.Restrict("[SenderEmailAddress] = 'contact@codeforests.com'")
#messages = messages.Restrict("[Subject] = 'Sample Report'")
db = []
db_contacted = []
for msg in list(messages) :
    ignoreCustomer = False
    if '"UPN"=>"' in msg.Body :
        findAfter = '"UPN"=>"'
        findUntil = '"}'
        startChar = msg.Body.find(findAfter)+len(findAfter)
        endChar = startChar + msg.Body[msg.Body.find(findAfter)+len(findAfter):len(msg.Body)].find(findUntil)
        customerEmail = msg.Body[startChar:endChar]
    elif '"email"=>"' in msg.Body :
        findAfter = '"email"=>"'
        findUntil = '"}'
        startChar = msg.Body.find(findAfter)+len(findAfter)
        endChar = startChar + msg.Body[msg.Body.find(findAfter)+len(findAfter):len(msg.Body)].find(findUntil)
        customerEmail = msg.Body[startChar:endChar]
    else :
        continue
    if not customerEmail.find('@') >= 0 :
        ignoreCustomer = True
    for ign in ignorelist :
        if str(customerEmail.lower()).find(ign.lower()) >= 0 :
            ignoreCustomer = True
    if ignoreCustomer == False and db.count(str(customerEmail).lower()) == 0 :
        db.append(str(customerEmail).lower())
i = 0
for data in list(db) :
        print(data)
        i = i + 1
print('\n',i,'unique customer email addresses were found\n')
j = 0
for snt in list(sent) :
    recipients = snt.Recipients
    recipients_list = []
    for r in recipients:
        recipients_list.append(r)
    for recipient in recipients_list:    
        try:
            #contactedCustomer = recipient.AddressEntry.GetExchangeUser().PrimarySmtpAddress
            contactedCustomer = str(recipient.Address).lower()
        except:
            continue
        if db.count(str(contactedCustomer).lower()) != 0 and db_contacted.count(str(contactedCustomer).lower()) == 0 :
            db_contacted.append(str(contactedCustomer).lower())
            print(contactedCustomer)
            j = j + 1
print('\n',j,'customers have been contacted\n')
uncontactedCustomers = set(db)- set(db_contacted)
k = 0
for uncontacted in uncontactedCustomers :
    if uncontacted.find('evoleap.') > 0 :
        continue
    else:
        print(uncontacted)
        k = k + 1
print('\n',k,'customers to contact\n')