import math

class VirtualRobot:

    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3
    def __init__(self, _p_target, _vmax, _acc, _dec):
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0 # current speed
        self.p = 0 # current position
        self.phase = VirtualRobot.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def set_position_target(self, target):
        self.p_target = target
        self.phase = VirtualRobot.ACCEL

    def evaluate(self, delta_t):
        if self.phase == VirtualRobot.ACCEL:
            self.p = self.p + self.v * delta_t \
                     + self.accel * delta_t * delta_t / 2
            self.v = self.v + self.accel * delta_t
            distance = self.p_target - self.p
            if distance < 0:
                distance = 0
            if self.v >= self.vmax:
                self.v = self.vmax
                self.phase = VirtualRobot.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.v:
                    self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.CRUISE:
            self.p = self.p + self.vmax * delta_t
            distance = self.p_target - self.p
            if distance <= self.decel_distance:
                self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.DECEL:
            self.p = self.p + self.v * delta_t \
                     - self.decel * delta_t * delta_t / 2
            self.v = self.v - self.decel * delta_t
            if self.p >= self.p_target:
                self.v = 0
                self.p = self.p_target
                self.phase = VirtualRobot.TARGET


# ------------------------------------------------------------

class VirtualRobot2D:

    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3
    
    def __init__(self, _vmax, _acc, _dec):
        self.linear_trajectory = VirtualRobot(0, _vmax, _acc, _dec)
        self.phase = None
        self.target_alpha = None

    def set_target(self, starting_coord, target_coord):
        self.starting_coord = starting_coord
        dx = target_coord[0] - starting_coord[0]
        dy = target_coord[1] - starting_coord[1]
        
        self.target_alpha = target_coord[2]
        self.linear_target = math.hypot(dx,dy)
        self.target_heading = math.atan2(dy,dx)

        self.linear_trajectory.set_position_target(self.linear_target)

    def evaluate(self, delta_t):
        self.linear_trajectory.evaluate(delta_t)
        x = self.starting_coord[0] + self.linear_trajectory.p * math.cos(self.target_heading)
        y = self.starting_coord[1] + self.linear_trajectory.p * math.sin(self.target_heading)

        self.phase = self.linear_trajectory.phase

        return (x,y,self.target_alpha)

class Path2DManipulator:

    def __init__(self, _vmax, _acc, _dec, _distance_threshold, _alpha_deg_threshold):
        self.target_got = False
        self.path_active = False
        self.distance_threshold = _distance_threshold
        self.alpha_deg_threshold = _alpha_deg_threshold
        self.path = [ ]
        self.trajectory = VirtualRobot2D(_vmax, _acc, _dec)

    def set_path(self, path):
        self.path = path
        self.target_got = False

    def start(self, start_pos):
        self.current_target = self.path.pop(0)
        self.trajectory.set_target(start_pos, self.current_target)  
        self.path_active = True      

    def _get_trajectory(self, delta_t, pose):
        (x, y, alpha) = self.trajectory.evaluate(delta_t)
        self.x_current = x
        self.y_current = y
        target_distance = math.hypot(pose[0] - self.current_target[0],
                                     pose[1] - self.current_target[1])

        target_alpha = abs(alpha - math.degrees(pose[2]))
        if target_distance < self.distance_threshold and target_alpha < self.alpha_deg_threshold: 
            return None
        return (x, y, alpha)
    
    def evaluate(self, delta_t, pose):
        target = self._get_trajectory(delta_t, pose)
        if target is None:
            if len(self.path) == 0:
                self.target_got = True
                return (None, None, None)
            else:
                self.start( pose )
                return pose
        return target




