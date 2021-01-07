import os
from pathlib import Path

def getFeedback() :
    global i, team, feedback, finalCheck
    i = 0
    team = [input('\nEnter the name of the person to be evaluated: ')]
    if team[i] == 'quit' :
        quit()
    feedback = [input('Enter your feedback/comments for '+team[i]+': ')]
    i = i + 1
    while team[i-1] != 'quit' :      
        team.append(input('\nEnter the name of the person to be evaluated, or enter "quit": '))
        if team[i] == 'quit' :
            break
        else :
            feedback.append(input('Enter your feedback/comments for '+team[i]+': '))
            i = i + 1
    print('\nPlease review your feedback:')
    print('================================================================================')
    for j in range(i) :
        print(team[j]+' : '+feedback[j])
    print('================================================================================')
    finalCheck = input('Are you satisfied with your comments above? (yes/no): ')

def writeReport() :
    if finalCheck[0] == 'y' :
        for k in range(i) :
            reportFolder = Path(os.path.expanduser('~')+'/src/py-apps/threesixty/')
            reportFile = open(reportFolder / 'report.txt','a')
            reportFile.write(team[k]+' : '+feedback[k]+'\n')
        reportFile.close()
        quit()
    else:
        getFeedback()

getFeedback()
writeReport()
if finalCheck[0] == 'y' :
    writeReport()
else :
    quitWithoutSaving = input('Quit without saving comments? (yes/no): ')
    if quitWithoutSaving[0] == 'y' :
        quit()
    else :
        getFeedback()
        writeReport()