import time
import math

import thumby

import Games.Throot.map
import Games.Throot.sprites

from random import randrange
from Games.Throot.artrepository import OBSTACLES
from Games.Throot.player import Player
from Games.Throot.map import ObstacleSlice, OBSTACLE_SLICES
from Games.Throot.sprites import Obstacle, update_entities
from Games.Throot.constants import CONST_FPS

class GameManager:
    EVENT_ROOM_CHANGE = {'start': 0, 'main': 1, 'end': 2, 'next': -1}
    
    def __init__(self, *rooms):
         self.rooms = rooms
         self.room_index = 0

    def start(self):
        # Set the FPS (without this call, the default fps is 30)
        thumby.display.setFPS(CONST_FPS)

    def room_goto(self, index):
        if index < 0:
            self.room_index = min(self.room_index + 1, len(self.rooms))
        else:
            self.room_index = index
            
        self.rooms[self.room_index].start()

    def restart(self):
        self.room_index = 0
        
    def update(self, tpf):
        event = self.rooms[self.room_index].update(tpf)
        
        thumby.display.update()
        
        if event:
            self.room_goto(self.EVENT_ROOM_CHANGE[event])
        

class Room:
    def start(self):
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
    
    def update(self, tpf):
        pass


class RoomTitle(Room):
    def update(self, tpf):
        super().update(tpf)
        
        if thumby.inputPressed():
            return 'main'
        
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
        self.current_depth = 0
        self.diving_velocity = 10
        self.diving_accel = 0
        self.current_obstacle_slice = OBSTACLE_SLICES[0]
        self.entities = set()

        self.player = Player()
        
        self.score = 0

    def get_obstacle_slice(self):
        return OBSTACLE_SLICES[randrange(0, len(OBSTACLE_SLICES))]

    def update(self, tpf):
        """
        Executes one tick of the game
        """
        super().update(tpf)
        prev_depth = self.current_depth
        self.diving_velocity += self.diving_accel * tpf
        self.current_depth += self.diving_velocity * tpf
        
        #print("%f (%f)" % (self.current_depth, self.current_depth % ObstacleSlice.height))

        #print("%f -> %f: %f -> %f" % (prev_depth, self.current_depth, prev_depth % ObstacleSlice.height, self.current_depth % ObstacleSlice.height))
        if (
            self.current_depth > prev_depth and self.current_depth % ObstacleSlice.height < prev_depth % ObstacleSlice.height
            or self.current_depth < prev_depth and self.current_depth % ObstacleSlice.height > prev_depth % ObstacleSlice.height
            ):
            self.current_obstacle_slice = self.get_obstacle_slice()

        self.player.update_phys(self.current_depth, prev_depth)

        # Generate new entities as needed
        self.entities |= update_entities(self.current_obstacle_slice, self.current_depth, prev_depth)

        # Updates the entities
        to_remove = set()
        for entity in self.entities:
            if not entity.update(tpf, self.current_depth, prev_depth):
                to_remove.add(entity)
            elif entity.intersects_pixel(self.player.xsub, self.player.ysub):
                if isinstance(entity, Obstacle):
                    print("Hit!")
        self.entities -= to_remove
        
        self.score = int(self.current_depth * 10)

        thumby.display.fill(0)
        # Draw the entities
        for entity in self.entities:
            entity.render(tpf, self.current_depth, prev_depth)
        self.player.update_draw(self.current_depth, prev_depth)

        thumby.display.drawText(str(self.score), thumby.display.width - (len(str(self.score)) + 2) * 5, 1, 1)
        thumby.display.update()

def main():    
    game = GameManager(RoomTitle(), GameLoop())
    game.start()

    prev_time = 0
    while True:
        t0 = time.ticks_ms()
        tps = (t0 - prev_time) / 1000
        #loop.update(tps)
        game.update(tps)
        prev_time = t0

main()
