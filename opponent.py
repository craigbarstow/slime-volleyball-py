#Created by Craig Barstow on 10/28/2014 for Slime Volleyball Project

class Opponent:
    def __init__(self, canvas, opponent_x, opponent_y, player_size, canvas_width, net_width, color):
        self.canvas = canvas
        self.canvas_width =  canvas_width
        self.net_width = net_width
        self.movement_distance = 6 #7.5 seems good
        self.opponent_x = opponent_x
        self.opponent_y = opponent_y
        self.opponent_dy = 0
        self.opponent_size = player_size
        self.center = [0,0]
        self.player = self.canvas.create_arc(self.opponent_x, self.opponent_y,
                                                  self.opponent_x+player_size,
                                                  self.opponent_y+player_size,
                                                  extent=180, fill=color)
        self.setCenter()

    def moveLeft(self):
        self.opponent_x -= self.movement_distance
        if self.opponent_x < 0:
            self.opponent_x = 0
        self.setCenter()

    def moveRight(self):
        self.opponent_x += self.movement_distance
        if self.opponent_x > self.canvas_width*.5-self.net_width*.5-self.opponent_size:
            self.opponent_x = self.canvas_width*.5-self.net_width*.5-self.opponent_size
        self.setCenter()

    def drawOpponent(self):
        self.canvas.coords(self.player, self.opponent_x, self.opponent_y,
                           self.opponent_x+self.opponent_size,self.opponent_y+self.opponent_size)

    def setCenter(self):
        self.center[0] = self.opponent_x + self.opponent_size*.5
        self.center[1] = self.opponent_y + self.opponent_size*.5