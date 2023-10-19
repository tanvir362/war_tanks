import pygame
from os.path import join


pygame.init()

WIDTH, HEIGHT = 1000, 600
TANK_WIDTH, TANK_HEIGHT = 60, 60
BULLET_SIZE = 10
WHITE = (255, 255, 255)
GRASS_GREEN = (124, 252, 0)
BLACK = (0, 0, 0)
FPS = 60
VEL = 5
VEL_B = 20

def get_dir(angle):
    movement_dir = {0: (1, 0), 90: (0, -1), 180: (-1, 0), -90: (0, 1)}

    return movement_dir.get(angle, (0, 0))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Fight")
pygame.display.set_icon(
    pygame.image.load(join('assets', 'tank_explosion.png'))
)

def normalize_angle(angle):
    angle = angle % 360  # Convert angle to equivalent angle within 360 degrees
    if angle > 180:
        angle -= 360  # Subtract 360 to get the angle within the range of -180 to 180
    return angle

def true_coord(x, y) -> tuple[float]:

    return (x-TANK_HEIGHT/2, y-TANK_HEIGHT/2)


tank1 = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(join('assets', 'tank1.png')), -90),
    (TANK_WIDTH, TANK_HEIGHT)
)
px, py = true_coord(200, 300)
player1 = pygame.Rect(px, py, TANK_WIDTH, TANK_HEIGHT)


tank2 = pygame.transform.scale(
    pygame.transform.rotate(pygame.image.load(join('assets', 'tank2.png')), 90),
    (TANK_WIDTH, TANK_HEIGHT)
)
px, py = true_coord(800, 300)
player2 = pygame.Rect(px, py, TANK_WIDTH, TANK_HEIGHT)

tank1_angle, tank2_angle = 0, 180

def create_bullet(player:pygame.Rect, angle):
    bx, by, = player.x+player.width, player.y+player.height/2-BULLET_SIZE/2

    if angle == 180:
        bx, by = player.x-BULLET_SIZE, player.y+player.height/2-BULLET_SIZE/2

    elif angle == 90:
        bx, by = player.x+player.width/2-BULLET_SIZE/2, player.y-BULLET_SIZE

    elif angle == -90:
        bx, by = player.x+player.width/2-BULLET_SIZE/2, player.y+player.height



    return pygame.Rect(bx, by, BULLET_SIZE, 10)

def draw():
    global tank1
    global tank2

    screen.fill(GRASS_GREEN)

    screen.blit(tank1, (player1.x, player1.y))
    screen.blit(tank2, (player2.x, player2.y))

    for bullet, dir in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

        dx , dy = dir
        bullet.x += dx*VEL_B
        bullet.y += dy*VEL_B

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




bullets = []

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
                    bullets.append(
                        (create_bullet(player1, tank1_angle), get_dir(tank1_angle))
                    )

                if event.key == pygame.K_SLASH:
                    bullets.append(
                        (create_bullet(player2, tank2_angle), get_dir(tank2_angle))
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