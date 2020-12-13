"""
Title: Lunar Lander Game
Authors: Alec Swainston, Nathan Page, Jordan Huffaker, Samuel Omondi
"""
import math
from typing import Optional
import arcade
import os

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

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 10

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 450

#Player Movement Force
PLAYER_MOVE_FORCE = 65

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

         # Physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        # MM: Lander object
        self.lander = Lander()
        self.output_service = OutputService()
        self.input_service = InputService()

    def setup(self):
        """ Set up everything with the game """

        self.output_service.setup()

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)
        
        self.physics_engine.add_collision_handler("player", "crash", post_handler=OutputService.wall_hit_handler)

        self.physics_engine.add_collision_handler("player", "land", post_handler=OutputService.platform_hit_handler)
        # Add the player.
        self.physics_engine.add_sprite(self.output_service.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        #self.physics_service.add_sprite(self.output_service.player_sprite)

        # Create the crash zones.
        self.physics_engine.add_sprite_list(self.output_service.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="crash",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Create the Landing Zones
        self.physics_engine.add_sprite_list(self.output_service.platform_list,  friction=WALL_FRICTION, collision_type="land", body_type=arcade.PymunkPhysicsEngine.STATIC) 

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.input_service.key_input(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        self.input_service.key_release(key, modifiers)
   
    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.input_service.right and self.lander._fuel > 0:
            force = (PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.output_service.player_sprite, force)
            self.lander._fuel -= 1
        elif self.input_service.left and self.lander._fuel > 0:
            force = (-PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.output_service.player_sprite, force)
            self.lander._fuel -= 1
        elif self.input_service.up and self.lander._fuel > 0:
            force = (0, PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.output_service.player_sprite, force)
            self.lander._fuel -= 1

        # MM: Check for collision with ground
        # MM: Update state of lander
        # Moving objects in physics engine
        self.physics_engine.step()

    def on_draw(self):
        """ Draw everything """
        
        arcade.start_render()
        self.output_service.wall_list.draw()
        self.output_service.platform_list.draw()

        self.output_service.draw_lander(self.lander)
        self.output_service.draw_fuel(self.lander)
        self.output_service.draw_altitude(self.lander)
        self.output_service.draw_success()

        

class Lander:
    """The Ship the Player controls
        Stereotype: 
            Structurer, Service Provider, Information Holder
    """
    def __init__(self):
        self._fuel = 500
        self._has_crashed = False

    def get_fuel(self):
        return self._fuel

    

class InputService:

    def __init__(self):
        self.right = False
        self.left = False
        self.up = False

    def key_input(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.right = True
        elif key == arcade.key.LEFT:
            self.left = True
        elif key == arcade.key.UP:
            self.up = True

    def key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.right = False
        elif key == arcade.key.LEFT:
            self.left = False
        elif key == arcade.key.UP:
            self.up = False
    


class OutputService:
    
    def __init__(self):
        self.player_sprite: Optional[arcade.Sprite] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.platform_list: Optional[arcade.SpriteList] = None
        arcade.set_background_color(arcade.color.BLACK)
        self.on_ground = False

    def setup(self):
        # Create Sprite Lists
        self.player_list = arcade.SpriteList()
        
        # Read in Map
        self.directory = os.path.dirname(__file__)
        map_name = os.path.join(self.directory, "moon.tmx")
        my_map = arcade.tilemap.read_tmx(map_name)
        
        # Read in the map layers
        self.wall_list = arcade.tilemap.process_layer(my_map, 'CRASH', SPRITE_SCALING_TILES)
        self.platform_list = arcade.tilemap.process_layer(my_map, 'LAND', SPRITE_SCALING_TILES)
        
        # Create player sprite
        file_name = os.path.join(self.directory, "lander.png")
        self.player_sprite = arcade.Sprite(file_name, SPRITE_SCALING_PLAYER)

        # Set player location
        grid_x = 12
        grid_y = 15
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

    def draw_lander(self, lander):
        self.player_list.draw()
    
    def draw_explosion(self, lander):
        pass

    def draw_fuel(self, lander):
        if lander._fuel > 0:
            fuel_text = f"Fuel: {(lander._fuel/10)*2}%"
            arcade.draw_text(fuel_text, 12, 600, arcade.csscolor.WHITE, 18)
        else:
            fuel_text = f"Fuel: Empty!"
            arcade.draw_text(fuel_text, 12, 600, arcade.csscolor.RED, 18)

    def draw_altitude(self, lander):
        altitude = self.player_sprite.center_y
        altitude_text = f"Altitude: {altitude:.0f}"
        arcade.draw_text(altitude_text, 165, 600, arcade.csscolor.WHITE, 18)
    
    def wall_hit_handler(self, player_sprite, wall_list, _arbiter, _space):
        player_sprite.remove_from_sprite_lists()

    def platform_hit_handler(self, player_sprite, platform_list, _arbiter, _space):
        self.on_ground = True

    def draw_success(self):
        if self.on_ground == True:
            win_text = f"You Landed!"
            arcade.draw_text(win_text, 250, 250, arcade.csscolor.GREEN, 24)
        
        


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

