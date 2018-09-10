# spring factor : 0.1,  0.01
# damping :       0.18, 0.03

SPRING_FACTOR = 0.1
DAMPING = 0.18
SPREAD_FACTOR = 0.5


class Vertice(object):
    def __init__(self, x, y):
        self.height = 0
        self.velocity = 0
        self.acceleration = 0
        self.x = x
        self.y = y
        self.disp_x = 0
        self.disp_y = 0

    def update(self):
        force = (SPRING_FACTOR * self.height) + (self.velocity * DAMPING)
        self.acceleration = -force
        self.velocity += self.acceleration
        self.height += self.velocity
