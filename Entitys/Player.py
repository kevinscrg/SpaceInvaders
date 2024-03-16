class Player:
    def __init__(self,health, x, y, velocity, image, score):
        self.health = health
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = image
        self.score = score


    def move(self):
        self.x += self.velocity

    def setVelocity(self,vel):
        self.velocity = vel
    def setScore(self, score):
        self.score = score

    def updateScore(self):
        self.score += 1
    def SetX(self,x):
        self.x = x

    def TakeDamage(self, damage):
        self.health -= damage


