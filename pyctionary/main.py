import numpy as np
import subprocess
from os import system, name
from time import sleep
from random import *
words = [ 'Swing', 'Coat', 'Shoe', 'Ocean', 'Dog', 'Mouth', 'Milk', 'Duck', 'Skateboard', 'Bird', 'Mouse', 'Whale', 'Jacket', 'Shirt', 'Hippo', 'Beach', 'Egg', 'Cookie', 'Cheese', 'Skip', 'Drum', 'homework', 'glue', 'eraser', 'peace', 'panic', 'alarm', 'far', 'comfy', 'dripping', 'boring', 'hot', 'cold', 'parents', 'closet', 'laugh', 'falling', 'sleepover', 'calendar', 'sunscreen', 'panda', 'detention', 'hair', 'ice skating', 'afraid', 'dictionary', 'homerun', 'root beer float', 'hibernation', 'street sweeper', 'spitball', 'drinking fountain', 'imagination', 'Angry', 'Fireworks', 'Pumpkin', 'Baby', 'Flower', 'Rainbow', 'Beard', 'Flying saucer', 'Recycle', 'Bible', 'Giraffe', 'Sand castle', 'Bikini', 'Glasses', 'Snowflake', 'Book', 'High heel', 'Stairs', 'Bucket', 'Ice cream cone', 'Starfish', 'Bumble bee', 'Igloo', 'Strawberry', 'Butterfly', 'Lady bug', 'Sun', 'Camera', 'Lamp', 'Tire', 'Cat', 'Lion', 'Toast', 'Church', 'Mailbox', 'Toothbrush', 'Crayon', 'Night', 'Toothpaste', 'Dolphin', 'Nose', 'Truck', 'Egg', 'Olympics', 'Volleyball', 'Eiffel Tower', 'Peanut', 'half cardboard', 'oar', 'baby-sitter', 'drip', 'shampoo', 'point', 'time machine', 'yardstick', 'think', 'lace darts', 'world', 'avocado bleach', 'shower', 'curtain', 'extension cord dent', 'birthday lap', 'sandbox', 'bruise', 'quicksand', 'fog', 'gasoline', 'pocket', 'honk', 'sponge', 'rim', 'bride', 'wig', 'zipper', 'wag', 'letter opener', 'fiddle', 'water buffalo', 'pilot', 'brand pail', 'baguette', 'rib mascot', 'fireman', 'pole zoo sushi', 'fizz ceiling', 'fan bald', 'banister punk', 'post office', 'season', 'Internet', 'chess', 'puppet', 'chime', 'ivy' ]
wordsHard = [ 'applause', 'application', 'avocato', 'award', 'badge', 'baggage', 'baker', 'barber', 'bargain', 'basket', 'bedbug', 'bettle', 'beggar', 'birthday', 'biscuit', 'bleach', 'blinds', 'bobsled', 'Bonnet', 'bookend', 'boundary', 'brain', 'bruise', 'bubble', 'Brain', 'Kitten', 'Playground', 'Bubble bath', 'Kiwi', 'Pumpkin pie', 'Buckle', 'Lipstick', 'Raindrop', 'Bus', 'Lobster', 'Robot', 'Car accident', 'Lollipop', 'Sand castle', 'Castle', 'Magnet', 'Slipper', 'Chain saw', 'Megaphone', 'Snowball', 'Circus tent', 'Mermaid', 'Sprinkler', 'Computer', 'Minivan', 'Statue of Liberty', 'Crib', 'Mount Rushmore', 'Tadpole', 'Dragon', 'Music', 'Teepee', 'Dumbbell', 'North pole', 'Telescope', 'Eel', 'Nurse', 'Train', 'Ferris wheel', 'Owl', 'Tricycle', 'Flag', 'Pacifier', 'Tutu', 'Junk mail', 'Piano', 'Garbage', 'Park', 'Pirate', 'Ski', 'Whistle', 'State', 'Baseball', 'Coal', 'Queen', 'Photograph', 'Computer', 'Hockey', 'Hot Dog', 'Salt and Pepper', 'iPad', 'Frog', 'Lawnmower', 'Mattress', 'Pinwheel', 'Cake', 'Circus', 'Battery', 'Mailman', 'Cowboy', 'Password', 'Harry Potter', 'Teacher', 'George Washington', 'Justin Bieber', 'Batman', 'Spongebob', 'Zendaya', 'Superman', 'Thomas the Tank Engine', 'Ariana Grande', 'Wonder Woman', 'President Donald Trump', 'Nemo', 'Black Panther', 'Teenage Mutant Ninja Turtles', 'Incredible', 'Spiderman', 'Vampire', 'Andi Mack', 'Captain America', 'Selena Gomez', 'Back seat', 'Highchair', 'Rock band', 'Birthday', 'Hockey', 'Sasquatch', 'Black hole', 'Hotel', 'Scrambled eggs', 'Blizzard', 'Jump rope', 'Seat belt', 'Burrito', 'Koala', 'Skip', 'Captain', 'Leprechaun', 'Solar eclipse', 'Chandelier', 'Light', 'Space', 'Crib', 'Mask', 'Stethoscope', 'Cruise ship', 'Carry', 'Run', 'Jump', 'Swim', 'Skip', 'Fly', 'Row', 'Catch', 'Watch', 'Swing', 'Learn', 'Love', 'Drink', 'Burp', 'Eat', 'Read', 'Type', 'Download', 'Call', 'Snap', 'Text', 'Pose', 'Shout', 'Sleep', 'Scratch', 'Hug', 'Cut', 'Bang', 'Spit', 'Tie', 'Open', 'Listen', 'Write', 'Sing', 'Pray', 'Close', 'Dance', 'Dispatch', 'Trade', 'Drive', 'Unite', 'Multiply', 'Cook', 'Unplug', 'Purchase', 'Mechanic', 'Stork', 'Dance', 'Mom', 'Sunburn', 'Deodorant', 'Mr Potato Head', 'Thread', 'Facebook', 'Pantyhose', 'Tourist', 'Flat', 'Paper plate', 'United States', 'Frame', 'Photo', 'WIFI', 'Full moon', 'Pilgram', 'Zombie', 'Game', 'Pirate', 'business', 'cabin', 'cardboard', 'carpenter', 'carrot', 'catalog', 'ceiling', 'channel', 'charger', 'cheerleader', 'chef', 'chess', 'chestnut', 'chime', 'Chuck Norris', 'cliff', 'cloak', 'clog', 'coach', 'comedian', 'comfy', 'commercial', 'computer monitor', 'conversation', 'convertible', 'cowboy', 'cramp', 'criticize', 'cruise', 'crumbs', 'crust', 'cuff', 'cupcake', 'curtain', 'darkness', 'darts', 'dashboard', 'Bicycle', 'Skate', 'Electricity', 'Thief', 'Teapot', 'Deep', 'Spring', 'Nature', 'Shallow', 'Outside', 'America', 'Bow tie', 'Wax', 'Light Bulb', 'Music', 'Popsicle', 'Brain', 'Birthday Cake', 'Knee', 'Pineapple', 'Tusk', 'Sprinkler', 'Money', 'Pool', 'Lighthouse', 'Doormat', 'Face', 'Flute', 'Rug', 'Snowball', 'Purse' ]
def clearScreen() :
    # for Windows
    if name == 'nt' :
        _ = system('cls')
    # for Linux and macOS
    else :
        _ = system('clear')
def buildTeams() :
    teamsComplete = False
    i = 2
    global teams
    teams = [input('Enter a team name: ')]
    teams.append(input('Enter another team name: '))
    while teamsComplete == False :
        teams.append(input('Enter another team name, or enter "Done" if there are no more teams: '))
        if teams[i] == 'Done' or teams[i] == 'done':
            teamsComplete = True
            break
        i = i + 1
    j = 0
    global players
    players = []
    for team in teams[0:len(teams)-1] :
        players.append([team])
        playersComplete = False
        i = 2
        players[j].append(input('Who is on team '+team+'?: '))
        while playersComplete == False :
            players[j].append(input('Who else is on '+team+' ("Done" if there are no more players)?: '))
            if players[j][i] == 'Done' or players[j][i] == 'done':
                playersComplete = True
            i = i + 1
        j = j + 1
def play(var, tm, pl) :
    roundScore = 0
    word = sample(words, 1)
    msg = input(str(tm)+' are up, with '+str(pl)+' drawing\n Hide the screen from your teammates and press ENTER/RETURN for your word\n')
    clearScreen()
    msg = input('The word is\n"'+word[0]+'"\nPress ENTER/RETURN and start drawing...')
    clearScreen()
    strTimer = '............................................................|'
    dt = 0
    for char in strTimer.split('.'):
        print(strTimer[0:dt])
        sleep(1)
        dt = dt + 1
        clearScreen()
    subprocess.call(["afplay","./sounds/buzzer.mp3"])
    msgScore = input('Did your team guess the word within the time limit? (yes/no): ')
    if msgScore == 'yes' or msgScore == 'Yes' :
        print('Great job '+str(pl)+'! '+str(tm)+'\'s score is now',var + 1)
        return var + 1
    else :
        return var
# Initialise the game
buildTeams()
gameQuit = False
i = 0
score = []
for team in teams[0:len(teams)-1]:
    score.append(0)
# Play the game
print('\nFantastic! Let\'s play, here are our teams')
for team in teams[0:len(teams)-1] :
    strPlayers = ''
    for player in players[i][1:len(players[i])-1] :
        strPlayers = strPlayers + str(player) + '\n'
    print(team + ':\n' + strPlayers)
    i = i + 1
k = 0
m = 1
n = 0
while gameQuit is False :
    score[k] = play(score[k],teams[k],players[k][m])
    msg = input('That was fun, press ENTER/RETURN to play again, or enter "Quit" to end the game: ')
    if msg == 'quit' or msg == 'Quit' :
        print('Great game everyone!')
        for team in teams[0:len(teams)-1]:
            print(str(teams[n])+' scored '+str(score[n]))
            n = n + 1
        quit()
    k = k + 1
    if k > len(teams) - 2 :
        k = 0
        m = m + 1
        if m > len(players[k]) - 1 :
            m = 1