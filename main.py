#to randomize key order
from random import shuffle

#to end game
from sys import exit

#necessary presets; command input and initial points
plyrCom = None
points = 0

#other presets; initial room, key in inventory, and win condition. reset at beginning of game
rmID = 0
keyNum = 0
inventory = 0
plyrWin = False

#list of all possible keys; randomized at beginning of game
keyOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

#matches key number with color
invenDesc = ['red', 'vermillion', 'orange', 'amber', 'yellow', 'chartreuse', 'green', 'teal', 'blue', 'violet', 'purple', 'magenta']

#room header prints when player enters; order determines indez for each room
rmName = ['You face the north wall.', 'You face the south wall.', 'You face the east wall.', 'You face the west wall.']

#room description prints when player first enters room, and when player looks around
rmDesc = [['You see a red, vermillion, and orange lock.', 1], ['You see a green, teal, and blue lock.', 1], ['You see an amber, yellow, and chartreuse lock.', 1], ['You see a violet, purple, and magenta lock.', 1]]

#indicates how rooms connect to each other [north, south, east, west]; index is rmID
rmMap = [[None, 1, 2, 3], [0, None, 2, 3], [0, 1, None, 3], [0, 1, 2, None]]

#divide possible inputs based on command type
north = ['north', 'n']
south = ['south', 's']
east = ['east', 'e']
west = ['west', 'w']
move = ['go'] + north + south + east + west
look = ['look', 'l']
invenCheck = ['inventory', 'i']
useItem = ['use', 'u']
plyrHelp = ['help', 'h']
plyrPoints = ['point', 'p']
quit = ['quit', 'q']
yes = ['yes', 'y']

#prints room header, and room description on first entry
def rm():
    print(rmName[rmID] + '\n')
    if rmDesc[rmID][1] == 1:
        rmDesc[rmID][1] = 0
        lk()

#prints room description
def lk():
    print(rmDesc[rmID][0] + '\n')

#moves player in desired direction if possible
def mov():
    global plyrCom, rmID
    if any(i in plyrCom for i in north):
        ID = rmMap[rmID][0]
    elif any(i in plyrCom for i in south):
        ID = rmMap[rmID][1]
    elif any(i in plyrCom for i in east):
        ID = rmMap[rmID][2]
    elif any(i in plyrCom for i in west):
        ID = rmMap[rmID][3]
    
    #only permits movement is room index is integer (if room exists in intended direction)
    try:
        rmID = ID + 0
        rm()
    except:
        print('You slam into the wall.\n')

#checks what key is in inventory
def inven():
    print('You have the ' + invenDesc[inventory] + ' key.\n')

#uses key on nearby lock if possible
def use():
    global inventory, keyNum, plyrWin, points
    useValid = False
    
    #use if valid if player uses key near proper lock
    if rmID == 0 and inventory <= 2:
        useValid = True
    elif rmID == 2 and inventory >= 3 and inventory <= 5:
        useValid = True
    elif rmID == 1 and inventory >= 6 and inventory <= 8:
        useValid = True
    elif rmID == 3 and inventory >= 9:
        useValid = True
    
    if useValid == True:
        print('The key fits into a lock.', end='')
        
        #checks if player has won. triggers win condition is so, otherwise gives player next key
        if keyNum < 10:
            keyNum += 1
            points += 1
            inventory = keyOrder[keyNum]
            print(' You receive the ' + invenDesc[inventory] + ' key. You earned a point!\n')
        else:
            points += 10
            plyrWin = True
            
    else:
        print('The key does not fit into any lock.\n')

#gives spiel of different commands player can use
def giveHelp():
    print('Welcome to Escape! So, I may have been... overambitious, and procrastinated JUST a bit on this project, so in this game the objective is simply to go around the room and unlock all of the locks you see before you.\n')
    print('Here are the commands you can use:\n')
    print('Go [N]orth, [S]outh, [E]ast, or [W]est to move around the room\n')
    print('[L]ook around to view the locks around you\n')
    print('Check your [I]nventory to see what key you currently have\n')
    print('[U]se the key to see if you can unlock any locks\n')
    print('Check how many [P]oints you have earned\n')
    print('[Q]uit if you are done playing\n')
    print('And of course, ask for [H]elp if you need a refresher!\n')

#reads number of points player has
def pointCheck():
    print('You have ' + str(points) + ' points.\n')

#main function - asks player for input, and acts accordingly
def com():
    global plyrCom
    plyrCom = input('> ').lower().split()
    print('\n')
    
    #checks whether player input matches a function call. can probably (definitely) be more efficient, but I don't know switch statements yet!! 
    if any(i in plyrCom for i in quit):
        exit()
    elif any(i in plyrCom for i in plyrHelp):
        giveHelp()
    elif any(i in plyrCom for i in move):
        mov()
    elif any(i in plyrCom for i in look):
        lk()
    elif any(i in plyrCom for i in invenCheck):
        inven()
    elif any(i in plyrCom for i in useItem):
        use()
    elif any(i in plyrCom for i in plyrPoints):
        pointCheck()
    else:
        print('I beg your pardon?\n')

#tells player they have won, and prompts for additional playthrough
def win():
    print('\n\n\n\nCongratulations! You have earned ' + str(points) + ' points in total, and have opened all the locks!\n')
    print("...Anticlimatic, I know. But still, that's all you get. If you REALLY want to continue, just give me a clear [Y]es; otherwise we can get out of each other's way.\n")
    plyrCom = input('> ').lower().split()
    if any(i in plyrCom for i in yes):
        print('\nOh, alright then!\n\n')
        game()
    else:
        print('\nUntil next time!\n')
        exit()

#main game loop
def game():
    global rmID, keyNum, inventory, plyrWin, rmDesc
    
    #resets key order, initial room, inventory, and win condition
    shuffle(keyOrder)
    rmID = 0
    for x in range(4):
        rmDesc[x][1] = 1
    keyNum = 0
    inventory = 0
    plyrWin = False

    #initially reads off inventory and room description for player
    inven()
    rm()
    
    #prompts for input until player wins game
    while plyrWin == False:
        com()
    win()

#prints help prompt, since player does not yet know command
print('At any time, enter [H]elp for guidance\n\n')
game()
