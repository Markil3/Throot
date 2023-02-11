import time
import thumby
import math
import random
from collections import namedtuple

from Games.Throot.constants import CONST_FPS

# didplay width 72
# display height 40

### constants
CONST_PL_SCREEN_Y =  int((0.5) * thumby.display.height)

CONST_INP_MOVE_LEFT = thumby.buttonL
CONST_INP_MOVE_RIGHT = thumby.buttonA
CONST_INP_MOVE_RIGHT_ALT = thumby.buttonR

### classes
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
        
        self.anim = PlayerAnimation(self)
        self.debugvisible = False
        
    def update_phys(self, tpf, camera: Camera):
        self.prev_x = self.xsub
        self.prev_y = self.ysub
        inp = int(0)
        if CONST_INP_MOVE_LEFT.pressed():
            inp -= 1
        if CONST_INP_MOVE_RIGHT.pressed() or CONST_INP_MOVE_RIGHT_ALT.pressed():
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
        self.anim.update_phys(camera)
        
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
    MAX_ROOT_OFFSET = int(2)
    
    MAX_GROW_DISTANCE = int(5)#int(3)
    MIN_GROW_DISTANCE = int(1)
    
    Point = namedtuple("Point", ["x", "y"])

    def __init__(self, player):
        self.player = player
        
        self.root_offset = self.MAX_ROOT_OFFSET
        self.grow_distance = self.MAX_GROW_DISTANCE
        
        self.points = []
        self.add_point()
        
    def add_point(self):
        self.points.append(self.Point(self.player.x, self.player.y))
    
    def update_phys(self, camera):
        
        # exit if distance from player to last root point is less than gorw distance
        dist_sqr = (
            (self.player.x - self.points[-1].x) ** 2 +
            (self.player.y - self.points[-1].y) ** 2
        )
        
        if dist_sqr < self.grow_distance ** 2:
            return
        
        # set new grow distance
        self.grow_distance = random.randint(self.MIN_GROW_DISTANCE, self.MAX_GROW_DISTANCE)
        
        # offset last root point to look random
        self.points[-1] = self.Point(
            self.points[-1].x + random.randrange(-self.root_offset, self.root_offset), 
            self.points[-1].y + random.randrange(-self.root_offset, self.root_offset)
        )
        
        # new root point created exactly on player
        self.add_point()
        
        # remove points in list that would make lines off the camera
        for point in self.points[1:]:
            if camera.entity_in_camera(point.x, point.y):
                break
            
            self.points.pop(0)
            
    def update_draw(self, camera, isdecend=1):
        
        # draw line from first position to next
        for i in range(len(self.points) - 1):
            x1, y1 = camera.relative_to_camera(self.points[i].x, self.points[i].y)
            x2, y2 = camera.relative_to_camera(self.points[i + 1].x, self.points[i + 1].y)
            thumby.display.drawLine(
                int(x1),
                int(y1), 
                int(x2),
                int(y2),
                isdecend
            )
