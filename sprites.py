import math
from random import randrange, random

import thumby

from Games.Throot.map import ObstacleSlice
from Games.Throot.player import Player, Camera
from Games.Throot.artrepository import *

class Entity:
    """
    An entity exists within the game world. It has coordinates, bounds, and optionally collision and sprite
    """
    def __init__(self, x: int = 0, y: int = 0, width: int = 8, height: int = 8, collision: bytearray = None, sprite: thumby.Sprite = None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.collision = collision
        self.width = width
        self.height = height

    def intersects_pixel(self, loc_x: int, loc_y: int) -> bool:
        """
        Checks to see if this entity intersects a location in the game world.

        :param loc_x:
            An global x location within the game world.
        :param loc_y:
            A global y position within the game world.
        :return:
            True if the collision shape of this entity intersects a point in the world,
            False otherwise.
        """
        if not self.collision:
            return False
        if loc_x < self.x or loc_x >= self.x + self.width or loc_y < self.y or loc_y >= self.y + self.height:
            return False
        rel_x = int(loc_x - self.x)
        rel_y = int(loc_y - self.y)
        return bool((self.collision[rel_x] >> (rel_y)) & 1)

    def can_render(self, camera: Camera) -> bool:
        """
        Checks to see if this sprite is within the game screen.

        :param current_depth:
            The current depth, as measured from the top of the screen. We can display anything
            up to the screen height down from this number.

        :return:
            True if the sprite shows up on screen in any capacity, false otherwise.
        """
        return camera.entity_in_camera(self.x, self.y, self.width, self.height)

    def update(self, tpf: float, player: Player, camera: Camera) -> bool:
        """
        Updates the state of the entity based on the game state.

        :param tpf:
            The number of seconds since the last tick.
        :param current_depth:
            The current depth the game is on.
        :param prev_depth:
            The depth the game was on last tick.

        :return:
            True if the game should keep this entity, false if the game should drop
            this entity from memory.
        """
        return True

    def render(self, tpf: float, camera: Camera) -> bool:
        """
        Sets the position of the sprite and draws it.
        
        :param tpf:
            The number of seconds since the last tick.
        :param current_depth:
            The current depth the game is on.
        :param prev_depth:
            The depth the game was on last tick.

        :return:
            True if the game should actually draw the sprite, false the sprite
            should be hidden.
        """
        if self.sprite:
            coordinates = camera.relative_to_camera(self.x, self.y)
            self.sprite.x = coordinates[0]
            self.sprite.y = coordinates[1]
            if self.can_render(camera):
                thumby.display.drawSprite(self.sprite)
                return True
        return False

class Obstacle(Entity):    
    def update(self, tpf: float, player: Player, camera: Camera) -> bool:
        return True

class Collectible(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 'score' in kwargs and kwargs['score'] or 10
        
    def update(self, tpf: float, player: Player, camera: Camera) -> bool:
        return True


def update_entities(entities, difficulty: int, current_depth: int, prev_depth: int):
    """
    Checks the current game state and generates new sprites based on said state.

    :param current_slice:
        The current obstacle slice we are using. Once the bottom of the slice displays, we switch
        to a new slice.
    :param current_depth:
        The global world depth we are at. This is modulused by the slice height to determine how
        far through the slice we are.
    :param prev_depth:
        The depth we were at during the last tick. This helps make sure we don't miss spawning
        entities

    :return:
        A list of entities to generate this tick.
    """
    
    OBSTACLE_BUFFER = 10
    
    if current_depth == prev_depth:
        # If we haven't moved, we don't need to spawn anything
        return set()
        
    spawned = set()
    max_spawned = randrange(0, difficulty + 1)
    while len(spawned) < max_spawned and random() < (2 * math.pow(difficulty + 0.01, 2)) / (3 * math.pow(difficulty + 0.01, 2) + 20 * (difficulty + 0.01)) + 0.05:
        if random() < 0.2:
            Clazz = Collectible
            if current_depth >= 0:
                sprite_image = collectibleunder
            else:
                sprite_image = collectibleover
        else:
            Clazz = Obstacle
            sprite_image = OBSTACLES[randrange(0, min((difficulty + 1) * 3, len(OBSTACLES)))]
        if sprite_image.width >= thumby.display.width:
            x = 0
        else:
            x = randrange(0, thumby.display.width - sprite_image.width)
        y = current_depth
        if current_depth > prev_depth:
            y += thumby.display.height // 2
        elif current_depth < prev_depth:
            y -= thumby.display.height // 2 + sprite_image.height
        error = False
        for entity in entities | spawned:
            if x > (entity.x - OBSTACLE_BUFFER) and x <= (entity.x + entity.width + OBSTACLE_BUFFER) and y > (entity.y - OBSTACLE_BUFFER) and y <= (entity.y + entity.height + OBSTACLE_BUFFER):
                error = True
                break
        if not error:
            sprite = thumby.Sprite(sprite_image.width, sprite_image.height, sprite_image.image, 0, 0, 0, False, False)
            spawned.add(Clazz(x, y, sprite_image.width, sprite_image.height, sprite_image.collision or sprite_image.image, sprite))
    return spawned
