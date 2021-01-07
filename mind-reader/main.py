import random
import numpy as np
from os import system, name
from time import sleep 

def accGuess(n) :
    global guess
    guess = card[n][0][0] + guess
    return guess

def clearScreen() :
    # for Windows
    if name == 'nt' :
        _ = sytem('cls')
    # for Linux and macOS
    else :
        _ = system('clear')
card = np.zeros((6,4,8))
choice = 'n'
guess = 0.
i = 0
card[0] = np.array([[
    1, 3, 5, 7, 9, 11, 13, 15],
    [17, 19, 21, 23, 25, 27, 29, 31],
    [33, 35, 37, 39, 41, 43, 45, 47],
    [49, 51, 53, 55, 57, 59, 61, 63]
])
card[1] = np.array([
    [2, 3, 6, 7, 10, 11, 14, 15],
    [18, 19, 22, 23, 26, 27, 30, 31],
    [34, 35, 38, 39, 42, 43, 46, 47],
    [50, 51, 54, 55, 58, 59, 62, 63]
])
card[2] = np.array([
    [4, 5, 6, 7, 12, 13, 14, 15],
    [20, 21, 22, 23, 28, 29, 30, 31],
    [36, 37, 38, 39, 44, 45, 46, 47],
    [52, 53, 54, 55, 60, 61, 62, 63]
])
card[3] = np.array([
    [8, 9, 10, 11, 12, 13, 14, 15],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [56, 57, 58, 59, 60, 61, 62, 63]
])
card[4] = np.array([
    [16, 17, 18, 19, 20, 21, 22, 23],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [56, 57, 58, 59, 60, 61, 62, 63]
])
card[5] = np.array([
    [32, 33, 34, 35, 36, 37, 38, 39],
    [40, 41, 42, 43, 44, 45, 46, 47],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [56, 57, 58, 59, 60, 61, 62, 63]
])
ncard = random.randint(0,5)
print("\nHello there, I am a super computer and I will read your mind!!!")
believe = input('Do you want me to show you my powers? (y/n): ')
if believe[0] == 'y' or believe[0] == 'Y':
    clearScreen()
    print("Excellent, let\'s get started...\n")
    print("\nSelect a number from this card\n", card[ncard])
    input("\nPress ENTER once your number is memorised: ")
    clearScreen()
    print("\n...\nyes...I am starting to see into your mind...\n")
    sleep(2)
    accGuess(ncard)

    while i < 6 :
        if i == ncard :
            i = i + 1
        else :
            clearScreen()
            print('\n')
            print(card[i])
            choice = input("\nIs your number shown above? (y/n): ")
            if choice[0] == 'y' or choice[0] == 'Y' :
                accGuess(i)
            i = i + 1
    clearScreen()
    print('\nOkay, in that case the number you chose was',guess,'\n')
    confirmation = input('Am I correct? (y/n): ')
    clearScreen()
    if confirmation[0] == 'y' or confirmation[0] == 'Y' :
        print("\nOf course, that\'s what I thought!\n")
    else :
        print("\nHmmm...let me double check...")
        sleep(2)
        print("My analysis shows that you have failed to account for one or more cards,\n Yo bad!\n")
else:
    clearScreen()
    print("\nHahahahah, I knew you where afraid...\nfeeble mortal...\n AWAY WITH YOU!!!\n")