
import arcade
import math

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Lunar Lander"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING

# Physics
MOVEMENT_SPEED = 10 * SPRITE_SCALING
JUMP_SPEED = 28 * SPRITE_SCALING
GRAVITY = .01 * SPRITE_SCALING
ANGLE_SPEED = 5

# These numbers represent "states" that the game can be in.
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        super().__init__(width, height, title)

        # Sprite lists

        # We use an all-wall list to check for collisions.
        self.all_wall_list = None

        # Drawing non-moving walls separate from moving walls improves performance.
        self.static_wall_list = None
        self.moving_wall_list = None
        self.floor_list = None
        self.explosions_list = None
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(
            file_name, sprite_width, sprite_height, columns, count)
        self.hit_sound = arcade.sound.load_sound(
            ":resources:sounds/explosion2.wav")

        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.game_over = False

        # Start 'state' will be showing the first page of instructions.
        self.current_state = INSTRUCTIONS_PAGE_0
        self.instructions = []
        texture = arcade.load_texture("game_over_PNG57.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("275-2755358_play-again-button-png-clip-art.png")
        self.instructions.append(texture)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_wall_list = arcade.SpriteList()
        self.static_wall_list = arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(
            ":resources:images/space_shooter/playerShip3_orange.png", SPRITE_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 600
        self.player_list.append(self.player_sprite)

        # Create floor
        for i in range(30):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
            wall.bottom = 0
            wall.center_x = i * GRID_PIXEL_SIZE
            self.static_wall_list.append(wall)
            self.floor_list.append(wall)

        # Create platform side to side
        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 2 * GRID_PIXEL_SIZE
        wall.center_x = 5 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        # Create platform side to side
        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 2 * GRID_PIXEL_SIZE
        wall.center_x = 8 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 4 * GRID_PIXEL_SIZE
        wall.center_x = 7 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        # second one
        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 6 * GRID_PIXEL_SIZE
        wall.center_x = 10 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 4 * GRID_PIXEL_SIZE
        wall.center_x = 9 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        # Create platform side to side first one
        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 5 * GRID_PIXEL_SIZE
        wall.center_x = 5 * GRID_PIXEL_SIZE
        # wall.boundary_left = 2 * GRID_PIXEL_SIZE
        # wall.boundary_right = 8 * GRID_PIXEL_SIZE
        # wall.change_x = 2 * SPRITE_SCALING

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(
            ":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = 7 * GRID_PIXEL_SIZE
        wall.center_x = 7 * GRID_PIXEL_SIZE

        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           self.floor_list,
                                           gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.game_over = False
    
    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    # STEP 3: Add this function

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

    def draw_game(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing

        # Draw the sprites.
        self.static_wall_list.draw()
        self.moving_wall_list.draw()
        self.floor_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()

        # Put the text on the screen.
        # Adjust the text position based on the viewport so that we don't
        # scroll the text too.
        distance = self.player_sprite.right
        output = f"Distance: {distance}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20,
                         arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()


    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.UP:
                self.player_sprite.speed = MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_angle = ANGLE_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_angle = -ANGLE_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.current_state == GAME_RUNNING:
            # Call update on all sprites
            self.player_list.update()
            self.physics_engine.update()
            self.explosions_list.update()

            for walls in self.moving_wall_list:
                hit_list = arcade.check_for_collision_with_list(
                    walls, self.player_list)

                if len(hit_list) > 0:
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    explosion.update()

                    # Add to a list of sprites that are explosions
                    self.explosions_list.append(explosion)

                for player in hit_list:
                    player.remove_from_sprite_lists()
                    self.current_state = GAME_OVER

                    arcade.sound.play_sound(self.hit_sound)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
