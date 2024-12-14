import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA
from typing import List, Dict, Tuple

class World:
    def __init__(self, data: Dict, map_image: pg.Surface):
        """
        Initialize the World instance.

        :param data: The level data.
        :param map_image: The image of the map.
        """
        self.level = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints: List[Tuple[float, float]] = []
        self.level_data = data
        self.image = map_image
        self.enemy_list: List[str] = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self) -> None:
        """
        Process the level data to extract relevant information.
        """
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data: List[Dict[str, float]]) -> None:
        """
        Process the waypoints data to extract individual sets of x and y coordinates.

        :param data: The waypoints data.
        """
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self) -> None:
        """
        Process the enemies data to create a list of enemies to spawn.
        """
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type, enemies_to_spawn in enemies.items():
            self.enemy_list.extend([enemy_type] * enemies_to_spawn)
        random.shuffle(self.enemy_list)

    def check_level_complete(self) -> bool:
        """
        Check if the level is complete.

        :return: True if the level is complete, False otherwise.
        """
        return (self.killed_enemies + self.missed_enemies) == len(self.enemy_list)

    def reset_level(self) -> None:
        """
        Reset the level by clearing enemy variables.
        """
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def draw(self, surface: pg.Surface) -> None:
        """
        Draw the map image on the given surface.

        :param surface: The surface to draw the map on.
        """
        surface.blit(self.image, (0, 0))