import time
import thumby
import math

import Games.Throot.map
import Games.Throot.sprites
from Games.Throot.artrepository import OBSTACLES

from random import randrange

import thumby

from Games.Throot.map import ObstacleSlice, OBSTACLE_SLICES
from Games.Throot.sprites import update_entities

class GameLoop:
    def __init__(self):
        self.current_depth = 0
        self.diving_velocity = 10
        self.diving_accel = 0
        self.current_obstacle_slice = OBSTACLE_SLICES[0]
        self.entities = set()

    def get_obstacle_slice(self):
        return OBSTACLE_SLICES[randrange(0, len(OBSTACLE_SLICES))]

    def update(self, tpf):
        """
        Executes one tick of the game
        """
        prev_depth = self.current_depth
        self.diving_velocity += self.diving_accel * tpf
        self.current_depth += self.diving_velocity * tpf

        if self.current_depth % ObstacleSlice.height < prev_depth % ObstacleSlice.height:
            self.current_obstacle_slice = self.get_obstacle_slice()

        # Generate new entities as needed
        self.entities |= update_entities(self.current_obstacle_slice, self.current_depth, prev_depth)

        # Updates the entities
        to_remove = set()
        for entity in self.entities:
            if not entity.update(tpf, self.current_depth, prev_depth):
                to_remove.add(entity)
        self.entities -= to_remove

        thumby.display.fill(0)
        # Draw the entities
        for entity in self.entities:
            entity.render(tpf, self.current_depth, prev_depth)
        thumby.display.update()

def main():
    # Set the FPS (without this call, the default fps is 30)
    thumby.display.setFPS(60)

    print("Starting game loop")
    loop = GameLoop()

    prev_time = 0
    while True:
        t0 = time.ticks_ms()
        tps = (t0 - prev_time) / 1000
        loop.update(tps)
        prev_time = t0

main()