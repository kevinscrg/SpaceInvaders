class Bullet:
    def __init__(self, x, y, vel, img, type, is_visible = True):
        self.x = x
        self.y = y
        self.vel = vel
        self.image = img
        self.is_visible = is_visible
        self.type = type

    def move(self):
        self.y += self.vel

    def exit_screen_area(self):
        if self.y <= -64 and self.type == 0:
            self.is_visible = False
        elif self.y >= 1000 and self.type == 1:
            self.is_visible = False
