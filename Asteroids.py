"""
This Program is just a rough personal project.  It's movement is similar to the game 'Asteroids'
Author: Alec Swainston
"""

import arcade

class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(50, 100)

        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = 100
        self.player_y = 200
        self.player_speed = 250
        
        self.sprite1 = arcade.Sprite("Arcade API Tutorials/sprites/lander.png", center_x = 100, center_y = 100)

        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.gravity = True
        self.gravForce = 50
    
    def on_draw(self):
        arcade.start_render()
        self.sprite1.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.right = True
        if symbol == arcade.key.LEFT:
            self.left = True
        if symbol == arcade.key.UP:
            self.sprite1.strafe(2)
            self.up = True
        if symbol == arcade.key.DOWN:
            self.down = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            self.right = False
        if symbol == arcade.key.LEFT:
            self.left = False
        if symbol == arcade.key.UP:
            self.up = False
        if symbol == arcade.key.DOWN:
            self.down = False  
    
    def on_mouse_motion(self, x, y, dx, dy):
        #if x > 1:
        #    self.sprite1.turn_right(2)
        #if x < 1:
        #    self.sprite1.turn_left(2)
        pass
    
    def on_update(self, delta_time):
        if self.right:
            self.sprite1.turn_right(2)
            #self.player_x += self.player_speed * delta_time
        if self.left:
            self.sprite1.turn_left(2)
            #self.player_x -= self.player_speed * delta_time
        if self.up:
            self.sprite1.strafe(0.05)
            pass
            #self.player_y += self.player_speed * delta_time
        if self.down:
            pass
            #self.player_y -= self.player_speed * delta_time
        #if self.gravity == True:
            #self.player_y -= self.gravForce * delta_time
            
        #self.sprite1.set_position(self.player_x, self.player_y)
        self.sprite1.update()
MyGameWindow(1280, 720, "My Game Window")
arcade.run()