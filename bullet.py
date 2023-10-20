import pygame

class Bullet:
    SIZE = 10
    VEL = 20
    count = 0

    # angle is in degree between 0 and 180 with sign
    def __init__(self, player:pygame.Rect, angle):
        self.id = Bullet.count
        Bullet.count += 1

        bx, by, = player.x+player.width, player.y+player.height/2-Bullet.SIZE/2

        if angle == 180:
            bx, by = player.x-Bullet.SIZE, player.y+player.height/2-Bullet.SIZE/2

        elif angle == 90:
            bx, by = player.x+player.width/2-Bullet.SIZE/2, player.y-Bullet.SIZE

        elif angle == -90:
            bx, by = player.x+player.width/2-Bullet.SIZE/2, player.y+player.height

        self.rect:pygame.Rect = pygame.Rect(bx, by, Bullet.SIZE, Bullet.SIZE)
        self.dir:tuple = (0, 0)

    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"bullet {self.id}"

    def set_dir(self, dir:tuple):
        self.dir = dir