import pygame
from os.path import join

from bullet import Bullet


pygame.init()

WIDTH, HEIGHT = 1000, 600
TANK_WIDTH, TANK_HEIGHT = 60, 60
WHITE = (255, 255, 255)
GRASS_GREEN = (124, 252, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
VEL = 5
DAMAGE_UNIT = 10

def get_dir(angle):
    movement_dir = {0: (1, 0), 90: (0, -1), 180: (-1, 0), -90: (0, 1)}

    return movement_dir.get(angle, (0, 0))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("War of tanks")
pygame.display.set_icon(
    pygame.image.load(join('assets', 'tank_explosion.png'))
)

def normalize_angle(angle):
    angle = angle % 360  # Convert angle to equivalent angle within 360 degrees
    if angle > 180:
        angle -= 360  # Subtract 360 to get the angle within the range of -180 to 180
    return angle


tank1 = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(join('assets', 'tank1.png')), -90),
    (TANK_WIDTH, TANK_HEIGHT)
)
player1 = pygame.Rect(100, 100, TANK_WIDTH, TANK_HEIGHT)


tank2 = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(join('assets', 'tank2.png')), 90),
    (TANK_WIDTH, TANK_HEIGHT)
)
player2 = pygame.Rect(WIDTH-TANK_WIDTH-100, HEIGHT-TANK_HEIGHT-100, TANK_WIDTH, TANK_HEIGHT)

tank1_angle, tank2_angle = 0, 180


def check_in_game_area(unit:pygame.Rect):
    return 0<=unit.x<WIDTH and 0<=unit.y<HEIGHT

def handle_hit(bullet:Bullet):
    global health1
    global health2
    global health_bar1
    global health_bar2


    if bullet.rect.colliderect(player1):
        health1 -= DAMAGE_UNIT
        health_bar1.width = health1
        
        return True
    if bullet.rect.colliderect(player2):
        health2 -= DAMAGE_UNIT
        health_bar2.width = health2
        return True
    
    return False

health1 = 100
health_bar1 = pygame.Rect(10, 10, health1, 10)

health2 = 100
health_bar2 = pygame.Rect(WIDTH-100-10, 10, health2, 10)

def draw():
    global tank1
    global tank2
    global bullets

    screen.fill(GRASS_GREEN)

    screen.blit(tank1, (player1.x, player1.y))
    screen.blit(tank2, (player2.x, player2.y))

    discarded = []
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet.rect)

        dx , dy = bullet.dir
        bullet.rect.x += dx*Bullet.VEL
        bullet.rect.y += dy*Bullet.VEL

        if not check_in_game_area(bullet.rect):
            discarded.append(bullet)

        elif handle_hit(bullet):
            discarded.append(bullet)

    for bullet in discarded:
        bullets.discard(bullet)

    pygame.draw.rect(screen, BLUE, health_bar1)
    pygame.draw.rect(screen, BLUE, health_bar2)

    pygame.display.update()

def handle_tank1_rotation(key):
    global tank1
    global tank1_angle

    if key == pygame.K_a:
        tank1_angle += 90
        tank1_angle = normalize_angle(tank1_angle)
        tank1 = pygame.transform.rotate(tank1, 90)

    if key == pygame.K_d:
        tank1_angle -= 90
        tank1_angle = normalize_angle(tank1_angle)
        tank1 = pygame.transform.rotate(tank1, -90)

def handle_tank2_rotation(key):
    global tank2
    global tank2_angle

    if key == pygame.K_LEFT:
        tank2_angle += 90
        tank2_angle = normalize_angle(tank2_angle)
        tank2 = pygame.transform.rotate(tank2, 90)

    if key == pygame.K_RIGHT:
        tank2_angle -= 90
        tank2_angle = normalize_angle(tank2_angle)
        tank2 = pygame.transform.rotate(tank2, -90)


def move_forward(player, angle):
    dx, dy = get_dir(angle)

    player.x += dx*VEL
    player.y += dy*VEL

def move_backward(player, angle):
    dx, dy = get_dir(angle)

    player.x -= dx*VEL
    player.y -= dy*VEL




bullets = set()

def main():
    global tank1
    global tank2
    global tank1_angle
    global tank2_angle
    global bullets

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    handle_tank1_rotation(event.key)
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    handle_tank2_rotation(event.key)

                if event.key == pygame.K_q:
                    bullet = Bullet(player1, tank1_angle)
                    bullet.set_dir(get_dir(tank1_angle))
                    bullets.add(
                        bullet
                    )

                if event.key == pygame.K_RSHIFT:
                    bullet = Bullet(player2, tank2_angle)
                    bullet.set_dir(get_dir(tank2_angle))
                    bullets.add(
                        bullet
                    )

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            move_forward(player=player1, angle=tank1_angle)

        if key_pressed[pygame.K_s]:
            move_backward(player=player1, angle=tank1_angle)

        if key_pressed[pygame.K_UP]:
            move_forward(player=player2, angle=tank2_angle)

        if key_pressed[pygame.K_DOWN]:
            move_backward(player=player2, angle=tank2_angle)

        draw()
                
        
        

        
            
        
        

    pygame.quit()

        
if __name__ == '__main__':
    main()