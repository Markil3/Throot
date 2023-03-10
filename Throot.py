import time
import math

import thumby

import Games.Throot.map
import Games.Throot.sprites

from random import randrange

from Games.Throot.artrepository import *
from Games.Throot.player import Player, Camera
from Games.Throot.map import ObstacleSlice, OBSTACLE_SLICES
from Games.Throot.sprites import Entity, Obstacle, Collectible, update_entities
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
    def __init__(self):
        self.ind_button = 0
    
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
        #thumby.display.drawSprite(sprite_title.width, sprite_title.height, sprite_title.image)
        
        thumby.display.blit(sprite_title.image, 0, 0, sprite_title.width, sprite_title.height, 
        -1, 0, 0)
        
        # title text
        chrx = 5
        chry = 7
        buff = 2
        
        x = 14#int(round(thumby.display.width / 2 - (chr_len * len(title_text)) / 2))
        y = 40 - chry - buff#int(round(thumby.display.height / 2 - chr_len / 2))
        
        w = chrx * 6 + buff
        h = chry + buff
        thumby.display.drawFilledRectangle(x - buff, y - buff, w, h * 2 + buff, 0)
        #thumby.display.drawText('press a', x, y, 0)
        thumby.display.drawText('start', x, y, 1)
        
        spr_b = thumby.Sprite(sprite_buttona1.width, sprite_buttona1.height, sprite_buttona1.image + sprite_buttona2.image, 2, 40 - 8, 
        -1, 0, 0)
        
        # thumby.display.blit(sprite_buttona.image, 2, 40 - 8, sprite_buttona.width, sprite_buttona.height, 
        # -1, 0, 0)
        
        self.ind_button = (self.ind_button + 1) % (2 * CONST_FPS)
        spr_b.setFrame(self.ind_button // (2 * CONST_FPS))
        
        #print(self.ind_button // CONST_FPS)
        
        thumby.display.drawSprite(spr_b)
        
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
        
        seed_sprite = thumby.Sprite(seed.width, seed.height, seed.image, 0, 0, 0, False, False)
        self.seed = Entity((thumby.display.width - seed.width) // 2, 0, seed.width, seed.height, None, seed_sprite)
    
    def start(self, event):
        self.entities.clear()
        self.entities.add(
            self.seed
        )
        self.current_obstacle_slice = OBSTACLE_SLICES[0]
        self.player = Player()
        self.player.yspeed = 10
        self.score = 'score' in event and event['score'] or 0
        self.level = 'level' in event and event['level'] or 0
        
        self.finish_depth = 100 + 5 * self.level ** 2
        self.camera = Camera(self.player)

    def get_obstacle_slice(self):
        return OBSTACLE_SLICES[randrange(0, len(OBSTACLE_SLICES))]
    
    def draw_sky(self):
        sky_x = 0
        sky_y = -thumby.display.height
        sky_width = thumby.display.width
        sky_height = thumby.display.height
        if self.camera.entity_in_camera(sky_x, sky_y, sky_width, sky_height):
            sky_x, sky_y = self.camera.relative_to_camera(sky_x, sky_y)
            thumby.display.drawFilledRectangle(int(sky_x), int(sky_y), int(sky_width), int(sky_height), 1)
        sky_x = 0
        sky_y = 0
        sky_width = thumby.display.width
        sky_height = thumby.display.height
        if self.camera.entity_in_camera(sky_x, sky_y, sky_width, sky_height):
            sky_x, sky_y = self.camera.relative_to_camera(sky_x, sky_y)
            thumby.display.drawFilledRectangle(int(sky_x), int(sky_y), int(sky_width), int(sky_height), 0)
        
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
                elif isinstance(entity, Collectible):
                    self.score += entity.score
                    to_remove.add(entity)
        self.entities -= to_remove
        
        self.score += int(abs(self.player.ysub - self.player.prev_y) * 10)
        
        # finish level
        if self.player.y > self.finish_depth + int(thumby.display.height * 1.5):
            self.score += 20
            self.level += 1
            self.start({
                'score': self.score,
                'level': self.level
            })

        thumby.display.fill(0)
        self.draw_sky()
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
