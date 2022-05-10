
from random import randint
import pygame 
import sys
import time

block_size = 5
dimention = (90,90)
mines = (dimention[0] * dimention[1]) // 10
main_color = (125,255,255) #  darck_light_green : (100,100,50)


# creating the pygame window
pygame.init()
font = pygame.font.SysFont('monospace', block_size)
window = pygame.display.set_mode((block_size*dimention[0],block_size*dimention[1]))
pygame.display.set_caption("mine sweeper")

def _rectangle(x,y,color):
    pygame.draw.rect(window,color,pygame.Rect(x,y,block_size,block_size))

class Table :
    def __init__(self,height, width,mines):
        self.table = []
        self.vision = []
        self.height = height
        self.width = width
        self.mines = mines
        
    def mine_nabor(self,x,y):
        mine_count = 0
        for line in range(-1,2):
            for col in range(-1,2):
                if line+y >= 0 and col + x >= 0 and line + y < len(self.table) and col + x < len(self.table[0]) and (line,col) != (0,0):
                    if self.table[line + y][col + x] == -1:
                        mine_count += 1
        return mine_count
    
    def test(self):
        self.table = [[0,0,0],
                    [0,-1,0],
                    [0,0,0]]

    def generate(self):
        # create a table full of 0
        for line in range(self.height):
            self.table.append([])
            self.vision.append([])
            for col in range(self.width):
                self.table[line].append(0)
                self.vision[line].append(-2)
        # put the mines as -1
        mines_to_place = self.mines
        while mines_to_place > 0:
            mine_pos = [randint(0,self.width-1),randint(0,self.height-1)]
            if self.table[mine_pos[1]][mine_pos[0]] != -1:
                self.table[mine_pos[1]][mine_pos[0]] = -1
                mines_to_place -= 1
        # put in the number of mines
        for line in range(len(self.table)):
            for col in range(len(self.table[0])):
                if self.table[line][col] != -1:
                    self.table[line][col] = self.mine_nabor(col,line) 
    def __repr__(self):
        for i in self.table:
            print(i)
        for i in self.vision:
            print(i)
    
    def expand(self,x,y):
        # if it is an uncoverend blank case
        if self.table[y][x] == 0 and self.vision[y][x] == -2:
            # iterate through the suroundings
            for line in range(-1,2):
                for col in range(-1,2):
                    # cheks if not out of bounds
                    if line+y >= 0 and col + x >= 0 and line + y < len(self.table) and col + x < len(self.table[0]) :
                        if (line, col) != (0,0):
                            self.expand(col + x,line + y)
                        if self.vision[line+y][col+x] != -3:
                            self.vision[line+y][col+x] = self.table[line+y][col+x]
        # cheks if it is not flaged and uncovered                    
        elif self.vision[y][x] == -2:
            self.vision[y][x] = self.table[y][x]
            # for esthetical purpose
            map._render()
            pygame.display.flip()
                        
    def flag(self,x,y):
        if self.vision[y][x] == -3:
            self.vision[y][x] = -2
        else:
            self.vision[y][x] = -3

    def click(self,x,y):
        if self.vision[y][x] != -3:
            if self.table[y][x] >= 0:
                self.expand(x,y)
            if self.table[y][x] == -1:
                print("you BLEW up!!!!")


    def _render(self):
        for line in range(len(self.vision)):
            for col in range(len(self.vision[0])):
                # if empty
                if self.vision[line][col] == 0:
                    _rectangle(col*block_size,line*block_size,(0,0,0))
                # if covered
                elif self.vision[line][col] == -2 :
                    _rectangle(col*block_size,line*block_size,main_color)
                # if flaged
                elif self.vision[line][col] == -3:
                    _rectangle(col*block_size,line*block_size,main_color)
                    text = font.render(">",True,(0,0,0))
                    window.blit(text,(col*block_size,line*block_size))
                # if mine
                elif self.vision[line][col] == -1 :
                    _rectangle(col*block_size,line*block_size,(255,0,255))
                # if number
                else:
                    gradient = 250/16*self.vision[line][col]
                    _rectangle(col*block_size,line*block_size,(gradient,gradient,gradient))
                    text = font.render(str(self.vision[line][col]),True,main_color)
                    window.blit(text,(col*block_size,line*block_size))

    def solution(self):
        for line in range(len(self.table)):
            for col in range(len(self.table[0])):
                if self.table[line][col] == -1 :
                    _rectangle(col*block_size,line*block_size,(255,0,255))
                elif self.table[line][col] == 0 :
                    _rectangle(col*block_size,line*block_size,(0,0,0))
                else:
                    gradient = 250/8*self.table[line][col]
                    _rectangle(col*block_size,line*block_size,(gradient,gradient,gradient))
                    text = font.render(str(self.table[line][col]),True,main_color)
                    window.blit(text,(col*block_size,line*block_size))
    def dif(self):
        pass 

class Timer:
    def __init__(self,x,y):
        pass


class TextDisplay:
    def __init__(self,x,y):
        pass

map = Table(dimention[0],dimention[1],mines)
map.generate()
# map.__repr__()

while True:
    for event in pygame.event.get() :
        # make the x on the window work
        if event.type == pygame.QUIT:
            sys.exit()
        # mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            position = [pos // block_size for pos in position]
            if event.button == 1:
                map.click(position[0],position[1])
            if event.button == 2:
                map.solution()
                pygame.display.flip()
                time.sleep(3)
            if event.button == 3:
                map.flag(position[0],position[1])

    map._render()
    pygame.display.flip()


