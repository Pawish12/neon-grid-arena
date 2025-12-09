import pygame
import sys
import random
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- SOUND LOADING ---
def load_sound(path):
    try:
        if os.path.isfile(path):
            return pygame.mixer.Sound(path)
        else:
            print(f"Warning: Sound file not found: {path}")
            return None
    except Exception as e:
        print(f"Warning: Could not load sound '{path}': {e}")
        return None

catch_sound = load_sound("SOUNDE.wav")
special_sound = load_sound("rajini2.wav")  # FIXED WRONG FILENAME

# --- COLORS ---
BG = (10, 10, 25)
GRID = (0, 255, 220)
PLAYER_COLOR = (255, 40, 200)
ORB_COLOR = (60, 255, 140)
WALL_COLOR = (255, 245, 90)

# --- GRID ---
def draw_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)

# --- PLAYER CLASS ---
class Player:
    def __init__(self):     # FIXED
        self.rect = pygame.Rect(WIDTH//2 - 16, HEIGHT//2 - 16, 32, 32)
        self.speed = 7
        self.alive = True

    def move(self, keys):
        if self.alive:
            if keys[pygame.K_LEFT]: self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]: self.rect.x += self.speed
            if keys[pygame.K_UP]: self.rect.y -= self.speed
            if keys[pygame.K_DOWN]: self.rect.y += self.speed

            # border
            self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
            self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect, border_radius=10)

# --- ORB CLASS ---
class Orb:
    def __init__(self):      # FIXED
        self.rect = pygame.Rect(
            random.randint(20, WIDTH - 36),
            random.randint(20, HEIGHT - 36),
            18, 18
        )

    def draw(self):
        pygame.draw.ellipse(screen, ORB_COLOR, self.rect)

# --- WALL CLASS ---
class Wall:
    def __init__(self):      # FIXED
        self.w = random.choice([40, 160])
        self.h = random.choice([40, 160])
        self.t = random.choice(['h', 'v'])

        if self.t == 'h':
            self.rect = pygame.Rect(random.randint(0, WIDTH - self.w), -self.h, self.w, self.h)
            self.dx, self.dy = 0, random.randint(2, 6)
        else:
            self.rect = pygame.Rect(-self.w, random.randint(0, HEIGHT - self.h), self.w, self.h)
            self.dx, self.dy = random.randint(2, 6), 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, WALL_COLOR, self.rect, border_radius=7)

# --- HIGH SCORE ---
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip() or "0")
    except:
        return 0

def save_highscore(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except:
        pass

# --- GAME RESET ---
def reset_game():
    player = Player()
    orbs = [Orb()]
    walls = []
    wall_timer = 0
    score = 0
    return player, orbs, walls, wall_timer, score

player, orbs, walls, wall_timer, score = reset_game()
highscore = load_highscore()
font = pygame.font.SysFont("Consolas", 28)

# --- MAIN LOOP ---
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Restart
    if not player.alive and keys[pygame.K_r]:
        player, orbs, walls, wall_timer, score = reset_game()

    # Player movement
    player.move(keys)

    if player.alive:
        # Orb collection
        for orb in orbs[:]:
            if player.rect.colliderect(orb.rect):
                orbs.remove(orb)
                score += 1
                if catch_sound: catch_sound.play()
                orbs.append(Orb())

        # Spawn walls
        wall_timer += 1
        if wall_timer > 40:
            if len(walls) < 12:
                walls.append(Wall())
            wall_timer = 0

        # Wall update + collision
        for wall in walls[:]:
            wall.update()
            offscreen = (
                wall.rect.right < 0 or wall.rect.left > WIDTH or
                wall.rect.bottom < 0 or wall.rect.top > HEIGHT
            )
            if offscreen:
                walls.remove(wall)
            elif player.rect.colliderect(wall.rect):
                player.alive = False
                if special_sound: special_sound.play()
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)

    # --- DRAW ---
    screen.fill(BG)
    draw_grid()

    for wall in walls:
        wall.draw()
    for orb in orbs:
        orb.draw()
    player.draw()

    score_color = GRID if player.alive else (255, 90, 90)
    score_text = font.render(f"Score: {score}", True, score_color)
    screen.blit(score_text, (16, 8))

    hs_text = font.render(f"High Score: {highscore}", True, (255, 255, 255))
    screen.blit(hs_text, (16, 40))

    if not player.alive:
        tx = font.render("GAME OVER - Press R to Restart", True, (255, 70, 90))
        screen.blit(tx, (WIDTH//2 - tx.get_width()//2,
                         HEIGHT//2 - tx.get_height()//2))

    pygame.display.flip()
    clock.tick(60)
