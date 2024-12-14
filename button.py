import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from typing import Tuple

class Button:
    def __init__(self, x: int, y: int, image: Surface, single_click: bool):
        """
        Initialize the Button instance.

        :param x: The x-coordinate of the button.
        :param y: The y-coordinate of the button.
        :param image: The image to be used for the button.
        :param single_click: If True, the button can only be clicked once.
        """
        self.image = image
        self.rect: Rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface: Surface) -> bool:
        """
        Draw the button on the given surface and check for clicks.

        :param surface: The surface to draw the button on.
        :return: True if the button is clicked, False otherwise.
        """
        action = False
        pos = self.get_mouse_position()

        if self.is_mouse_over(pos) and self.is_mouse_clicked():
            action = True
            if self.single_click:
                self.clicked = True

        if not self.is_mouse_pressed():
            self.clicked = False

        surface.blit(self.image, self.rect)
        return action

    def get_mouse_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position.

        :return: A tuple containing the x and y coordinates of the mouse.
        """
        return pg.mouse.get_pos()

    def is_mouse_over(self, pos: Tuple[int, int]) -> bool:
        """
        Check if the mouse is over the button.

        :param pos: The current mouse position.
        :return: True if the mouse is over the button, False otherwise.
        """
        return self.rect.collidepoint(pos)

    def is_mouse_clicked(self) -> bool:
        """
        Check if the mouse button is clicked.

        :return: True if the mouse button is clicked, False otherwise.
        """
        return pg.mouse.get_pressed()[0] == 1 and not self.clicked

    def is_mouse_pressed(self) -> bool:
        """
        Check if the mouse button is pressed.

        :return: True if the mouse button is pressed, False otherwise.
        """
        return pg.mouse.get_pressed()[0] == 1