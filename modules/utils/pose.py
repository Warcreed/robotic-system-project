class Pose:

    x_center = 120
    y_center = 700

    def __init__(self, x = 0, y = 0, a = 0):
        self.__x = x
        self.__y = y
        self.__a = a

    def get_pose(self):
        return (self.__x, self.__y, self.__a)

    def get_a(self):
        return self.__a

    def set_pose(self, x, y, a):
        self.__x = x
        self.__y = y
        self.__a = a

    def to_pixel(self):
        return (Pose.x_center + self.__x * 1000, Pose.y_center - self.__y * 1000)

    @classmethod
    def xy_to_pixel(_cls_, x, y):
        return (Pose.x_center + x * 1000, Pose.y_center - y * 1000)

    @classmethod
    def pixel_scale(_cls_, val):
        return val * 1000

