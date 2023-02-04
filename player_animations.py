import time
import thumby
import math
import random

# didplay width 72
# display height 40

# constants
CONST_FPS = 60
CONST_PL_SCREEN_Y =  int((0.5) * thumby.display.height)

CONST_INP_MOVE_LEFT = thumby.buttonL
CONST_INP_MOVE_RIGHT = thumby.buttonA

# classes
class Player:
    def __init__(self):
        self.xsub = float(thumby.display.width / 2)
        self.ysub = float(0)
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        self.yspeed = 32 / CONST_FPS
        self.movespeed = 32 / CONST_FPS
        self.isRoot = 1
        
        self.anim = PlayerAnimation(self.x, self.y)
        self.debugvisible = True
        
    def update_phys(self):
        inp = int(0)
        if CONST_INP_MOVE_LEFT.pressed():
            inp -= 1
        if CONST_INP_MOVE_RIGHT.pressed():
            inp += 1
            
        # debug visible
        if thumby.buttonU.pressed():
            self.debugvisible = not self.debugvisible
        
        # clamp to screen
        self.xsub = max(min(self.xsub + inp * self.movespeed, thumby.display.width), 0)
        self.ysub += self.yspeed
        
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        # animation
        self.anim.update_phys(self.x, self.y, CONST_PL_SCREEN_Y)
        
    def update_draw(self, cam):
        # debug draw
        if self.debugvisible:
            thumby.display.setPixel(self.x - cam.x, self.y - cam.y, self.isRoot)
        
        # animation
        self.anim.update_draw(cam, self.isRoot)
        

class Camera:
    def __init__(self, target):
        self.x = int(0)
        self.y = int(0)
        self.target = target
    
    def update_phys(self, plscreeny):
        # position player
        self.y = self.target.y - plscreeny


class PlayerAnimation:
    # width and height of range bounding box
    RANDOM_RANGE = int(7)
    POS_RANGE = int(3)
    POS_X = int(0)
    POS_Y = int(1)
    
    def __init__(self, plworldx, plworldy):
        self.poslist = [(plworldx, plworldy)]
        self.debugrandomrange = self.RANDOM_RANGE
        self.debugposrange = self.POS_RANGE
    
    def update_phys(self, plworldx, plworldy, plscreeny):
        
        ### exit if player y pos less than random range
        # # debug change random range
        # inp = int(0)
        # if thumby.buttonD.justPressed():
        #     inp -= 1
        # if thumby.buttonU.justPressed():
        #     inp += 1
            
        # if inp != 0:
        #     self.debugposrange = max(self.debugposrange + inp * 2, 1)
        #     print('debugposrange: ', self.debugposrange)
            
        # # if plworldy < self.poslist[-1][self.POS_Y] + random.randint(1, self.debugposrange):
        # #     return
        
        # if plworldy < self.poslist[-1][self.POS_Y] + self.debugposrange:
        #     return
            
        if plworldy < self.poslist[-1][self.POS_Y] + self.POS_RANGE:
            return
        
        ### get new position
        rad = self.RANDOM_RANGE // 2
        
        # # debug change random range
        # inp = int(0)
        # if thumby.buttonB.justPressed():
        #     inp -= 1
        # if thumby.buttonA.justPressed():
        #     inp += 1
            
        # if inp != 0:
        #     self.debugrandomrange = max(self.debugrandomrange + inp * 2, 1)
        #     print('debugrandomrange:', self.debugrandomrange)
            
        # rad = max(self.debugrandomrange // 2, 1)
        
        # vector int
        # self.poslist.append((plworldx + random.randrange(-rad, rad), 
        # plworldy + random.randrange(-rad, rad)))
        
        # move last pos
        self.poslist[-1] = (plworldx + random.randrange(-rad, rad), 
        plworldy + random.randrange(-rad, rad))
        
        # new pos is perfectly on player
        self.poslist.append((plworldx, plworldy))
        
        # # debug
        # self.poslist.append((plworldx, plworldy))
        
        ### remove the fist item in the list if its full line is off screen
        if self.poslist[1][self.POS_Y] < plworldy - plscreeny:
            self.poslist.pop(0)
            
        #print(len(self.poslist))
            
    def update_draw(self, cam,  isRoot=1):
        ### draw line from first position to next
        
        for i in range(len(self.poslist) - 1):
            thumby.display.drawLine(self.poslist[i][self.POS_X] - cam.x,  self.poslist[i][self.POS_Y] - cam.y, 
            self.poslist[i + 1][self.POS_X] - cam.x,  self.poslist[i + 1][self.POS_Y] - cam.y, isRoot)
        

### start
# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(CONST_FPS)

pl = Player()
cam = Camera(pl)

print("game ready")


### game loop
while(True):
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(0) # Fill canvas to black
    
    # update physics
    pl.update_phys()
    cam.update_phys(CONST_PL_SCREEN_Y)
    
    # update drawing
    pl.update_draw(cam)
    
    thumby.display.update()
