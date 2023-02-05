import time
import math

import thumby

import Games.Throot.map
import Games.Throot.sprites

from random import randrange

from Games.Throot.artrepository import *
from Games.Throot.player import Player, Camera
from Games.Throot.map import ObstacleSlice, OBSTACLE_SLICES
from Games.Throot.sprites import Obstacle, update_entities
from Games.Throot.constants import *


class GameManager:
    def __init__(self, *rooms):
         self.rooms = rooms
         self.room_index = 0

    def start(self):
        # Set the FPS (without this call, the default fps is 30)
        thumby.display.setFPS(CONST_FPS)

    def room_goto(self, event):
        index = event['room']
        if index < 0:
            self.room_index = min(self.room_index + 1, len(self.rooms))
        else:
            self.room_index = index
            
        self.rooms[self.room_index].start(event)

    def restart(self):
        self.room_index = 0
        
    def update(self, tpf):
        event = self.rooms[self.room_index].update(tpf)
        
        thumby.display.update()
        
        if event:
            self.room_goto(event)
        

class Room:
    def start(self, event):
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
    
    def update(self, tpf):
        pass


class RoomTitle(Room):
    def update(self, tpf):
        super().update(tpf)
        
        if thumby.inputPressed():
            return {
                'room': ROOM_MAIN
            }
        
        # draw title sprite
        title_text = 'press a to start'
        
        chr_len = 5
        x = int(round(thumby.display.width / 2 - (chr_len * len(title_text)) / 2))
        y = int(round(thumby.display.height / 2 - chr_len / 2))
        
        buff = 2
        w = chr_len * len(title_text) + buff
        h = chr_len + buff
        thumby.display.drawFilledRectangle(x - buff, y - buff, w, h, 1)
        thumby.display.drawText(title_text, x, y, 0)
        
class GameLoop(Room):
    def __init__(self):
        self.diving_velocity = 10
        self.diving_accel = 0
        self.current_obstacle_slice = OBSTACLE_SLICES[0]
        self.entities = set()

        self.player = None
        self.camera = None
        
        self.score = 0
        self.level = 0
        self.finish_depth = 0
        
        self.waterx = float(0)
    
    def start(self, event):
        self.entities.clear()
        self.current_obstacle_slice = OBSTACLE_SLICES[0]
        self.player = Player()
        self.player.yspeed = 10
        self.score = 0
        
        self.finish_depth = 100 + 5 * self.level ** 2
        self.camera = Camera(self.player)

    def get_obstacle_slice(self):
        return OBSTACLE_SLICES[randrange(0, len(OBSTACLE_SLICES))]
        
    def draw_water(self):
        # bookwater
        
        # exit if depth is less than 2 screens of the finish depth
        if self.player.y + thumby.display.height < self.finish_depth:
            return
        
        self.waterx += sprite_water.width / CONST_FPS
        if self.waterx > sprite_water.width:
            self.waterx = 0
            
        # water surface.
        for i in range(math.ceil(thumby.display.width / sprite_water.width) + 1):
            
            x, y = self.camera.relative_to_camera(
                (int(self.waterx) - sprite_water.width) + i * sprite_water.width,
                self.finish_depth
            )
        
            thumby.display.blit(
                sprite_water[0],
                int(x), int(y), 
                sprite_water.width, sprite_water.height,
                0, 
                0, 0
            )
            
        # water below surface
        x, y = self.camera.relative_to_camera(
            0,
            self.finish_depth
        )
        
        thumby.display.drawFilledRectangle(
                int(x), int(y) + sprite_water.height,
                thumby.display.width, self.finish_depth + thumby.display.height * 3,
                1,
        )
        
        # win text
        if self.player.y > self.finish_depth + (thumby.display.height // 2):
            thumby.display.drawText('water reach!', 0, thumby.display.height // 4, 0)
            thumby.display.drawText(f'   stage {self.level + 1}', 0, thumby.display.height // 4 + 9, 0)

    def update(self, tpf):
        """
        Executes one tick of the game
        """
        super().update(tpf)

        self.player.update_phys(tpf, self.camera)
        
        self.camera.update_phys()

        # Generate new entities as needed
        if abs(self.player.y) < abs(self.finish_depth):
            self.entities |= update_entities(self.entities, self.level, self.player.ysub, self.player.prev_y)
        else:
            self.entities.clear()

        # Updates the entities
        to_remove = set()
        for entity in self.entities:
            if not entity.update(tpf, self.player, self.camera) or abs(entity.y - self.player.y) > self.camera.height * 1.5:
                to_remove.add(entity)
            elif entity.intersects_pixel(self.player.xsub, self.player.ysub):
                if isinstance(entity, Obstacle):
                    return {
                        'room': ROOM_END,
                        'score': self.score,
                        'level': self.level + 1
                    }
        self.entities -= to_remove
        
        self.score = int(abs(self.player.y) * 10)
        
        # finish level
        if self.player.y > self.finish_depth + int(thumby.display.height * 1.5):
            self.level += 1
            self.start({})

        thumby.display.fill(0)
        
        # Draw the entities
        for entity in self.entities:
            entity.render(tpf, self.camera)
        self.player.update_draw(self.camera)

        self.draw_water()
        
        thumby.display.drawText(str(self.score), thumby.display.width - (len(str(self.score)) + 2) * 5, 1, 1)
        
        
class EndRoom(Room):
    def __init__(self):
        self.score = 0
    
    def start(self, event):
        self.score = event['score']
        # Used to make sure that we aren't triggering from input mean't for the game.
        self.still_pressed = thumby.inputPressed()
    
    def update(self, tpf):
        if not thumby.inputPressed():
            self.still_pressed = False
        elif not self.still_pressed and thumby.inputPressed():
            return {
                'room': ROOM_START
            }
        thumby.display.fill(0)
        thumby.display.drawText("Final Score:", (thumby.display.width - 60) // 2, 1, 1)
        thumby.display.drawText(str(self.score), (thumby.display.width - (len(str(self.score)) * 5)) // 2, 9, 1)

def main():    
    game = GameManager(RoomTitle(), GameLoop(), EndRoom())
    game.start()

    prev_time = 0
    while True:
        t0 = time.ticks_ms()
        tps = (t0 - prev_time) / 1000
        #loop.update(tps)
        game.update(tps)
        prev_time = t0

main()
