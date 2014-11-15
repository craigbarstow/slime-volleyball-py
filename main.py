from Tkinter import *
#from vectors import *
import player, opponent, collisionHandler, math, opponentAI
import random

class SlimeVolleyball:
    def __init__(self, parent):
        #canvas variables
        self.canvas_width = 700 #800
        self.canvas_height = 500
        self.floor_height = 5
        self.net_height = self.canvas_height/5
        self.net_width = 6
        self.net_points = [self.canvas_width/2.0-self.net_width/2.0, self.canvas_height-self.floor_height-self.net_height,
                           self.canvas_width/2.0+self.net_width/2.0, self.canvas_height-self.floor_height]
        #player variables
        self.player_size = 100
        #ball variables
        self.ball_size = 60
        self.ball_start_x = 0
        self.ball_x = 0
        self.ball_start_y = self.canvas_height*.4
        self.ball_y = self.ball_start_y
        self.ball_center = [0,0]

        #physics/speed variables
        self.dx = 0
        self.dy = 0
        self.player_gravity_strength = 40
        self.ball_gravity_strength = 10
        #divisor, to make the nice int gravity variables appropriately small
        self.grav_divisor = 100.0
        self.wait_time = 5
        self.update_ball_landing_spot_flag = True
        self.calculated_landing_spot = 0
        #opponent variables




        #set up canvas
        self.canvas = Canvas(parent, width=self.canvas_width, height=self.canvas_height, background="grey")
        self.canvas.grid(column=0,row=0)
        self.canvas.wait_visibility()

        #set up floor
        self.canvas.create_rectangle(0, self.canvas_height-self.floor_height, self.canvas_width, self.canvas_height, fill="brown4")

        #fixme remove this eventually
        self.expected_landing_spot = self.canvas.create_oval(self.canvas_width*.5-self.floor_height*.5,
                                                             self.canvas_height-self.floor_height,
                                                             self.canvas_width*.5+self.floor_height*.5,
                                                             self.canvas_height, fill="white")

        #set up net
        self.canvas.create_rectangle(self.net_points[0],self.net_points[1],
                                     self.net_points[2],self.net_points[3], fill = "black")

        #add start button
        self.startButton = Button(parent, text="Play", command=self.preLoop)
        self.startButton.grid(row=2, column=0)

        #add player
        player_x = self.canvas_width*.75-self.player_size*.5
        player_y = self.canvas_height-self.floor_height-self.player_size*.5
        self.player = player.Player(self.canvas, player_x, player_y, self.player_size, self.canvas_width, self.net_width, "blue")
        parent.bind('a', self.player.moveCharacter)
        parent.bind('d', self.player.moveCharacter)
        parent.bind('w', self.player.moveCharacter)

        #fixme create players this way
        #self.canvas.create_arc(100,100,200,200,extent=180,fill="blue")

        #add opponent
        opponent_x = self.canvas_width*.25-self.player_size*.5
        opponent_y = self.canvas_height-self.floor_height-self.player_size*.5
        self.opponent = opponent.Opponent(self.canvas, opponent_x, opponent_y, self.player_size,
                                          self.canvas_width, self.net_width, "red")
        #add opponent AI
        #FIXME remove canvas parameter
        self.ai = opponentAI.OpponentAI(self.canvas, self.canvas_width, self.canvas_height, self.floor_height,
                                        self.ball_size, self.player_size, self.ball_gravity_strength)

        #create ball
        self.ball_start_x = self.player.center[0]-self.ball_size*.5
        self.ball_x = self.ball_start_x
        self.ball = self.canvas.create_oval(self.ball_x, self.ball_y,
                                            self.ball_x+self.ball_size, self.ball_y+self.ball_size,
                                            fill="white")
        self.ballSetCenter()
        #initialize collision handler
        self.collision_handler = collisionHandler.CollisionHandler(self.canvas_width, self.canvas_height,
                                                                   self.floor_height, self.net_points,
                                                                   self.ball_size, self.player_size)

        self.v_vector = self.canvas.create_line(-1, -1, 0, 0, fill="red")
        self.centers_vector = self.canvas.create_line(-20,-20,-19,-19, fill="black")
        self.out_vector = self.canvas.create_line(-1, -1, 0, 0, fill="green")

    def preLoop(self):
        #clear any built up player dy
        self.player.player_dy = 0
        #hide play button
        self.startButton.grid_remove()
        self.resetBall()
        self.gameLoop()

    def gameLoop(self):
         # gravity equation
        self.dy += self.ball_gravity_strength/self.grav_divisor
        #update ball position
        self.ball_x += self.dx
        self.ball_y += self.dy
        self.ballSetCenter()
        #display ball in its updated position
        self.canvas.coords(self.ball, self.ball_x, self.ball_y,
                           self.ball_x+self.ball_size, self.ball_y+self.ball_size)
        #update player position
        #if player not on floor
        #if self.player.center[1] < self.canvas_height - self.floor_height - self.player_size*.5:
        self.player.player_dy += self.player_gravity_strength/self.grav_divisor
        self.player.player_y += self.player.player_dy
        self.player.setCenter()
        self.player.drawCharacter(self.collision_handler.checkForPlayerFloorCollision(self.player.center[1]))
        #increment jump timeout counter
        self.player.jump_timeout_count += 1

        #opponent stuff
        opponent_move = self.ai.chooseMovementX(self.ball_center, self.opponent.center, self.dx, self.calculated_landing_spot)
        if opponent_move == "left":
            self.opponent.moveLeft()
        elif opponent_move == "right":
            self.opponent.moveRight()

        #draw opponent in new position
        self.opponent.drawOpponent()

        #ball collision detection stuff
        """
        if self.collision_handler.ballHitFloor(self.ball_center[1]):
            #increment score, possibly display alert of some kind
            self.postLoop()
            #break from recursion
            return
        """
        if self.collision_handler.ballHitFloor(self.ball_center[1]):
            self.dy *= -1
            self.ball_y = self.canvas_height - self.floor_height - self.ball_size
            self.update_ball_landing_spot_flag = True
        elif self.collision_handler.checkForCeilingCollision(self.ball_center[1]):
            #reverse motion in Y direction if ball hits the ceiling
            self.dy *= -1
            self.ball_y = 0
            self.ballSetCenter()
            self.update_ball_landing_spot_flag = True
        elif self.collision_handler.checkForWallCollision(self.ball_center[0]):
            #reverse motion in x direction if ball hits a wall
            self.dx *= -1
            if self.ball_x < self.canvas_width/2.0:
                self.ball_x = 0
            else:
                self.ball_x = self.canvas_width-self.ball_size
            self.ballSetCenter()
            self.update_ball_landing_spot_flag = True
        elif self.collision_handler.checkForNetSideCollision(self.ball_center):
            #fixme Set the x coordinate of the ball to be outside the net
            #reverse motion in x direction if ball collides with side of net
            self.dx *= -1
            self.update_ball_landing_spot_flag = True
        elif self.collision_handler.checkForTopNetCollision(self.ball_center, self.dy):
            #reverse motion in y direction if ball collides with top of net
            print self.dy
            self.dy *= -1
            self.update_ball_landing_spot_flag = True
        elif self.collision_handler.checkForPlayerCollision(self.ball_center, self.player.center):
            self.playerHitsBall()
            self.debugWithArt()
            self.update_ball_landing_spot_flag = True
            #return
        elif self.collision_handler.checkForPlayerCollision(self.ball_center, self.opponent.center):
            self.opponentHitsBall()
            self.update_ball_landing_spot_flag = True

        #calculate new landing position of ball if a collision has occurred
        if self.update_ball_landing_spot_flag:
            self.calculateBallLandingSpot()
            self.update_ball_landing_spot_flag = False

        #aaaaaaand again!
        self.canvas.after(self.wait_time, self.gameLoop)

    def postLoop(self):
        #bring start button back
        self.startButton.grid(row=1,column=0)

    def calculateBallLandingSpot(self):
        actual_grav = self.ball_gravity_strength/self.grav_divisor
        #displacement is distance between floor and bottom of ball
        displacement = self.canvas_height-self.floor_height - (self.ball_center[1]+self.ball_size*.5)
        #if displacement is negative, set to zero so it wont break square root
        if displacement < 0:
            displacement = 0
        #find final velocity (dy)
        #vf = math.sqrt(2ad+vo^2)
        dy_final = math.sqrt(2*actual_grav*displacement+abs(self.dy)**2)
        #solve for "time"
        #vf = v0 + at
        #acceleration in pixels per loop
        #t = (vf - v0)/a
        time_to_apex_and_back = 0
        if self.dy < 0:
            time_to_apex_and_back = (-self.dy - self.dy)/float(actual_grav)
        time = (dy_final - abs(self.dy))/float(actual_grav) + time_to_apex_and_back
        self.calculated_landing_spot = self.ball_center[0]+self.dx*time
        #if landing spot off screen, anticipate collision with wall, and recalculate appropriately
        if self.calculated_landing_spot < 0:
            self.calculated_landing_spot *= -1
        elif self.calculated_landing_spot > self.canvas_width:
            self.calculated_landing_spot -= self.calculated_landing_spot - self.canvas_width

        #fixme remove this eventually, for debug purposes only
        #redraw landing spot indicator
        self.canvas.coords(self.expected_landing_spot, self.calculated_landing_spot-self.floor_height*.5,
                               self.canvas_height-self.floor_height, self.calculated_landing_spot+self.floor_height*.5,
                               self.canvas_height)

    def ballSetCenter(self):
        ball_center_x = self.ball_x + self.ball_size*.5
        ball_center_y = self.ball_y + self.ball_size*.5
        self.ball_center = [ball_center_x, ball_center_y]

    def resetBall(self):
        self.canvas.coords(self.ball, self.ball_start_x, self.ball_start_y,
                           self.ball_start_x+self.ball_size, self.ball_start_y+self.ball_size)
        #FIXME uncomment this
        self.dx = 0#random.randint(-10,10)
        self.dy = 0
        self.ball_x = self.ball_start_x
        self.ball_y = self.ball_start_y

    def playerHitsBall(self):
        """
        initial_alignment_vector = [self.ball_center[0]-self.player.center[0], self.ball_center[1]-self.player.center[1]]
        #unit vector in direction of line between ball centers
        alignment_vector = [initial_alignment_vector[0]/math.sqrt(initial_alignment_vector[0]**2+initial_alignment_vector[1]**2),
                            initial_alignment_vector[1]/math.sqrt(initial_alignment_vector[0]**2+initial_alignment_vector[1]**2)]
        #self.canvas.create_line(200,200,200+alignment_vector[0]*50,200+alignment_vector[1]*50,fill="white")
        #unit vector in the direction of ball motion
        ball_vector = [self.dx/math.sqrt(self.dx**2+self.dy**2), self.dy/math.sqrt(self.dx**2+self.dy**2)]
        #self.canvas.create_line(200,200,200+ball_vector[0]*50,200+ball_vector[1]*50,fill="red")
        dot_prod = alignment_vector[0]*ball_vector[0]+alignment_vector[1]*ball_vector[1]
        alignment_vector_magnitude = math.sqrt(alignment_vector[0]**2+alignment_vector[1]**2)
        ball_vector_magnitude = math.sqrt(ball_vector[0]**2+ball_vector[1]**2)
        vector_angle = self.rad_to_deg(math.acos(dot_prod/(alignment_vector_magnitude*ball_vector_magnitude)))
        print vector_angle
        if vector_angle > 90:
            vector_angle = abs(vector_angle-180)
        print "corrected angle = "+str(vector_angle)
        """
        ball_mass = 20
        player_mass = 20

        collision_dist = math.sqrt((self.player.center[0] - self.ball_center[0])**2+
                                   (self.player.center[1] - self.ball_center[1])**2)

        #correct ball position if it overlaps with player
        if collision_dist < self.player_size+self.ball_size:
            #print "collision dist = "+str(collision_dist)
            #print "correct dist = "+str(self.player_size+self.ball_size)
            vector_multiplier = collision_dist/float(self.player_size+self.ball_size)
            #print "vector multiplier = "+str(vector_multiplier)
            if self.ball_center[1] > self.player.center[1]:
                #upper left quadrant
                if self.ball_center[0] < self.player.center[0]:
                    """
                    print "upper left"
                    print "ball center x = "+str(self.ball_center[0])
                    print "ball center x = "+str(self.ball_center[1])
                    """
                    self.ball_center[0] -= vector_multiplier * abs(self.player.center[0] - self.ball_center[0])
                    self.ball_center[1] -= vector_multiplier * abs(self.player.center[1] - self.ball_center[1])
                    """
                    print self.ball_center[0]
                    print self.ball_center[1]
                    """
                #lower left quadrant
                else:
                    """
                    print "lower right"
                    print "ball center x = "+str(self.ball_center[0])
                    print "ball center x = "+str(self.ball_center[1])
                    """
                    self.ball_center[0] -= vector_multiplier * abs(self.player.center[0] - self.ball_center[0])
                    self.ball_center[1] += vector_multiplier * abs(self.player.center[1] - self.ball_center[1])
                    """
                    print self.ball_center[0]
                    print self.ball_center[1]
            print "final collision distance = "+str(math.sqrt((self.player.center[0] - self.ball_center[0])**2+
                                   (self.player.center[1] - self.ball_center[1])**2))
            print "correct collision distance = "+str(self.player_size+self.ball_size)
            """
        print self.dx
        print self.dy
        print "end start"
        collision_dist = math.sqrt((self.player.center[0] - self.ball_center[0])**2+
                                   (self.player.center[1] - self.ball_center[1])**2)
        n_x = (self.player.center[0] - self.ball_center[0]) / float(collision_dist)
        n_y = (self.player.center[1] - self.ball_center[1]) / float(collision_dist)
        p = 2 * (self.dx * n_x + self.dy * n_y) / (ball_mass + player_mass)
        #print self.dx
        #print self.dy
        self.dx = self.dx - p * ball_mass * n_x - p * player_mass * n_x
        self.dy = self.dy - p * ball_mass * n_y - p * player_mass * n_y
        #print self.dx
        #print self.dy

        #set player dy to zero
        self.player.player_dy = 0
        print "ball vx = "+str(self.dx)
        print "ball vy = "+str(self.dy)
        print "ball velocity = "+str(math.sqrt(self.dx**2+self.dy**2))

    def opponentHitsBall(self):
        """
        initial_alignment_vector = [self.ball_center[0]-self.player.center[0], self.ball_center[1]-self.player.center[1]]
        #unit vector in direction of line between ball centers
        alignment_vector = [initial_alignment_vector[0]/math.sqrt(initial_alignment_vector[0]**2+initial_alignment_vector[1]**2),
                            initial_alignment_vector[1]/math.sqrt(initial_alignment_vector[0]**2+initial_alignment_vector[1]**2)]
        #self.canvas.create_line(200,200,200+alignment_vector[0]*50,200+alignment_vector[1]*50,fill="white")
        #unit vector in the direction of ball motion
        ball_vector = [self.dx/math.sqrt(self.dx**2+self.dy**2), self.dy/math.sqrt(self.dx**2+self.dy**2)]
        #self.canvas.create_line(200,200,200+ball_vector[0]*50,200+ball_vector[1]*50,fill="red")
        dot_prod = alignment_vector[0]*ball_vector[0]+alignment_vector[1]*ball_vector[1]
        alignment_vector_magnitude = math.sqrt(alignment_vector[0]**2+alignment_vector[1]**2)
        ball_vector_magnitude = math.sqrt(ball_vector[0]**2+ball_vector[1]**2)
        vector_angle = self.rad_to_deg(math.acos(dot_prod/(alignment_vector_magnitude*ball_vector_magnitude)))
        print vector_angle
        if vector_angle > 90:
            vector_angle = abs(vector_angle-180)
        print "corrected angle = "+str(vector_angle)
        """
        ball_mass = 20
        player_mass = 20

        collision_dist = math.sqrt((self.opponent.center[0] - self.ball_center[0])**2+
                                   (self.opponent.center[1] - self.ball_center[1])**2)

        #correct ball position if it overlaps with player
        if collision_dist < self.player_size+self.ball_size:
            #print "collision dist = "+str(collision_dist)
            #print "correct dist = "+str(self.player_size+self.ball_size)
            vector_multiplier = collision_dist/float(self.player_size+self.ball_size)
            #print "vector multiplier = "+str(vector_multiplier)
            if self.ball_center[1] > self.opponent.center[1]:
                #upper left quadrant
                if self.ball_center[0] < self.opponent.center[0]:
                    """
                    print "upper left"
                    print "ball center x = "+str(self.ball_center[0])
                    print "ball center x = "+str(self.ball_center[1])
                    """
                    self.ball_center[0] -= vector_multiplier * abs(self.opponent.center[0] - self.ball_center[0])
                    self.ball_center[1] -= vector_multiplier * abs(self.opponent.center[1] - self.ball_center[1])
                    """
                    print self.ball_center[0]
                    print self.ball_center[1]
                    """
                #lower left quadrant
                else:
                    """
                    print "lower right"
                    print "ball center x = "+str(self.ball_center[0])
                    print "ball center x = "+str(self.ball_center[1])
                    """
                    self.ball_center[0] -= vector_multiplier * abs(self.opponent.center[0] - self.ball_center[0])
                    self.ball_center[1] += vector_multiplier * abs(self.opponent.center[1] - self.ball_center[1])
                    """
                    print self.ball_center[0]
                    print self.ball_center[1]

            print "final collision distance = "+str(math.sqrt((self.opponent.center[0] - self.ball_center[0])**2+
                                   (self.opponent.center[1] - self.ball_center[1])**2))
            print "correct collision distance = "+str(self.player_size+self.ball_size)
            """

        collision_dist = math.sqrt((self.opponent.center[0] - self.ball_center[0])**2+
                                   (self.opponent.center[1] - self.ball_center[1])**2)
        n_x = (self.opponent.center[0] - self.ball_center[0]) / float(collision_dist)
        n_y = (self.opponent.center[1] - self.ball_center[1]) / float(collision_dist)
        p = 2 * (self.dx * n_x + self.dy * n_y) / (ball_mass + player_mass)
        #print self.dx
        #print self.dy
        self.dx = self.dx - p * ball_mass * n_x - p * player_mass * n_x
        self.dy = self.dy - p * ball_mass * n_y - p * player_mass * n_y
        #print self.dx
        #print self.dy

        #set opponent dy to zero
        print "ball vx = "+str(self.dx)
        print "ball vy = "+str(self.dy)
        print "ball velocity = "+str(math.sqrt(self.dx**2+self.dy**2))


    def deg_to_rad(self, degrees):
        return (degrees/360.0)*2*math.pi

    def rad_to_deg(self, radians):
        return (radians/(2.0*math.pi))*360.0

    def debugWithArt(self):
        self.canvas.coords(self.centers_vector, self.ball_center[0], self.ball_center[1], self.player.center[0], self.player.center[1])
        x_difference = math.fabs(self.ball_center[0]-self.player.center[0])*.5
        line_center_x = 0
        if self.ball_center[0] < self.player.center[0]:
            line_center_x = self.ball_center[0]+x_difference
        else:
            line_center_x = self.player.center[0]+x_difference
        y_difference = math.fabs(self.ball_center[1]-self.player.center[1])*.5
        line_center_y = 0
        if self.ball_center[1] < self.player.center[1]:
            line_center_y = self.ball_center[1]+y_difference
        else:
            line_center_y = self.player.center[1]+y_difference
        self.canvas.coords(self.v_vector,line_center_x, line_center_y, line_center_x+self.dx*-5.0,
                                line_center_y+self.dy*-5.0)
        #FIXME add code to draw output vector once it exists


root = Tk()
root.title("Slime Volleyball")
app = SlimeVolleyball(root)
root.mainloop()
