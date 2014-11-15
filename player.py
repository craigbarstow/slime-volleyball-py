#created by Craig Barstow on 10/28/2014 for Slime Volleyball Project

class Player:
    def __init__(self, canvas, player_x, player_y, player_size, canvas_width, net_width, color):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.net_width = net_width
        self.movement_distance = 15
        self.player_x = player_x
        self.initial_player_y = player_y
        self.player_y = self.initial_player_y
        self.player_dy = 0
        self.jump_power = -120
        self.player_size = player_size
        self.center = [0,0]
        self.player = self.canvas.create_arc(self.player_x,self.player_y,self.player_x+player_size,self.player_y+player_size,
                                             extent=180,fill=color)
        self.jump_timeout_count = 70
        self.jump_wait_time = 70

        self.setCenter()

    def moveCharacter(self, event):
        if event.char == 'a':
            self.player_x -= self.movement_distance
            if self.player_x < self.canvas_width*.5+self.net_width*.5:
                self.player_x = self.canvas_width*.5+self.net_width*.5
        elif event.char == 'd':
            self.player_x += self.movement_distance
            if self.player_x > self.canvas_width-self.player_size:
                self.player_x = self.canvas_width-self.player_size
        elif event.char == 'w':
            if self.jump_timeout_count >= self.jump_wait_time:
                #zero velocity to allow double jumps
                self.player_dy = 0
                #add upward velocity
                self.player_dy += self.jump_power/10.0
                #zero jump timer
                self.jump_timeout_count = 0
        self.setCenter()
        self.drawCharacter(False)

    def drawCharacter(self, floor_collision_status):
        if floor_collision_status:
            self.player_y = self.initial_player_y
            self.player_dy = 0
        self.canvas.coords(self.player, self.player_x, self.player_y,
                           self.player_x+self.player_size, self.player_y+self.player_size)

    def setCenter(self):
        self.center[0] = self.player_x + self.player_size*.5
        self.center[1] = self.player_y + self.player_size*.5


