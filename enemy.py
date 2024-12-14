import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA
from typing import List, Dict

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type: str, waypoints: List[Vector2], images: Dict[str, pg.Surface]):
        """
        Initialize the Enemy instance.

        :param enemy_type: The type of the enemy.
        :param waypoints: The list of waypoints for the enemy to follow.
        :param images: A dictionary of images for different enemy types.
        """
        super().__init__()
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world) -> None:
        """
        Update the enemy's state.

        :param world: The game world instance.
        """
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world) -> None:
        """
        Move the enemy along the waypoints.

        :param world: The game world instance.
        """
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.reach_end(world)

        dist = self.movement.length()
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self) -> None:
        """
        Rotate the enemy to face the next waypoint.
        """
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world) -> None:
        """
        Check if the enemy is still alive.

        :param world: The game world instance.
        """
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

    def reach_end(self, world) -> None:
        """
        Handle the enemy reaching the end of the path.

        :param world: The game world instance.
        """
        self.kill()
        world.health -= 1
        world.missed_enemies += 1