import numpy as np
import random
import pyglet
from pyglet.window import mouse, key

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
CELL_WIDTH = 16
CELL_HEIGHT = 16
RUN = True
window = pyglet.window.Window(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)


class BrownianSim:
    def __init__(self, width = (WINDOW_WIDTH//CELL_WIDTH) -2, height = (WINDOW_HEIGHT//CELL_HEIGHT) -2, draw_x = CELL_WIDTH, draw_y = CELL_HEIGHT):
        self.steps = 0
        self.width, self.height = width, height
        self.draw_x, self.draw_y = draw_x, draw_y
        self.neighborhood = ((-1,0),(1,0),(0,1),(0,-1))
        self.maxVal = 6
        self.minVal = 0
        
        self.wraparound = False
        
        self.randomBoard(width,height)
        self.board[height//2][width//2] = -1
      
    def toggleBorder(self):
        self.wraparound = not self.wraparound
        
    def emptyBoard(self, width = WINDOW_WIDTH//CELL_WIDTH, height = WINDOW_HEIGHT//CELL_HEIGHT):
        self.board = np.zeros((height, width), dtype = int)
        
    def randomBoard(self, width = WINDOW_WIDTH//CELL_WIDTH, height = WINDOW_HEIGHT//CELL_HEIGHT):
        self.board = (np.random.random((height, width)) > 0.96).astype(int) * self.maxVal

    def getDestination(self,x,y,dx,dy):
        if self.wraparound:
            return (x + dx + self.width)%self.width, (y + dy + self.height)%self.height
        else:
            return max(0, min(x + dx, self.width-1)), max(0, min(y + dy, self.height-1))
            
    def getDestinationValue(self,x,y,dx,dy):
        x2, y2 = self.getDestination(x,y,dx,dy)
        return self.board[y2][x2]
        
    def destinationIsWithinBounds(self,x,y,dx,dy):
        return 0<=x+dx<self.width and 0<=y+dy<self.height

    def getListNeighborsCoords(self,x,y):
        if self.wraparound:
            return [self.getDestination(x,y,dx,dy) for dx,dy in self.neighborhood]
        else:
            return [self.getDestination(x,y,dx,dy) for dx,dy in self.neighborhood if self.destinationIsWithinBounds(x,y,dx,dy)]
        
    def getListNeighbors(self,x,y):
        return [self.board[j][i] for i,j in self.getListNeighborsCoords(x,y)]

    def drawBoard(self):
        for y in range(self.height):
            for x in range(self.width):
                currentCell = self.board[y][x]
                drawBlock = False
                
                if currentCell > 0:
                    v = int( (currentCell / self.maxVal) * 255)
                    drawColor = (v,0,0)
                    drawBlock = True
                elif currentCell < 0:
                    drawBlock = True
                    b = currentCell * 16 #currentCell has values -1 to -5
                    drawColor = (0,240 + b,175 - b);  #ICE
                    
                if drawBlock:
                    X1,Y1 = self.draw_x + (x * CELL_WIDTH), self.draw_y + (y * CELL_HEIGHT),
                    X2,Y2 = X1 + CELL_WIDTH,Y1 + CELL_HEIGHT
                    pyglet.graphics.draw(4 ,pyglet.gl.GL_POLYGON, ('v2i',[X1,Y1, X2,Y1, X2,Y2, X1,Y2] ), ('c3B', drawColor * 4 ) )
                    
        #DRAW BORDER
        if not self.wraparound:
            X1,Y1 = self.draw_x, self.draw_y,
            X2,Y2 = X1 + (CELL_WIDTH*self.width),Y1 + (CELL_HEIGHT*self.height)
            pyglet.graphics.draw(8 ,pyglet.gl.GL_LINES, ('v2i',[X1,Y1, X2,Y1,  X2,Y1, X2,Y2,  X1,Y2, X2,Y2,  X1,Y1, X1,Y2] ), ('c3B', (255,255,255)* 8 ) )
          
          
    def updateBoard(self):
        newBoard = np.copy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                currentCell = self.board[y][x]
                listNeighbors = self.getListNeighbors(x,y)
                
                #AVOID MOVING INTO FREEZY BLOCKS
                if not self.wraparound:
                    validDirections = [n for n in self.neighborhood if self.destinationIsWithinBounds(x,y,n[0],n[1]) and self.getDestinationValue(x,y,n[0],n[1])>-1]
                else:
                    validDirections = [n for n in self.neighborhood if self.getDestinationValue(x,y,n[0],n[1])>-1]
                    
                #FREEZE
                freezeNearby = sum([1 for neighbor in listNeighbors if neighbor < 0])
                if currentCell > 0 and freezeNearby: 
                    newBoard[y][x] = -1
                    currentCell = -1
                        
                #AESTHETIC FREEZING        
                if currentCell < 0:
                    if freezeNearby == 0: newBoard[y][x] = -1; currentCell = -1
                    if freezeNearby == 1: newBoard[y][x] = -2; currentCell = -2
                    if freezeNearby == 2: newBoard[y][x] = -3; currentCell = -3
                    if freezeNearby == 3: newBoard[y][x] = -4; currentCell = -4
                    if freezeNearby == 4: newBoard[y][x] = -5; currentCell = -5
                            
                if validDirections:
                    #DIFFUSION
                    if currentCell > 1 and random.random() > 0.5:    
                        for dx,dy in validDirections:
                            x2,y2 = self.getDestination(x,y,dx,dy)
                            if self.board[y2][x2] + 1 <= self.maxVal:
                                if currentCell: 
                                    newBoard[y][x] -= 1
                                    newBoard[y2][x2] += 1
                                    currentCell -= 1                                 
                    #MOVEMENT
                    if currentCell > 0: 
                        dx, dy = random.choice(validDirections)
                        x2, y2 = self.getDestination(x,y,dx,dy)
                        if self.board[y2][x2] + currentCell <= self.maxVal:
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
        #PAUSE SIMULATION
        RUN = not RUN
    elif symbol == key.R:
        #RANDOMIZE THE BOARD
        TEST.randomBoard()
    elif symbol == key.E:
        #CLEAR THE BOARD
        TEST.emptyBoard()
    elif symbol == key.W:
        #TOGGLE BORDER
        TEST.toggleBorder()
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
            
pyglet.clock.schedule_interval(update, 1/180)
pyglet.app.run()
