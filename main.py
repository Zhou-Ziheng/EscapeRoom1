#-----------------------------------------------------------------------------------
# Name: Tony Zhou
# Date: June 20, 2021
# Class Code: ICS4U
# Teacher: Mr. Asad
# Description: An Escape Room Game
# References: https://realpython.com/python3-object-oriented-programming/
              #
#-----------------------------------------------------------------------------------
import traceback
import pygame
import random


# from replit import audio


class Inventory:  # Instantiate a new class called Inventory

    # Constructor method that takes the x, y pos and the image
    def __init__(self, x, y, name, imageName="trans.png"):  # If no image is given, default to a transparent image
        self.x = x
        self.y = y
        self.name = name
        self.imageName = imageName
        self.smallImage = pygame.transform.scale(pygame.image.load(imageName), (60, 60))

    def getName(self):  # Gets the name of the object stored in the inventory slot
        return self.name

    def getSmallImage(self):  # Gets the icon image of the object stored in the inventory slot
        return self.smallImage

    def getX(self):  # Gets the x position of the icon slot
        return self.x

    def getY(self):  # Gets the y position of the icon slot
        return self.y

    def getRect(self):  # Gets the Rect object corresponding to the inventory slot
        return pygame.Rect(self.x, self.y, 70, 70)


def printMessage(message):  # Prints the message at the top of the screen
    sub = pygame.Surface((800, 50)).convert_alpha()  # Create a surface and converts it to alpha
    sub.fill((255, 255, 255, 200))  # fill the screen with a semi-transparent white strip
    screen.blit(sub, (0, 0))  # Blits the subscreen to the main screen
    text = getText(message, (40), (0, 0, 0))  # gets the text according to the given parameter
    screen.blit(text, (400 - text.get_width() / 2, 25 - text.get_height() / 2))  # Blits the text to the screen


def getMazeSolution():  # Gets the solution to the make
    sol = []  # Declare an array called sol

    # Make the 2d array 10 by 10 and assign value False to all the elements
    for i in range(10):
        sol.append([])
        for j in range(10):
            sol[i].append(False)

    # Individually assign each square on the correct path to True
    for i in range(5):
        sol[0][i] = True
    for i in range(4):
        sol[i][4] = True
    for i in range(4):
        sol[3][i] = True
    sol[4][0] = True
    for i in range(7):
        sol[5][i] = True
    sol[4][6] = True
    for i in range(6, 10):
        sol[3][i] = True
    for i in range(4, 7):
        sol[i][9] = True
    for i in range(10):
        sol[7][i] = True
    sol[8][0] = True
    for i in range(10):
        sol[9][i] = True
    return sol


# Get's a surface with text on it
def getText(str, size, color):
    pygame.font.init()  # Initialize font
    myFont = pygame.font.SysFont(None, size)  # Setting the font
    textSurface = myFont.render(str, False, color)  # Rendering the text
    return textSurface  # Return surface


# WHERE THE ACTUAL PROGRAM STARTS
pygame.init()  # Initialize pygame
pygame.mixer.init()  # Initialize pygame mixer for music

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 150, 150)

# Setting the screen size to 800 by 600
SIZE = (800, 600)
screen = pygame.display.set_mode(SIZE)

# loading the background image
background = pygame.image.load("escape room 2.jpg")
background = pygame.transform.scale(background, (800, 600))
running = True  # setting running to True for game loop
myClock = pygame.time.Clock()  # Instantiate an object of the Clock module
framecount = 0
password = str(random.randint(1000, 9999))  # Generate a random 4 digit number as the pin to the safe

# Hit box of all the interactives
safeHitBox = pygame.Rect(380, 230, 60, 37)
mazeHitBox = pygame.Rect(588, 445, 30, 25)
mugHitBox = pygame.Rect(177, 348, 26, 29)
paperHitBox = pygame.Rect(478, 367, 13, 10)
doorHitBox = pygame.Rect(439, 68, 84, 214)

# State Variables
success = False  # If the game is finished
safeOpened = False  # If the safe is unlocked
keyTaken = False  # If the key is taken from the safe
mazeSolved = False  # If the maze is solved
mazeAdded = False  # If the maze is added to the inventory
mugDiscovered = False  # If player discovered the mug
mugAdded = False  # If the mug has been added
paperDiscovered = False  # If the player discovered the slip of paper
paperAdded = False  # If the slip of paper is added to the inventory
doorOpened = False  # If the door opening sound has been played

inventorySize = 4  # Size of the inventory
inventory = []  # an array to store the Inventory objects
temporary = None  # A variable to store any temporary data

# The following block of code is only here to show that I can use file I/O
word = "SUCCESS"
file = open("success.txt", 'w')  # Open file success.txt with writing privelege
for i in word:
    file.write(i + "\n")  # Write each letter in success to the file
file.close()

# Initial message
message = "You are locked in a room. Find clues to escape!"

# Create four Inventory objects at correct postions and add them to a list
for i in range(260, 540, 70):
    inventory.append(Inventory(i, 530, None))

mazeSolution = getMazeSolution()  # Gets the solution of the maze
mazeGrid = []  # Gets the rect objects that makes up each tile in the maze
counter = 0  # Counter for the loop

for i in range(200, 600, 40):
    mazeGrid.append([])
    for j in range(100, 500, 40):
        mazeGrid[counter].append(pygame.Rect(i + 3, j + 3, 34, 34))  # Add each rect object to mazeGrid list
    counter += 1


# Draws the background
def draw_background(screen):
    screen.blit(background, (0, 0))


# Draws the inventory slots
def drawInventory(screen):
    for i in inventory:  # For each element in the list of Inventory objects
        transparent = pygame.Surface((70, 70)).convert_alpha()  # create a transparent surface of size 70 by 70
        pygame.draw.rect(transparent, (200, 200, 200, 200), (0, 0, 70, 70), 0)  # Draw a transluscent background
        pygame.draw.rect(transparent, (0, 0, 0, 255), (0, 0, 70, 70), 2)  # Draw a colored in border
        screen.blit(transparent, (i.getX(), i.getY()))  # Blit the surface to the main pygame screen
        screen.blit(i.getSmallImage(), (i.getX() + 5, i.getY() + 5))  # Blit the stored image to the main pygame screen


# Draws the safe
def drawSafe(screen):
    if safeOpened is False:  # If safe is not opened
        # draws the safe image at the proper location
        safe = pygame.image.load("safe.png")
        safe = pygame.transform.scale(safe, (safeHitBox.width, safeHitBox.height))
        screen.blit(safe, (safeHitBox.x, safeHitBox.y))
    else:  # If safe is opened
        # draws the safe image
        safe = pygame.image.load("safe.png")
        safe = pygame.transform.scale(safe, (safeHitBox.width, safeHitBox.height))
        screen.blit(safe, (safeHitBox.x, safeHitBox.y))

        # draws the interior of the safe
        screen.blit(pygame.transform.scale(pygame.image.load("safeInterior.png"), (50, 24)), (385, 238))
        if not keyTaken:  # if the key is not taken, draw the key as well
            screen.blit(pygame.transform.scale(pygame.image.load("key.png"), (30, 10)), (400, 250))


# Draw scene method that draws everything on the main window
def scene_draw(screen):
    draw_background(screen)
    # add your drawing functions here

    drawSafe(screen)
    drawInventory(screen)


# A function that draws the buttons
def drawButtons(buttons, hover=999):
    label = [1, 2, 3, 4, 5, 6, 7, 8, 9, "Enter", 0, "<--"]  # A list that stores the text on each button
    index = 0
    for i in buttons:  # Goes through each element in buttons
        color = (255, 255, 255)  # Button color defaults to write

        # If the mouse is hovering over the current button, change color to grey
        if index == hover:
            color = (200, 200, 200)
        pygame.draw.rect(screen, color, i)  # Draw the button

        # Draw the text at the center of each button
        text = getText(str(label[index]), (30), (0, 0, 0))
        screen.blit(text, (i.left + 25 - text.get_width() / 2, i.top + 19 - text.get_height() / 2))
        index += 1


# A sub loop for the when the user clicks on the safe
def safeSubProgram():
    global keyTaken  # Tells the program to modify the global keyTaken variable
    trueOrFalse = safeOpened  # A temporary variable
    running = True
    userInput = ""  # A string to store the user input
    passwordEnter = []  # A list to store the rect objects for the buttons

    # A dictionary that converts the index of the button pressed to its corresponding string value
    dict = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8", 8: "9", 10: "0"}
    key = pygame.Rect(300, 400, 300, 150)  # Hitbox for the key
    exit = pygame.Rect(725, 25, 50, 50)  # Hit box for the exit button
    hoverIndex = None  # The index of the button the mouse is hovered over

    #Add each button to the index of buttons
    for y in range(240, 390, 39):
        for x in range(335, 453, 58):
            passwordEnter.append(pygame.Rect(x, y, 41, 28))
    while running:
        if not trueOrFalse:# If the safe is not opened
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1:#If left mouse button is pressed
                    mx, my = evt.pos
                    if exit.collidepoint(mx, my):#If the cursor clicked on the exit button
                        running = False #Leave the sub loop
                    if userInput == "WRONG":
                        userInput = "" #Reset user input
                    for i in range(len(passwordEnter)): #Go through each button and test if the mouse clicked it
                        button = passwordEnter[i]

                        #If the mouse clicked one of the numeric buttons, add the corresponding character to userInput
                        if button.collidepoint(mx, my) and (i < 9 or i == 10) and len(userInput) < 7:
                            userInput += dict[i]

                        #If the mouse clicked enter, test the input against the password
                        elif button.collidepoint(mx, my) and i == 9:

                            #If the password is correct, unlock the safe
                            if userInput == password or trueOrFalse:
                                userInput = "CORRECT"
                                trueOrFalse = True
                            else: #If the password is incorrect, display "Wrong"
                                userInput = "WRONG"
                                trueOrFalse = False

                        #If the mouse clicked backspace, remove the last character
                        elif button.collidepoint(mx, my) and i == 11:
                            userInput = userInput[:len(userInput) - 1]

                # Else if the cursor moved without clicking
                if evt.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()

                    #Determine if the cursor is hovering over one of the
                    for i in range(len(passwordEnter)):
                        button = passwordEnter[i]
                        if button.collidepoint(mx, my):
                            hoverIndex = i
                            break
            scene_draw(screen) #Draws the background
            screen.blit(pygame.transform.scale(pygame.image.load("safe.png"), (800, 600)), (0, 0)) #Draws the safe

            pygame.draw.rect(screen, WHITE, (340, 190, 150, 40)) #Draws the input bar
            drawButtons(passwordEnter, hoverIndex) #Draws the buttons

            # Draws the user input
            textSurface = getText(userInput, 50, (0, 0, 0))
            screen.blit(textSurface, (340, 190))

            #Draw the message
            printMessage("You found a safe, but it requires a password to unlock")

            #Draw the exit button
            pygame.draw.rect(screen, RED, exit)
            screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))
            drawInventory(screen) #Draw the inventory
            pygame.display.flip() #Flip pygame screen

            myClock.tick(60)#Wait long  enough to have 60 fps
        else: #Else if the safe is unlocked
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If left mouse button is pressed

                    mx, my = pygame.mouse.get_pos()
                    if exit.collidepoint(mx, my):
                        running = False

                    #If mouse clicks on the key
                    if key.collidepoint(mx, my) and not keyTaken:

                        #Add the key to the next empty inventory slot
                        for i in range(len(inventory)):
                            obj = inventory[i]
                            if obj.getName() == None:
                                inventory[i] = Inventory(obj.getX(), obj.getY(), "key", "key.png")
                                break;

                        keyTaken = True
            #Draw the safe
            screen.blit(pygame.transform.scale(pygame.image.load("safe.png"), (800, 600)), (0, 0))
            #Draw the safe interior
            screen.blit(pygame.transform.scale(pygame.image.load("safeInterior.png"), (700, 440)), (53, 103))
            #Draw the exit button
            pygame.draw.rect(screen, RED, exit)
            screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))
            if not keyTaken: #if the key is not taken, draw the key
                screen.blit(pygame.transform.scale(pygame.image.load("key.png"), (300, 150)), (300, 400))
            pygame.display.flip()
            myClock.tick(60) #wait long enough for 60 fps
    return trueOrFalse

#When the user clicks on the starting tile in the maze, this function is called to play the maze
def playMaze():
    grid = mazeGrid #Get the maze tiles
    screen.blit(pygame.transform.scale(pygame.image.load("maze.png"), (400, 400)), (200, 100)) #Draw the maze
    pygame.draw.rect(screen, GREEN, grid[0][0]) #Paint the starting grid green
    while pygame.mouse.get_pressed()[0]: #While the left mouse is being held down
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION: #if the mouse moves
                mx, my = pygame.mouse.get_pos()

                #Goes through all the grids
                for i in range(10):
                    for j in range(10):
                        #If the mouse collides with any of the grid
                        if grid[i][j].collidepoint(mx, my):
                            pygame.draw.rect(screen, GREEN, grid[i][j]) #Paint the tile green
                            pygame.display.flip() #Flip the display

                            if i == 9 and j == 9: #if user successfully reaches the final tile

                                #Print success and return True
                                text = getText("SUCCESS", 100, (0, 0, 0))
                                screen.blit(text, ((800 - text.get_width()) / 2, (600 - text.get_height()) / 2))
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                return True
                            #If use hits a tile thats incorrect
                            if not mazeSolution[i][j]:
                                #Paint the tile red
                                pygame.draw.rect(screen, RED, grid[i][j])

                                #Display fail
                                text = getText("FAIL", 100, (0, 0, 0))
                                screen.blit(text, ((800 - text.get_width()) / 2, (600 - text.get_height()) / 2))

                                pygame.display.flip()
                                pygame.time.wait(1000)

                                #Return False
                                return False

# The sub loop when the user clicks on the maze
def mazeSubProgram():
    global mazeAdded
    trueOrFalse = mazeSolved
    running = True
    exit = pygame.Rect(725, 25, 50, 50) #Exit Hitbox
    sol = mazeSolution #Get the solution to the maze
    grid = mazeGrid #Get the maze grid
    while running:

        #If the maze is not solved
        if not trueOrFalse:
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if exit.collidepoint(mx, my):
                        running = False

                    #If the top left button is clicked, run the playMaze function
                    elif grid[0][0].collidepoint(mx, my):
                        trueOrFalse = playMaze()

            #Draw the maze
            screen.blit(pygame.transform.scale(pygame.image.load("maze.png"), (400, 400)), (200, 100))

            #Print the message
            printMessage("Try solving this by starting from the top left")

            #Draw the exit button
            pygame.draw.rect(screen, RED, exit)
            screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))
            pygame.display.flip()

            myClock.tick(144)
        else: #If the maze is solved
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #When left mouse button is clicked
                    mx, my = pygame.mouse.get_pos()
                    if exit.collidepoint(mx, my): #If exit button is clicked
                        if not mazeAdded:
                            #Save a screenshot of the screen.
                            sub = screen.subsurface((200, 100, 400, 400))
                            pygame.image.save(sub, "password.png")

                            #Add maze to the inventory
                            for i in range(len(inventory)):
                                obj = inventory[i]
                                if obj.getName() is None:
                                    inventory[i] = Inventory(obj.getX(), obj.getY(), "maze", "password.png")
                                    mazeAdded = True
                                    break;
                        running = False
            scene_draw(screen) #Draw the background
            pygame.draw.rect(screen, (155, 140, 136), (200, 100, 400, 400)) #Draw the maze background

            #Print the hint message to the maze
            key = getText(password[0] + "_" + password[2] + "_", 200, (165, 150, 140))
            screen.blit(key, (400 - key.get_width() / 2, 300 - key.get_height() / 2))

            #Draw the exit button
            pygame.draw.rect(screen, RED, exit)
            screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))
            pygame.display.flip()
            myClock.tick(144)
    return trueOrFalse

#When the user clicks on the mug, this function is called
def mugSubProgram():
    global mugAdded
    running = True
    exit = pygame.Rect(725, 25, 50, 50) #exit hitbox
    while running:

        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #if left mouse is clicked
                mx, my = pygame.mouse.get_pos()
                if exit.collidepoint(mx, my):
                    if not mugAdded:#if the mug is not added to the inventory
                        #Add mug to the inventory
                        for i in range(len(inventory)):
                            obj = inventory[i]
                            if obj.getName() == None:
                                inventory[i] = Inventory(obj.getX(), obj.getY(), "mug", "mug.png")
                                mugAdded = True
                                break;
                    running = False
        scene_draw(screen) #Draw background

        screen.blit(pygame.transform.scale(pygame.image.load("mug.png"), (400, 400)), (200, 100)) #Draw an enlarged mug

        #Print the hint message
        key = getText("[1] = " + password[1], 100, (255, 255, 255))
        screen.blit(key, (420 - key.get_width() / 2, 300 - key.get_height() / 2))

        #Print the narration message
        printMessage("You found a mug, it has writing on it")

        #Draw the exit button
        pygame.draw.rect(screen, RED, exit)
        screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))

        pygame.display.flip()
        myClock.tick(144)

#When the user clicks on the piece of paper, this function is called
def paperSubProgram():
    global paperAdded
    running = True
    exit = pygame.Rect(725, 25, 50, 50) #exit button hitbox
    while running:

        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN and event.button == 1:#if left mouse is clicked
                mx, my = pygame.mouse.get_pos()
                if exit.collidepoint(mx, my):
                    if not paperAdded: #if the paper is not added to inventory

                        #Add paper to inventory
                        for i in range(len(inventory)):
                            obj = inventory[i]
                            if obj.getName() == None:
                                inventory[i] = Inventory(obj.getX(), obj.getY(), "paper", "paper.png")
                                paperAdded = True
                                break;
                    running = False
        scene_draw(screen) #Draws the background
        #Draws the slip of paper
        screen.blit(pygame.transform.scale(pygame.image.load("paper.png"), (600, 200)), (100, 200))

        #Print the clue
        key = getText("Last number is " + password[3], 90, (0, 0, 0))
        screen.blit(key, (420 - key.get_width() / 2, 300 - key.get_height() / 2))

        #Print the narration
        printMessage("You found a piece of paper")

        #Draw the exit button
        pygame.draw.rect(screen, RED, exit)
        screen.blit(pygame.transform.scale(pygame.image.load("exit.png"), (40, 40)), (730, 30))

        pygame.display.flip()
        myClock.tick(144)

#Animation for dragging the key around
def moveKey():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        scene_draw(screen)
        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONUP: #If mouse button is released
                mx, my = pygame.mouse.get_pos()
                if doorHitBox.collidepoint(mx, my): #If the key is dropped at the door
                    return True
                else:  #If the key is not dropped at the door
                    return False

        #Draw the key at the mouse position
        screen.blit(pygame.transform.scale(pygame.image.load("key.png"), (200, 100)), (mx - 60, my - 60))
        pygame.display.flip()
        myClock.tick(144)


# main game loop
while running:
    try:
        framecount += 1
        scene_draw(screen)

        # checks if user has clicked 'x' to exit program
        for event in pygame.event.get():

            # print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if safeHitBox.collidepoint(mx, my): #If the user clicked on the safe
                    safeOpened = safeSubProgram() #Run the safe loop
                if mazeHitBox.collidepoint(mx, my) and not mazeSolved: #if user clicked on an undiscovered maze
                    mazeSolved = mazeSubProgram() #Run the maze loop
                if mugHitBox.collidepoint(mx, my) and not mugDiscovered: #if user clicked on an undiscovered mug
                    mugDiscovered = True
                    mugSubProgram() #Run the mug loop
                if paperHitBox.collidepoint(mx, my) and not paperDiscovered: #if the user clicked on the paper
                    paperDiscovered = True
                    paperSubProgram() #Run the paper loop
                if doorHitBox.collidepoint(mx, my): #if the user clicked on the door
                    message = "You found a door, unlock it with a key" #print the narrative message

                #If the user clicked on an item in the inventory
                for i in inventory:
                    if i.getRect().collidepoint(mx, my):

                        #Determine what the item is and run the approporiate loop function
                        if i.getName() == "mug":
                            mugSubProgram()
                        elif i.getName() == "paper":
                            paperSubProgram()
                        elif i.getName() == "maze":
                            mazeSubProgram()
                        elif i.getName() == "key":
                            print("KEY")
                            success = moveKey()
        if success: #if game is beat
            if doorOpened is False: #if the music hasn't been played
                doorOpened = True
                # sound = audio.play_file('unlock.mp3',does_loop=True,loop_count=-1)
                doorSound = pygame.mixer.music.load('unlock.mp3') #Play the door unlocking music
                pygame.mixer.music.play()
                pygame.time.wait(2000)

            #The following block of is only used to show that I know file I/O
            word = ""
            file = open("success.txt", "r")
            for i in file:
                word += i.rstrip("\n") #read each line in success.txt and add it to word

            #print success to the screen
            text = getText(word, 100, (0, 255, 0))
            screen.blit(text, (400 - text.get_width() / 2, 300 - text.get_height() / 2))
        else:#If the game is not beaten
            printMessage(message) #Print the narrative message at the top
        pygame.display.flip()
        myClock.tick(144)
    except Exception:
        traceback.print_exc()
pygame.quit()
