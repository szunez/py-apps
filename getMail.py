import win32com.client
import os
from datetime import datetime, timedelta
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")
for idx, folder in enumerate(mapi.Folders(1).Folders(7).Folders(1).Folders(1).Folders): 
    print(idx+1, folder)
outbox = mapi.GetDefaultFolder(4)
sent = mapi.GetDefaultFolder(5).Items
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
    if '"UPN"=>"' in msg.Body :
        findAfter = '"UPN"=>"'
        findUntil = '"}'
        startChar = msg.Body.find(findAfter)+len(findAfter)
        endChar = startChar + msg.Body[msg.Body.find(findAfter)+len(findAfter):len(msg.Body)].find(findUntil)
        customerEmail = msg.Body[startChar:endChar]
        if customerEmail.find('evoleap.') > 0 \
        or customerEmail.find('.xom.com') > 0 \
        or customerEmail.find('@genesisenergies.') > 0 \
        or customerEmail.find('@galp.') > 0 \
        or customerEmail.find('@technip.') > 0 \
        or customerEmail.find('@technipfmc.') > 0 \
        or customerEmail.find('@xodusgroup.') > 0 \
        or customerEmail.find('@afs.') > 0 \
        or customerEmail.find('@wintershalldea.') > 0 \
        or customerEmail.find('@gate.') > 0 \
        or customerEmail.find('@rosen-group.') > 0 \
        or customerEmail.find('quantaservices.com') > 0 \
        or customerEmail.find('blade-energy.com') > 0 \
        or customerEmail.find('@nwe.northwesternenergy.com') > 0 \
        or customerEmail.find('.local') > 0 \
        or customerEmail.find('@wecenergygroup.com') > 0 \
        or customerEmail.find('@nustarenergy.com') > 0 \
        or customerEmail.find('@global.cnooc.corp') > 0 \
        or customerEmail.find('"Organization"=>"Air Liquide') > 0 \
        or customerEmail.find('"Organization"=>"Energean') > 0 :
            continue
        else:
            if db.count(str(customerEmail).lower()) == 0 :
                db.append(str(customerEmail).lower())
i = 0
for data in list(db) :
        print(data)
        i = i + 1
print('\n',i-1,'unique customer email addresses were found\n')
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
        if db.count(str(contactedCustomer).lower()) != 0 :
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
print('\n',k-1,'customers to contact\n')