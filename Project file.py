import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BG = (10, 10, 25)
GRID = (0, 255, 220)
PLAYER = (255, 40, 200)
ORB = (60, 255, 140)
WALL = (255, 245, 90)

# Grid lines
def draw_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID, (x,0), (x,HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID, (0,y), (WIDTH,y), 1)

class Player: 
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2-16, HEIGHT//2-16, 32, 32)
        self.speed = 7
        self.alive = True

    def move(self, keys):
        if self.alive:
            if keys[pygame.K_LEFT]: self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]: self.rect.x += self.speed
            if keys[pygame.K_UP]: self.rect.y -= self.speed
            if keys[pygame.K_DOWN]: self.rect.y += self.speed
            # Boundaries
            self.rect.x = max(0, min(WIDTH-32, self.rect.x))
            self.rect.y = max(0, min(HEIGHT-32, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, PLAYER, self.rect, border_radius=10)

class Orb:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(20, WIDTH-36),
            random.randint(20, HEIGHT-36),
            18, 18
        )

    def draw(self):
        pygame.draw.ellipse(screen, ORB, self.rect)

class Wall:
    def __init__(self):
        self.w = random.choice([40, 160])
        self.h = random.choice([40, 160])
        self.t = random.choice(['h','v'])
        if self.t=='h':
            self.rect = pygame.Rect(random.randint(0,WIDTH-self.w), -self.h, self.w, self.h)
            self.dx, self.dy = 0, random.randint(2,6)
        else:
            self.rect = pygame.Rect(-self.w, random.randint(0,HEIGHT-self.h), self.w, self.h)
            self.dx, self.dy = random.randint(2,6), 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, WALL, self.rect, border_radius=7)

# --- INITIAL GAME STATE ---
player = Player()
orbs = [Orb()]
walls = []
wall_timer = 0
score = 0
font = pygame.font.SysFont("Consolas", 28)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # --- SIMPLE RESTART ---
    if not player.alive and keys[pygame.K_r]:
        player = Player()
        orbs = [Orb()]
        walls = []
        wall_timer = 0
        score = 0

    # --- GAMEPLAY ---
    player.move(keys)
    if player.alive:
        # Orb collection
        for orb in orbs[:]:
            if player.rect.colliderect(orb.rect):
                orbs.remove(orb)
                score += 1
                orbs.append(Orb())

        # Spawn walls
        wall_timer += 1
        if wall_timer > 40:
            if len(walls) < 12:
                walls.append(Wall())
            wall_timer = 0

        # Wall movement + collision
        for wall in walls[:]:
            wall.update()
            if wall.rect.right < 0 or wall.rect.left > WIDTH or wall.rect.bottom < 0 or wall.rect.top > HEIGHT:
                walls.remove(wall)
            elif player.rect.colliderect(wall.rect):
                player.alive = False

    # --- DRAWING ---
    screen.fill(BG)
    draw_grid()

    for wall in walls: wall.draw()
    for orb in orbs: orb.draw()
    player.draw()

    sc = font.render(f"Score: {score}", True, GRID if player.alive else (255,90,90))
    screen.blit(sc, (16, 8))

    if not player.alive:
        tx = font.render("GAME OVER - Press R to Restart", True, (255, 70, 90))
        screen.blit(tx, (WIDTH//2 - 220, HEIGHT//2 - 26))

    pygame.display.flip()
    clock.tick(60)
