import time
import thumby
import math
import random
from collections import namedtuple

from Games.Throot.constants import CONST_FPS

# didplay width 72
# display height 40

class Input:
    def move_right(self):
        return (
            thumby.buttonA.pressed() or
            thumby.buttonR.pressed()
        )
        
    def move_left(self):
        return thumby.buttonL.pressed()
        
inp = Input()

### classes
class Player:
    def __init__(self):
        self.prev_x = 0
        self.prev_y = 0
        self.xsub = float(thumby.display.width / 2)
        self.ysub = float(0)
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        self.isdecend = 1
        
        self.input_x = float(0)
        
        # constants
        self.speed_x_start = 32
        self.speed_x_max = 200
        self.acc_x_start = 64
        self.jerk_x = 128
        
        self.speed_x = self.speed_x_start
        self.acc_x = self.acc_x_start
        
        # y speed is constant
        self.speed_y = 16
        
        self.anim = PlayerAnimation(self)
        
        
    def update_phys(self, tpf, camera: Camera):
        # prevoius sub pixel position
        self.prev_x = self.xsub
        self.prev_y = self.ysub
        
        ### x movement
        
        # x input
        if inp.move_left() and (not inp.move_right()):
            self.input_x = -1
            
        if inp.move_right() and (not inp.move_left()):
            self.input_x = 1
            
        if (not inp.move_left()) and (not inp.move_right()):
            self.input_x = 0
        
        # acceleration and jerk
        self.speed_x += self.acc_x * tpf
        self.acc_x += self.jerk_x * tpf
        
        # limit speed
        self.speed_x = min(self.speed_x_max, self.speed_x)
        
        # reset speed and acceleration if no input
        if (self.input_x == 0) and (self.speed_x != self.speed_x_start):
            self.speed_x = self.speed_x_start
            self.acc_x = self.acc_x_start
            
        # set x sub pixel position
        self.xsub += self.speed_x * tpf * self.input_x
        
        ### y movement
        
        # set y sub pixel position
        self.ysub += self.speed_y * tpf
        
        ### stay in world bounds
        self.xsub = max(min(self.xsub, thumby.display.width - 1), 0)
        
        ### pixel positions
        self.x = int(self.xsub)
        self.y = int(self.ysub)
        
        ### animation physics
        self.anim.update_phys(camera)
        
    def update_draw(self, camera):
        ### animation render
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
    MAX_ROOT_OFFSET = int(4)
    
    MAX_GROW_DISTANCE = int(6)#int(3)
    MIN_GROW_DISTANCE = int(2)
    
    Point = namedtuple("Point", ["x", "y"])

    def __init__(self, player):
        self.player = player
        
        self.root_offset = self.MAX_ROOT_OFFSET
        self.grow_distance = self.MAX_GROW_DISTANCE
        
        self.points = []
        self.add_point()
        
        self.debug_visible = False
        self.debug_exact = True
        
    def add_point(self):
        self.points.append(self.Point(self.player.x, self.player.y))
    
    def update_phys(self, camera):
        # debug visible
        if thumby.buttonB.justPressed():
            self.debug_visible = not self.debug_visible
            
        # debug exact
        if thumby.buttonU.justPressed():
            self.debug_exact = not self.debug_exact
            
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
        
        # points are not removed so the camera can pan back up
        # # remove points in list that would render lines off the camera
        # for point in self.points[1:]:
        #     if camera.entity_in_camera(point.x, point.y):
        #         break
            
        #     self.points.pop(0)
            
    def update_draw(self, camera, isdecend=1):
        # debug render
        if self.debug_visible:
            pix_x, pix_y = camera.relative_to_camera(self.player.x, self.player.y)
            thumby.display.setPixel(int(pix_x), int(pix_y), isdecend)
            return
        
        # draw line from last point to player
        if self.debug_exact:
            x1, y1 = camera.relative_to_camera(self.player.x, self.player.y)
            x2, y2 = camera.relative_to_camera(self.points[-1].x, self.points[-1].y)
            thumby.display.drawLine(
                int(x1),
                int(y1), 
                int(x2),
                int(y2),
                isdecend
            )

        # draw line from last point to previous
        point_off_camera_count = 2
        point_prev = self.points[-1]
        for point in self.points[-2::-1]:
            
            # break if entire line is off camera
            if not camera.entity_in_camera(point.x, point.y):
                point_off_camera_count -= 1
                if point_off_camera_count <= 0:
                    break
            
            x1, y1 = camera.relative_to_camera(point_prev.x, point_prev.y)
            x2, y2 = camera.relative_to_camera(point.x, point.y)
            point_prev = point
            
            thumby.display.drawLine(
                int(x1),
                int(y1), 
                int(x2),
                int(y2),
                isdecend
            )
