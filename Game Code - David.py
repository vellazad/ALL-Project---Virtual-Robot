arena = [['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w', 0],['w',0,'e1D',0,0,0,0,0,0,0,'m',0,0,0,0,'w',0,'e2D',0,'w',0],['w','a',0,0,0,0,0,0,0,0,0,0,0,0,0,'w','a',0,0,'w',0],['w','w',0,0,0,0,0,0,'w','w',0,0,0,0,0,'w',0,0,0,'w',0],['w','w','w','w','w',0,0,0,0,0,0,0,0,'w',0,0,0,0,0,'w'],['w',0,0,0,'w','w','w',0,0,0,0,0,0,'w',0,0,0,0,0,'w',0],['w',0,0,0,0,0,'w',0,0,0,'w',0,0,0,'m',0,0,0,0,'w',0],['w',0,0,0,0,0,0,0,0,0,'w',0,0,0,'w','w','w','w','w','w',0],['w','w','w','w',0,0,0,0,0,'a','w','m',0,0,0,0,0,0,0,'w',0],['w','a',0,0,0,0,0,'w','w','w','w','w','w','w',0,0,0,0,'a','w',0],['w',0,0,0,0,0,0,0,0,'m','w','a',0,0,0,0,0,0,0,'w'],['w',0,0,'w','w',0,0,0,0,0,'w',0,0,0,0,0,0,0,0,'w',0],['w',0,0,0,0,0,0,0,0,0,'w',0,0,0,0,0,'w','w','w','w',0],['w',0,0,0,'m',0,0,'w',0,0,0,0,0,0,0,0,0,0,0,'w',0],['w',0,0,0,0,0,0,'w',0,0,0,0,0,'w','w',0,0,0,0,'w',0],['w','w','w','w','w',0,0,'w',0,0,0,0,0,0,'w',0,0,0,0,'w',0],['w','a',0,0,0,0,0,'w',0,0,0,0,0,0,'w',0,0,0,0,'w',0],['w',0,0,0,0,0,0,'w',0,0,0,0,0,0,'w',0,0,0,0,'w',0],['w',0,'uF',0,0,0,0,'w',0,0,0,0,0,0,'w',0,0,'e3F',0,'w',0],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w',0]]

import pygame
from random import randint
from math import sqrt  # Used to calculate distances
pygame.init()  # Starts Pygame

# Loads sprites as surface objects in Pygame
AItankd = pygame.image.load('AItankd.bmp')
AItankf = pygame.image.load('AItankf.bmp')
AItankl = pygame.image.load('AItankl.bmp')
AItankr = pygame.image.load('AItankr.bmp')
ammo = pygame.image.load('ammo.bmp')
bg = pygame.image.load('bg.bmp')
bullet = pygame.image.load('bullet.bmp')
explosion = pygame.image.load('explosion.bmp')
mine = pygame.image.load('mine.bmp')
tankd = pygame.image.load('tankd.bmp')
tankf = pygame.image.load('tankf.bmp')
tankl = pygame.image.load('tankl.bmp')
tankr = pygame.image.load('tankr.bmp')
wall = pygame.image.load('wall.bmp')

# Creates screen as a surface object of 500x500 pixels
size = (500,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tanks")

# Each AI tank has three positions stored: its starting position, current position and previous position (used to ensure it doesn't backtrack)
prevUserPosition = [3, 19]
userPosition = [3, 19]
preve1Position = [3, 2]
e1Position = [3, 2]
e1StartPosition = e1Position
preve2Position = [18, 2]
e2Position = [18, 2]
e2StartPosition = e2Position
preve3Position = [18, 19]
e3Position = [18, 19]
e3StartPosiion = e3Position

def nextPosition(direction, user):
    '''Used for movement.  Checks if the position the player/robot wants to move to is valid, and returns the new position or none otherwise'''
    if user == 'user':
        position = userPosition
    elif user == 'e1':
        position = e1Position
    elif user == 'e2':
        position = e2Position
    elif user == 'e2':
        position = e3Position
    if direction == 'f':
        tentativePosition = [position[0], position[1] - 1]
    elif direction == 'd':
        tentativePosition = [position[0], position[1] + 1]
    elif direction == 'l':
        tentativePosition = [position[0] - 1, position[1]]
    elif direction == 'r':
        tentativePosition = [position[0] + 1, position[1]]
    if tentativePosition[0] > 20 or tentativePosition[1] > 20 or arena[tentativePosition[1] - 1][tentativePosition[0] - 1] == 'w':
        return None
    else:
        return tentativePosition
    
def pixelPosition(x, y):
    '''Takes x and y coordinates of a position on the grid, and converts them to pixel coordinates.  Used for the placement of images'''
    xPixel = (x - 1)*25
    yPixel = (y - 1)*25
    return [xPixel, yPixel]

def distanceBetweenTwoPoints(position1, position2):
    '''Takes two positions as input and returns the distance between them'''
    x1 = position1[0]
    x2 = position2[0]
    y1 = position1[1]
    y2 = position2[1]
    distance = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance

def nextMove(enemy):
    '''Takes the name of a robot as input (robot 1, 2 or 3) and calculates its next move'''
    # Sets positions according to which robot is being controlled by the function
    if enemy == 'e1':
        robotPosition = e1Position
        robotStartPosition = e1StartPosition
        prevPosition = preve1Position
    elif enemy == 'e2':
        robotPosition = e2Position
        robotStartPosition = e2StartPosition
        prevPosition = preve2Position
    elif enemy == 'e3':
        robotPosition = e3Position
        robotStartPosition = e3StartPosition
        prevPosition = preve3Position
        
    distanceFromUser = distanceBetweenTwoPoints(robotPosition, userPosition)  # Distance from the user
    distanceFromStart = distanceBetweenTwoPoints(robotPosition, robotStartPosition)  # Distance from the start
    
    possibleMoves = [nextPosition('f', enemy), nextPosition('d', enemy), nextPosition('l', enemy), nextPosition('r', enemy)]  # List of coordinates of the four possible moves (up, down, left right) of the robot
    
    # Deletes all invalid coordinates
    noneCount = 0
    for x in range(4):
        if possibleMoves[x] == None:
            noneCount = noneCount + 1
    if noneCount == 0:
        pass
    else:
        for x in range(noneCount):
            possibleMoves.remove(None)
            
    # Calculates the distances from the user each possible move would have
    possibleDistances = []
    for x in range(len(possibleMoves)):
        possibleDistances.append(distanceBetweenTwoPoints(possibleMoves[x], userPosition))
        
    # Selects the move with the shortest distance from the user
    smallestDistance = min(possibleDistances)
    index = possibleDistances.index(smallestDistance)
    move = [possibleMoves[index][0], possibleMoves[index][1], 'f']
    
    # Checks that this move wouldn't cause the robot to backtrack and selects another move at random if it does
    while [move[0], move[1]] == prevPosition:
        randMove = randint(0, len(possibleMoves) - 1)
        move = [possibleMoves[randMove][0], possibleMoves[randMove][1], 'f']
        
    return move  # Returns the x and y-coordinates of the next move, as well as the direction

# Draws the arena
xCoord = 0
yCoord = 0
x = 0
y = 0
while x <= 19:
        while y <= 19:
            if arena[x][y] == 'e1D' or arena[x][y] == 'e2D' or arena[x][y] == 'e3D':
                screen.blit(AItankd,(xCoord, yCoord))
            elif arena[x][y] == 'e1F' or arena[x][y] == 'e2F' or arena[x][y] == 'e3F':
                screen.blit(AItankf,(xCoord, yCoord))
            elif arena[x][y] == 'e1L' or arena[x][y] == 'e2L' or arena[x][y] == 'e3L':
                screen.blit(AItankl,(xCoord, yCoord))
            elif arena[x][y] == 'e1R' or arena[x][y] == 'e2R' or arena[x][y] == 'e3R':
                screen.blit(AItankr,(xCoord, yCoord))
            elif arena[x][y] == 'a':
                screen.blit(ammo,(xCoord, yCoord))
            elif arena[x][y] == 0:
                screen.blit(bg,(xCoord, yCoord))
            elif arena[x][y] == 'b':
                screen.blit(bullet,(xCoord, yCoord))
            elif arena[x][y] == 'e':
                screen.blit(explosion,(xCoord, yCoord))
            elif arena[x][y] == 'm':
                screen.blit(mine,(xCoord, yCoord))
            elif arena[x][y] == 'uD':
                screen.blit(tankd,(xCoord, yCoord))
            elif arena[x][y] == 'uF':
                screen.blit(tankf,(xCoord, yCoord))
            elif arena[x][y] == 'uL':
                screen.blit(tankl,(xCoord, yCoord))
            elif arena[x][y] == 'uR':
                screen.blit(tankr,(xCoord, yCoord))
            elif arena[x][y] == 'w':
                screen.blit(wall,(xCoord, yCoord))
            xCoord = xCoord + 25
            if xCoord == 1000:
                xCoord = 0
            y = y + 1
            if y == 20:
                break
        xCoord = 0
        x = x + 1
        yCoord = yCoord + 25
        y = 0

# Main game loop
running = True 
clock = pygame.time.Clock()
loop = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Ends the loop if the user presses the 'x' button at the top right of the screen
            running = False
        if event.type == pygame.KEYDOWN:  # Receives keyboard input for movement from the user and moves the tank accordingly
            if event.key == pygame.K_w:
                if nextPosition('f', 'user') == None:
                    pass
                else:
                    screen.blit(bg,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
                    userPosition = nextPosition('f', 'user')
                    screen.blit(tankf,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
            elif event.key == pygame.K_d:
                if nextPosition('r', 'user') == None:
                    pass
                else:
                    screen.blit(bg,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
                    userPosition = nextPosition('r', 'user')
                    screen.blit(tankr,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
            elif event.key == pygame.K_s:
                if nextPosition('d', 'user') == None:
                    pass
                else:
                    screen.blit(bg,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
                    userPosition = nextPosition('d', 'user')
                    screen.blit(tankd,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
            elif event.key == pygame.K_a:
                if nextPosition('l', 'user') == None:
                    pass
                else:
                    screen.blit(bg,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))
                    userPosition = nextPosition('l', 'user')
                    screen.blit(tankl,(pixelPosition(userPosition[0], userPosition[1])[0], pixelPosition(userPosition[0], userPosition[1])[1]))

    # This block of code calls the function to calculate the first tank's next move, and updates the screen accordingly
    screen.blit(bg,(pixelPosition(e1Position[0], e1Position[1])[0], pixelPosition(e1Position[0], e1Position[1])[1]))  # Blanks the tank's current position
    e1Data = nextMove('e1') # Calls the function to calculate the next move
    preve1Position = e1Position # Updates the current position to be the next previous position
    e1Position = [e1Data[0], e1Data[1]]
    e1Direction = e1Data[2]
    if e1Direction == 'f':  # Chooses the tank's sprite according to the direction it will face in the next move
        nextSprite = AItankf
    elif e1Direction == 'd':
        nextSprite = AItankd
    elif e1Direction == 'l':
        nextSprite = AItankl
    elif e1Direction == 'r':
        nextSprite = AItankr  
    screen.blit(nextSprite,(pixelPosition(e1Position[0], e1Position[1])[0], pixelPosition(e1Position[0], e1Position[1])[1]))  # Draws the tank at its next position

    # This block of code is exactly like the one above but for the second tank
    screen.blit(bg,(pixelPosition(e2Position[0], e2Position[1])[0], pixelPosition(e2Position[0], e2Position[1])[1]))
    e2Data = nextMove('e2')
    preve2Position = e2Position
    e2Position = [e2Data[0], e2Data[1]]
    e2Direction = e2Data[2]
    if e1Direction == 'f':
        nextSprite = AItankf
    elif e1Direction == 'd':
        nextSprite = AItankd
    elif e1Direction == 'l':
        nextSprite = AItankl
    elif e1Direction == 'r':
        nextSprite = AItankr
    screen.blit(nextSprite,(pixelPosition(e2Position[0], e2Position[1])[0], pixelPosition(e2Position[0], e2Position[1])[1]))

    pygame.display.flip()  # Updates screen with what we've drawn
    pygame.time.delay(200)  # This delay is used to adjust the speed of the robot
    clock.tick(60)  # Limits game to a maximum of 60 FPS

pygame.quit()  # Quits the game when user is done





