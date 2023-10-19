import pygame

class Bullet:
    size = 10
    vel = 20
    count = 0

    # angle is in degree between 0 and 180 with sign
    def __init__(self, player:pygame.Rect, angle):
        self.id = Bullet.count
        Bullet.count += 1

        bx, by, = player.x+player.width, player.y+player.height/2-Bullet.size/2

        if angle == 180:
            bx, by = player.x-Bullet.size, player.y+player.height/2-Bullet.size/2

        elif angle == 90:
            bx, by = player.x+player.width/2-Bullet.size/2, player.y-Bullet.size

        elif angle == -90:
            bx, by = player.x+player.width/2-Bullet.size/2, player.y+player.height

        self.rect:pygame.Rect = pygame.Rect(bx, by, Bullet.size, Bullet.size)
        self.dir:tuple = (0, 0)

    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"bullet {self.id}"

    def set_dir(self, dir:tuple):
        self.dir = dir