"""
Title: Lunar Lander Game
Authors: Alec Swainston, Nathan Page, Jordan Huffaker, Samuel Omondi
"""
import math
from typing import Optional
import arcade

SCREEN_TITLE = "Lunar Lander"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 64

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.25

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 20

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

class Game():
    pass

class Window(arcade.Window):
    
    def __init__(self, width, height, title):
        pass

class Lander():
    pass

class Landscape():
    
    def __init__(self):
        map_name = "landscape.tmx"
    
    def read(self,map_name):
        my_map = arcade.tilemap.read_tmx(map_name)
        
        # Read in the map layers
        self.wall_list = arcade.tilemap.process_layer(my_map, 'Landing Zone', SPRITE_SCALING_TILES)

class Score():
    pass

class Fuel():
    pass

class Movement():
    pass

if __name__ == "__main__":
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)