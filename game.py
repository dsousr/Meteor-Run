import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desvie dos Meteoros")
clock = pygame.time.Clock()

# Player
player_img = pygame.image.load("assets/imgs/pixel.png")
player_img = pygame.transform.scale(player_img, (50, 50))
player = pygame.Rect(180, 500, 40, 40)
player_speed = 5

# Obstacles
obstacles = []
meteor_img = pygame.image.load("assets/imgs/meteor.png")
meteor_img = pygame.transform.scale(meteor_img, (60, 60))

# Power Up
star_img = pygame.image.load("assets/imgs/star.png")
star_img = pygame.transform.scale(star_img, (20, 20))
power_up = None
has_shield = False

# Timer
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)
seconds = 0

font = pygame.font.SysFont(None, 40)

def create_obstacle():
    x = random.randint(0, WIDTH - 40)
    return pygame.Rect(x, -40, 40, 40)

def create_powerup():
    x = random.randint(0, WIDTH - 40)
    return pygame.Rect(x, -40, 40, 40)

def draw_text(text, size, y, color=(255, 255, 255)):
    f = pygame.font.SysFont(None, size)
    render = f.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def start_screen():
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        draw_text("DESVIE DOS METEOROS", 36, 120)
        draw_text("Pressione ESPAÇO para jogar", 24, 300)
        draw_text("Pressione ESC para sair", 24, 350)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_over_screen(score):
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        draw_text("GAME OVER", 48, 200, (255, 0, 0))
        draw_text(f"Pontuação: {score}", 30, 280)
        draw_text("Pressione [R] para reiniciar", 24, 360)
        draw_text("Pressione ESC para sair", 24, 400)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_loop():
    global seconds, obstacles, player, power_up, has_shield
    seconds = 0
    obstacles = []
    player = pygame.Rect(180, 500, 40, 40)
    power_up = None
    has_shield = False
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == TIMER_EVENT:
                seconds += 1

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # Random spawn meteor
        if random.randint(1, 30) == 1:
            obstacles.append(create_obstacle())

        # Random spawn power-up
        if power_up is None and not has_shield and random.randint(1, 500) == 1:
            power_up = create_powerup()

        # Update meteors
        for obs in obstacles:
            obs.y += 5
            if obs.colliderect(player):
                if has_shield:
                    has_shield = False
                    obstacles.remove(obs)
                else:
                    running = False
            screen.blit(meteor_img, (obs.x, obs.y))

        obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]

        # Update power-up
        if power_up:
            power_up.y += 4
            screen.blit(star_img, (power_up.x, power_up.y))
            if power_up.colliderect(player):
                has_shield = True
                power_up = None
            elif power_up.y > HEIGHT:
                power_up = None

        # Draw player
        screen.blit(player_img, (player.x, player.y))

        # Draw score
        score_text = font.render(f"Pontuação: {seconds}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Show shield status
        if has_shield:
            shield_text = font.render("Escudo ativado!", True, (0, 255, 0))
            screen.blit(shield_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    game_over_screen(seconds)

while True:
    start_screen()
    game_loop()