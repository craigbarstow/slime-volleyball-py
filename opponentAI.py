"""
Class designed to take inputs on ball position and velocity and make movement decisions for
computer controlled opponent
"""
from math import sqrt

class OpponentAI:
    def __init__(self, canvas, canvas_width, canvas_height, floor_height, ball_size, player_size, ball_grav):
        #FIXME remove this
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.floor_height = floor_height
        self.ball_size = ball_size
        self.player_size = player_size
        self.ball_grav = ball_grav
        self.movement_buffer_size = 25


    def chooseMovementX(self, ball_center, opponent_center, ball_dx, calculated_landing_spot):
        if ball_center[0] > self.canvas_width*.5 and ball_dx > 0:
            if abs(opponent_center[0] - self.canvas_width*.25) < self.movement_buffer_size:
                return
            elif opponent_center[0] < self.canvas_width*.25:
                return "right"
            elif opponent_center[0] > self.canvas_width*.25:
                return "left"
        #if ball on left side and heading left, square up
        else:
            if abs(calculated_landing_spot-opponent_center[0]) < self.movement_buffer_size:
                return
            elif opponent_center[0] > calculated_landing_spot:
                return "left"
            elif opponent_center[0] < calculated_landing_spot:
                return "right"

    def decideToJump(self):
        #if jumping is prudent
        return True