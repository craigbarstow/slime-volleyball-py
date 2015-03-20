import math

class CollisionHandler:
    def __init__(self, canvas_width, canvas_height, floor_height, net_coordinates, ball_size, player_size):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.floor_height = floor_height
        self.net_left = net_coordinates[0]
        self.net_top = net_coordinates[1]
        self.net_right = net_coordinates[2]
        self.ball_size = ball_size
        self.ball_radius = ball_size*.5
        self.player_radius = player_size*.5
        self.prev_player_collision_distance = 0
        self.prev_opponent_collision_distance = 0

    def ballHitFloor(self, ball_center_y):
        #fixme Ball can escape down net and out through floor
        if ball_center_y > self.canvas_height-self.floor_height-self.ball_radius:
            return True
        else:
            return False

    def checkForCeilingCollision(self, ball_center_y):
        if ball_center_y < self.ball_radius:
            return True
        else:
            return False

    def checkForWallCollision(self, ball_center_x):
        if ball_center_x < self.ball_radius or ball_center_x > self.canvas_width-self.ball_radius:
            return True
        else:
            return False


    def checkForTopNetCollision(self, ball_center, dy):
        #can be done more neatly and succinctly with constant accel equations
        #FIXME perfect this, still a bit off
        distance = math.sqrt((ball_center[0]-self.canvas_width*.5)**2+
                        (ball_center[1]-self.net_top)**2)
        if distance < self.ball_radius and dy > 0:
            return True
        else:
            return False

    def checkForNetSideCollision(self, ball_center):
        #FIXME perfect this, still a bit off
        if ball_center[1] > self.net_top:
            if math.fabs(ball_center[0]-self.canvas_width*.5) < self.ball_radius:
                return True
        else:
            return False

    def checkForPlayerCollision(self, player, ball_center, player_center):
        #FIXME store previous distance between centers, if new distance b/w centers is > old one, assume collision
        #has already happened and return false
        distance = math.sqrt((ball_center[0]-player_center[0])**2+
                        (ball_center[1]-player_center[1])**2)
        if self.distance_decreasing(player, distance) and distance < self.ball_radius+self.player_radius and ball_center > player_center[1]:
            return True
        else:
            return False

    def distance_decreasing(self, player, distance):
        if player:
            if distance < self.prev_player_collision_distance:
                self.prev_player_collision_distance = distance
                return True
            else:
                self.prev_player_collision_distance = distance
                return False
        else:
            if distance < self.prev_opponent_collision_distance:
                self.prev_opponent_collision_distance = distance
                return True
            else:
                self.prev_opponent_collision_distance = distance
                return False

    def checkForPlayerFloorCollision(self, player_center_y):
        if player_center_y > self.canvas_height - self.floor_height:
            return True
        else:
            return False
