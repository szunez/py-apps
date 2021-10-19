import string
import secrets
import sys
from os import system, name
import subprocess
def copyCmd() :
    global cpCmd
    # for Windows
    if name == 'nt' :
        cpCmd = 'clip.exe'
    # for Linux and macOS
    else :
        cpCmd = 'pbcopy'
def genPassword(n) :
    alphabet = string.ascii_letters + string.digits
    ifspecial = input('\nWould you like to include special characters? (yes/no): ')
    if ifspecial[0] == 'y' or ifspecial[0] == 'Y' :
        alphabet = alphabet + '!@#$%^&*()_+'
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(n))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    p = subprocess.Popen(cpCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    p.communicate(password)
    p.wait()
    ifshow = input('\nWould you like to see your new password now? (yes/no): ')
    if ifshow[0] == 'y' or ifshow[0] == 'Y':
        print('\n')
        sys.stdout.write(password)
        print('\n')
intChar=int(input('\nEnter an integer number character length for your password: '))
copyCmd()
genPassword(intChar)