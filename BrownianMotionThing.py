import numpy as np
import random
import pyglet
from pyglet.window import mouse, key

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
CELL_WIDTH = 16
CELL_HEIGHT = 16
RUN = True
window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)


class BrownianSim:
    def __init__(self, width = WINDOW_WIDTH//CELL_WIDTH, height = WINDOW_HEIGHT//CELL_HEIGHT, draw_x = 0, draw_y = 0):
        self.steps = 0
        self.width, self.height = width, height
        self.draw_x, self.draw_y = draw_x, draw_y
        self.neighborhood = ((-1,0),(1,0),(0,1),(0,-1))
        self.maxVal = 8
        self.minVal = 0
        
        self.emptyBoard(width,height)
        self.board[height//2][width//2] = -1
        
        
    def emptyBoard(self, width = WINDOW_WIDTH//CELL_WIDTH, height = WINDOW_HEIGHT//CELL_HEIGHT):
        self.board = np.zeros((height, width), dtype = int)
        
    def randomBoard(self, width = WINDOW_WIDTH//CELL_WIDTH, height = WINDOW_HEIGHT//CELL_HEIGHT):
        self.board = (np.random.random((height, width)) > 0.8).astype(int) 

    def chooseDirection(self):
        return random.choice(self.neighborhood)
        
    def getDestination(self,x,y,dx,dy):
        return (x + dx + self.width)%self.width, (y + dy + self.height)%self.height

    def getListNeighbors(self,x,y):
        list_coords = [self.getDestination(x,y,dx,dy) for dx,dy in self.neighborhood]
        return [self.board[j][i] for i,j in list_coords]

    def drawBoard(self):
        for y in range(self.height):
            for x in range(self.width):
                currentCell = self.board[y][x]
                drawBlock = False
                
                if currentCell > 0:
                    v = int( (currentCell / self.maxVal) * 128)
                    drawColor = (128 + v,0,0)
                    drawBlock = True
                else:
                    #if currentCell == -1: drawColor = (240,240,240); drawBlock = True #SOLID
                    if currentCell < 0: drawColor = (0,255,255); drawBlock = True #ICE
                    
                if drawBlock:
                    X1,Y1 = self.draw_x + (x * CELL_WIDTH), self.draw_y + (y * CELL_HEIGHT),
                    X2,Y2 = X1 + CELL_WIDTH,Y1 + CELL_HEIGHT
                    pyglet.graphics.draw(4 ,pyglet.gl.GL_POLYGON, ('v2i',[X1,Y1, X2,Y1, X2,Y2, X1,Y2] ), ('c3B', drawColor * 4 ) )
                    
                    
    def updateBoard(self):
        newBoard = np.copy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                currentCell = self.board[y][x]
                listNeighbors = self.getListNeighbors(x,y)
                
                #FREEZE
                if currentCell > 0:
                    freezeNearby = sum([1 for neighbor in listNeighbors if neighbor == -1])
                    if freezeNearby: 
                        newBoard[y][x] = -1
                        break #currentCell = -1
                
                #DIFFUSION
                if currentCell > 1:
                    list_coords = [self.getDestination(x,y,dx,dy) for dx,dy in self.neighborhood]
                    for x2,y2 in list_coords:
                        if self.board[y2][x2] > -1: #Avoid grid cells marked with negative numbers 
                            if self.board[y2][x2] + 1 < self.maxVal:
                                currentCell -= 1
                                newBoard[y][x] -= 1
                                newBoard[y2][x2] += 1    
                                
                        if currentCell <=0: break
                
                #MOVEMENT
                if currentCell > 0: 
                    dx, dy = self.chooseDirection()
                    x2, y2 = self.getDestination(x,y,dx,dy)
                    if self.board[y2][x2] > -1: #Avoid grid cells marked with negative numbers 
                        if self.board[y2][x2] + currentCell < self.maxVal:
                            newBoard[y][x] -= currentCell
                            newBoard[y2][x2] += currentCell
                            currentCell = 0 #This cell is now empty

                        
        self.board = newBoard
        self.steps += 1

TEST = BrownianSim()

@window.event
def on_draw():
    window.clear()
    TEST.drawBoard()
    
@window.event
def on_key_press(symbol, modifiers):
    global RUN
    if symbol == key.P:
        RUN = not RUN
    elif symbol == key.R:
        TEST.randomBoard()
    elif symbol == key.E:
        TEST.emptyBoard()
    pass
    
    
@window.event        
def on_mouse_press(x, y, button, modifiers):
    _x, _y = x // CELL_WIDTH, y // CELL_HEIGHT
    if button == mouse.LEFT:
        TEST.board[_y][_x] = TEST.maxVal
    elif button == mouse.RIGHT:
        if (TEST.board[_y][_x] == -1): 
            TEST.board[_y][_x] = 0
        else:
            TEST.board[_y][_x] = -1
           
def update(t):
    global RUN
    if RUN:
        TEST.updateBoard()
            
pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()
