"""
Title: Lunar Lander Game
Authors: Alec Swainston, Nathan Page, Jordan Huffaker, Samuel Omondi
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Lunar Lander"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 3


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.

        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        #Create the Sprite lists (add the floor later)
        self.player_list = arcade.SpriteList()
        self.landing_zone_list = arcade.SpriteList(use_spacial_hash=True)

        # Set up the lander, specifically placing it at these coordinates (centered for now).
        image_source = "landerAlpha.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 325
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Render the screen. """

        #Clear the screen to the background color
        arcade.start_render()
        
        #Draw Sprites (add floor later)
        self.player_list.draw()

class physicsEngine:
    def __init__(self.player_sprite, self.landing_zone_list):
        



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()