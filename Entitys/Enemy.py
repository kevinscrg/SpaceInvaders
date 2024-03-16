class Enemy:
    def __init__(self, health, rank, x, y, velocity, image):
        self.health = health
        self.rank = rank
        self.alive = True
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = image

    def move(self):
        self.x += self.velocity

    def setVelocity(self,vel):
        self.velocity = vel
    def setHealth(self, health):
        self.health = health
    def TakeDamage(self, damage):
        self.health -= damage


