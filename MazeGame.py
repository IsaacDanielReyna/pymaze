import pygame
import sys
import random
from Cell import *
from GameObject import *
pygame.init()

#MUST BE ODD!!!
MazeWidth = 9
MazeHeight = 9
###################

pygame.display.set_caption("PYMAZE")
screen = pygame.display.set_mode([500,500])

waiting = True
running = True

#Returns a standalone instance instead of a reference
def createGameObject(image, x, y):
    tmp = GameObject(image, x, y)
    return tmp

screen_size = screen.get_size()

padding = 25
small = createGameObject("small.png", 156, 294)
small.x = screen_size[0]/2 - small.width/2
medium = createGameObject("medium.png", small.x, small.y + small.height + padding)
medium.x = screen_size[0]/2 - medium.width/2
large = createGameObject("large.png", medium.x, medium.y + medium.height + padding)
large.x = screen_size[0]/2 - large.width/2

while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            running = False
            
    background = pygame.image.load("levelselect.png")
    
    screen.blit(background,(0,0))
    
    mouse = pygame.mouse.get_pressed()
    
    if mouse[0] == 1:
        mpos = pygame.mouse.get_pos()
        
        if small.getRect().collidepoint(mpos):
            MazeWidth = 9
            MazeHeight = 9
            waiting = False
        elif medium.getRect().collidepoint(mpos):
            MazeWidth = 21
            MazeHeight = 21
            waiting = False
        elif large.getRect().collidepoint(mpos):
            MazeWidth = 31
            MazeHeight = 31
            waiting = False

    small.blit()
    medium.blit()
    large.blit()
    pygame.display.flip()

###################################################################################################################################################
screen_width=MazeWidth*32
screen_height=MazeHeight*32
black = 0,0,0
red = (255,0,0)

#pygame.display.set_caption("MAZE RUNNER")
screen = pygame.display.set_mode([screen_width,screen_height])
background = pygame.image.load("brick1.png")
background = pygame.transform.scale(background,(screen_width,screen_height))


screen.fill(red)
screen.blit(background,(0,0))

#Character
characters = []
characters.append(createGameObject("character.png", 4000, 4000)) #doesn't matter how far, the checkbounds function returns it inside view.

#Walls List
walls = []

#Get Available Directions
def getAvailableDirections(m, r, c, width, height):
    tmp = []
    tmpRow = r
    tmpCol = c
    tmpRow2 = r
    tmpCol2 = c
    
    #up
    tmpRow-=2
    tmpRow2-=1
    if tmpRow > 0 and m[tmpRow][c] == 1:
        tmp.append(Cell(tmpRow,c))
        
    #right
    tmpCol+=2
    tmpCol2+=1
    if tmpCol <= width and m[r][tmpCol] == 1:
        tmp.append(Cell(r, tmpCol))

    tmpRow = r
    tmpCol = c                            
    #down
    tmpRow+=2
    tmpRow2+=1
    if tmpRow <=height and m[tmpRow][c] == 1:
        tmp.append(Cell(tmpRow,c))
        
    #left
    tmpCol-=2
    tmpCol2-=1
    if tmpCol > 0 and m[r][tmpCol] == 1:
        tmp.append(Cell(r, tmpCol))
    return tmp

def findPath(r, c, tR, tC):
    if (r>tR):
        row = r - 1
    elif (r<tR):
        row = r + 1
    else:
        row = r

    if (c>tC):
        col = c - 1
    elif (c<tC):
        col = c + 1
    else:
        col = c

    return Cell(row, col)

#Create backtracking
stack = []

#Create a 2-dimensional int array with odd row and column size. 0 represents paths and 1 would be walls.
Maze = [[0 for x in range(MazeHeight)] for x in range(MazeWidth)]

#Set all cells to 1(wall). There are no paths right now.
for height in range(0, MazeHeight):
    for width in range(0, MazeWidth):
        Maze[height][width] = 1

#Set the starting point. Generate odd numbers for row and col. Set that cell to 0.
row = int(random.randrange(1,MazeHeight,2))
col = int(random.randrange(1,MazeWidth,2))
Maze[row][col] = 0

#Choose a random direction(up, right, down, or left). Always move by 2 cells.
error = True
while error:
    
    #check avilable directions, if not avilable directions then backtrack and try again.
    directions = getAvailableDirections(Maze, row, col, MazeWidth-1, MazeHeight-1)
    if len(directions) >= 1:
        d = int(random.uniform(0, len(directions)))
        tmpRow = directions[d].row
        tmpCol = directions[d].col
        path = findPath(row, col, tmpRow, tmpCol)
        Maze[tmpRow][tmpCol] = 0
        Maze[path.row][path.col] = 0
        #print "OK:(From:({},{}) to ({},{}) was chosen, and ({},{}) was erased)".format(row, col, tmpRow, tmpCol, path.row, path.col)
        row = directions[d].row
        col = directions[d].col
        stack.append(Cell(row, col))
        
    else:
        if len(stack) == 1:
            error = False
        else:
            stack.pop()
            row = stack[-1].row
            col = stack[-1].col


#Choose a random starting and ending point
Maze[MazeHeight-1][MazeWidth-1] = 0
Maze[MazeHeight-1][MazeWidth-2] = 0
Maze[0][1] = 0

#Build maze
for height in range(0, MazeHeight):
    for width in range(0, MazeWidth):
        if (Maze[height][width] == 1):
            walls.append(createGameObject("tile1.png", (width*32), (height*32)))

#START GAME #
while running:        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(black)
    screen.blit(background,(0,0))

    for character in characters:
        character.update()#Updates: Detects input, Moves, then Blits
        character.checkBounds()#Forces GameObject to stay within window
        if character.collide(walls): #Checks if GameObject collides with another GameObject inside list of GameObjects.
            #characters.remove(character) # Kill/Remove Object
            character.move(character.previous) # Since it's colliding with walls, then don't let character past the wall.
            
        
    #Blit
    for wall in walls:
        wall.blit() #Draws the GameOjbect to screen

    pygame.display.flip()
pygame.quit()


  

