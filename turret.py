import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA
from pygame.surface import Surface
from pygame.sprite import Group
from typing import List, Dict

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheets: List[Surface], tile_x: int, tile_y: int, shot_fx: pg.mixer.Sound):
        """
        Initialize the Turret instance.

        :param sprite_sheets: List of sprite sheets for different upgrade levels.
        :param tile_x: The x-coordinate of the turret's tile.
        :param tile_y: The y-coordinate of the turret's tile.
        :param shot_fx: The sound effect to play when the turret shoots.
        """
        super().__init__()
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        # Position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.shot_fx = shot_fx

        # Animation variables
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # Update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Create transparent circle showing range
        self.range_image = self.create_range_image()
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self, sprite_sheet: Surface) -> List[Surface]:
        """
        Extract images from the sprite sheet.

        :param sprite_sheet: The sprite sheet to extract images from.
        :return: A list of images.
        """
        size = sprite_sheet.get_height()
        animation_list = [sprite_sheet.subsurface(x * size, 0, size, size) for x in range(c.ANIMATION_STEPS)]
        return animation_list

    def create_range_image(self) -> Surface:
        """
        Create a transparent circle showing the turret's range.

        :return: The range image.
        """
        range_image = pg.Surface((self.range * 2, self.range * 2))
        range_image.fill((0, 0, 0))
        range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(range_image, "grey100", (self.range, self.range), self.range)
        range_image.set_alpha(100)
        return range_image

    def update(self, enemy_group: Group, world) -> None:
        """
        Update the turret's state.

        :param enemy_group: The group of enemies.
        :param world: The game world instance.
        """
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group: Group) -> None:
        """
        Find an enemy to target.

        :param enemy_group: The group of enemies.
        """
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    self.target.health -= c.DAMAGE
                    self.shot_fx.play()
                    break

    def play_animation(self) -> None:
        """
        Play the firing animation.
        """
        self.original_image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def upgrade(self) -> None:
        """
        Upgrade the turret.
        """
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animation_list[self.frame_index]
        self.range_image = self.create_range_image()
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface: Surface) -> None:
        """
        Draw the turret on the given surface.

        :param surface: The surface to draw the turret on.
        """
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)