import time
import thumby
import math
import random

from Games.Throot.constants import CONST_FPS

# didplay width 72
# display height 40

# constants
CONST_PL_SCREEN_Y =  int((0.5) * thumby.display.height)

CONST_INP_MOVE_LEFT = thumby.buttonL
CONST_INP_MOVE_RIGHT = thumby.buttonA

# classes
class Player:
    def __init__(self):
        self.prev_x = 0
        self.prev_y = 0
        self.xsub = float(thumby.display.width / 2)
        self.ysub = float(0)
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        self.movespeed = 32 / CONST_FPS
        self.isdecend = 1
        
        self.xspeed = 32 / CONST_FPS
        self.yspeed = 32
        self.accx = 1 / (CONST_FPS * 4)
        self.accaccx = self.accx
        
        self.anim = PlayerAnimation(self.x, self.y)
        self.debugvisible = False
        
    def update_phys(self, tpf, camera: Camera):
        self.prev_x = self.xsub
        self.prev_y = self.ysub
        inp = int(0)
        if CONST_INP_MOVE_LEFT.pressed():
            inp -= 1
        if CONST_INP_MOVE_RIGHT.pressed():
            inp += 1
        
        # debug visible
        if thumby.buttonU.pressed():
            self.debugvisible = not self.debugvisible
        
        ### x movement
        self.xspeed += self.accx
        self.accx += self.accaccx
        
        if (inp == 0) and (self.xspeed > self.movespeed):
            self.xspeed = self.movespeed
            self.accx = self.accaccx
        
        xx = self.xsub + inp * self.xspeed
        
        # clamp to screen
        self.xsub = max(min(xx, thumby.display.width - 1), 0)
        
        ### y movement
        
        self.ysub += self.yspeed * tpf
        
        ### pixel positions
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        # animation
        self.anim.update_phys(self.x, self.y, camera)
        
    def update_draw(self, camera):
        # debug draw
        if self.debugvisible:
            pix_x, pix_y = camera.relative_to_camera(self.x, self.y)
            thumby.display.setPixel(int(pix_x), int(pix_y), self.isdecend)
        
        # animation
        self.anim.update_draw(camera, self.isdecend)
        

class Camera:
    def __init__(self, target):
        self.x = int(0)
        self.y = int(0)
        self.width = thumby.display.width
        self.height = thumby.display.height
        self.offset = -self.height / 2
        self.target = target
    
    def entity_in_camera(self, ent_x, ent_y, ent_width = 0, ent_height = 0) -> bool:
        return ent_x + ent_width >= self.x and ent_y + ent_height >= self.y and ent_x < self.x + self.width and ent_y < self.y + self.height
    
    def relative_to_camera(self, global_x, global_y):
        return (global_x - self.x, global_y - self.y)
    
    def update_phys(self):
        # position player
        self.y = self.target.y + self.offset


class PlayerAnimation:
    # width and height of range bounding box must be odd
    RANDOM_RANGE = int(5)
    POS_RANGE = int(3)
    POS_X = int(0)
    POS_Y = int(1)
    
    def __init__(self, plworldx, plworldy):
        self.poslist = [(plworldx, plworldy)]
        self.debugrandomrange = self.RANDOM_RANGE
        self.debugposrange = self.POS_RANGE
    
    def update_phys(self, plworldx, plworldy, camera):
            
        if plworldy < self.poslist[-1][self.POS_Y] + self.POS_RANGE:
            return
        
        ### get new position
        rad = self.RANDOM_RANGE // 2
        
        # move last pos
        self.poslist[-1] = (
            plworldx + random.randrange(-rad, rad), 
            plworldy + random.randrange(-rad, rad)
        )
        
        # new pos is perfectly on player
        self.poslist.append((plworldx, plworldy))
        
        ### remove the fist item in the list if its full line is off screen
        if not camera.entity_in_camera(self.poslist[1][self.POS_X], self.poslist[1][self.POS_Y]):
            self.poslist.pop(0)
            
    def update_draw(self, camera, isdecend=1):
        ### draw line from first position to next
        
        for i in range(len(self.poslist) - 1):
            x1, y1 = camera.relative_to_camera(self.poslist[i][self.POS_X], self.poslist[i][self.POS_Y])
            x2, y2 = camera.relative_to_camera(self.poslist[i + 1][self.POS_X], self.poslist[i + 1][self.POS_Y])
            thumby.display.drawLine(
                int(x1),
                int(y1), 
                int(x2),
                int(y2),
                isdecend
            )
