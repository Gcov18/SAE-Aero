import math

class Sheet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.I = (self.x**3 * self.y / 12, self.y**3 * self.x / 12)

class Stringer:
    def __init__(self, x, y, z, t) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.t = t
    def cm(self):
        x = (self.x * self.t * (self.x / 2) + (self.y - self.t) * self.t/2 * self.t) / (self.x * self.t + (self.y - self.t) * self.t)
        y = (self.y * self.t * (self.y / 2) + (self.x - self.t) * self.t/2 * self.t) / (self.x * self.t + (self.y - self.t) * self.t)
        return (x, y)
    def I(self):
        Iy = self.x ** 3 *self.t / 12 + self.x * self.t * (self.x/2 -self.cm()[0]) ** 2 + (self.t)**3 * (self.y - self.t)/12 + (self.y - self.t) * self.t * (self.cm()[0] - self.t/2) **2
        Ix = self.y ** 3 *self.t / 12 + self.y * self.t * (self.y/2 -self.cm()[1]) ** 2 + (self.t)**3 * (self.x - self.t)/12 + (self.x - self.t) * self.t * (self.cm()[1] - self.t/2) **2
        return(Ix, Iy)

