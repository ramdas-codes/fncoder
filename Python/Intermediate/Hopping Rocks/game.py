import math
import pygame
import sys
import time

pygame.init()

size = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
speed = [0, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

GLOWING = [pygame.image.load("assets/rock.png")]

floor_img = pygame.image.load("floor.png")
floor_img = pygame.transform.scale(floor_img, (SCREEN_WIDTH, 400))

sky_img = pygame.image.load("assets/sky.png")
sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

grass_img = pygame.image.load("assets/grass.png")
grass_img = pygame.transform.scale(grass_img, (32, 32))
grass_mid_img = pygame.image.load("assets/grass-mid.png")
grass_mid_img = pygame.transform.scale(grass_mid_img, (32, 32))

milestone_1 = pygame.image.load("assets/20.png")
milestone_1 = pygame.transform.scale(milestone_1, (100, 83))

# milestone_1 = pygame.transform.scale(milestone_1, (32, 32))
milestone_2 = pygame.image.load("assets/50.png")
milestone_2 = pygame.transform.scale(milestone_2, (100, 83))

milestone_3 = pygame.image.load("assets/-15.png")
milestone_3 = pygame.transform.scale(milestone_3, (100, 83))

milestone_4 = pygame.image.load("assets/100.png").convert_alpha()
milestone_4 = pygame.transform.scale(milestone_4, (100, 83))

ice_img = pygame.image.load("assets/ice.png")
# ice_img = pygame.transform.scale(grass_mid_img, (1, 32))

field = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

for i in range(0, 1300, 32):
    field.blit(grass_img, (i, 0))
for j in range(1, 6):
    for i in range(0, 1300, 32):
        field.blit(grass_mid_img, (i, j * 32))

GROUND_HEIGHT = 500


class Player:
    global gravity

    def __init__(self, x_pos, y_pos, width, height):
        self.x = x_pos
        self.y = y_pos
        self.center_x = self.x + (width / 2)
        self.center_y = self.y + (height / 2)
        self.width = width
        self.height = height
        self.glow_img = GLOWING

        self.image = self.glow_img[0]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        self.player_rect.width = self.width
        self.player_rect.height = self.height

    def update(self):
        index = int((clock.tick() - start_frame) * 5 % len(self.glow_img))
        self.image = self.glow_img[index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.player_rect = self.image.get_rect()
        self.player_rect.x = self.x
        self.player_rect.y = self.y

        self.center_x = self.x + (self.width / 2)
        self.center_y = self.y - (self.height / 2)
        # if self.Y_POS < GROUND_HEIGHT:
        #     self.X_POS += self.throw_distance
        #     self.Y_POS += gravity * self.mass * 2
        #     self.Y_POS = min(self.Y_POS, GROUND_HEIGHT)
        #     # self.throw_distance -= 0.1
        #     if self.throw_power <= 0.0:
        #         self.throw_power = 0.0
        #         # self.throw_distance = 0.0
        #
        # if self.throw_power > 0:
        #     self.Y_POS -= self.throw_power * 4
        #     self.X_POS += self.throw_distance * 2
        #     self.throw_power -= 0.2

    def draw(self, scr):
        scr.blit(self.image, (self.player_rect.x, self.player_rect.y))


clock = pygame.time.Clock()
p = Player(30, 500, 40, 40)
shoot = False
start_frame = clock.tick()


def add_score(left, right):
    global available_scores
    global score

    if 600 <= left < 700 or 600 <= right < 700:
        score += available_scores[0]
    elif 800 <= left < 900 or 800 <= right < 900:
        score += available_scores[1]
    elif 1000 <= left < 1100 or 1000 <= right < 1100:
        score += available_scores[2]
    elif 1180 <= left < 1280 or 1180 <= right < 1280:
        score += available_scores[3]


def findAngle(pos, player):
    ang = 0
    try:
        ang = math.atan((player.y - pos[1]) / (player.x - pos[0]))
    except:
        ang = math.pi / 2

    if pos[1] < player.y and pos[0] > player.x:
        ang = abs(ang)
    elif pos[1] < player.y and pos[0] < player.x:
        ang = math.pi - ang
    elif pos[1] > player.y and pos[0] < player.x:
        ang = math.pi + abs(ang)
    elif pos[1] > player.y and pos[0] > player.x:
        ang = (math.pi * 2) - ang

    return ang


def plot_trajectory(start_x, start_y, player_pow, ang, time_done):
    vel_x = math.cos(ang) * player_pow
    vel_y = math.sin(ang) * player_pow

    dist_x = vel_x * time_done
    dist_y = (vel_y * time_done) + ((-4.9 * (time_done ** 2)) / 2)

    new_x = round(dist_x + start_x)
    new_y = round(start_y - dist_y)

    return new_x, new_y


angle = 0
time_passed = 0
power = 0
power_load = False
pos_mouse_click = (-1, -1)
dt = 0
score = 0
POWER_MAX = 10
MAX_TURNS = 5
available_scores = [20, 50, -15, 100]

# [20, 50, -15, 100]
reset_state = False
turns = 0
game_over = False


def reset_game():
    global angle
    global time_passed
    global power
    global power_load
    global pos_mouse_click
    global turns
    global reset_state
    global game_over

    angle = 0
    time_passed = 0
    power = 0
    power_load = False
    pos_mouse_click = (-1, -1)

    reset_state = False
    p.x, p.y = 50, 498

    turns += 1
    if turns >= MAX_TURNS:
        game_over = True


while True:
    dt = clock.tick(60)
    speed = 1 / float(dt)
    screen.fill((5, 0, 5))

    screen.blit(sky_img, (0, 0))

    screen.blit(milestone_1, (600, 460))

    screen.blit(milestone_2, (800, 460))
    screen.blit(milestone_3, (1000, 460))
    screen.blit(milestone_4, (1180, 460))

    screen.blit(field, (0, 540))
    screen.blit(ice_img, (600, 540))
    screen.blit(ice_img, (800, 540))
    screen.blit(ice_img, (1000, 540))
    screen.blit(ice_img, (1180, 540))
    if game_over:
        game_over_font = pygame.font.SysFont("Arial", 30)
        game_over_lbl = game_over_font.render("Game Over. You scored: " + str(score), True, (255, 255, 255))
        press_any_lbl = game_over_font.render("Press any key to continue.", True, (255, 255, 255))
        game_over_rect = game_over_lbl.get_rect()
        press_any_rect = press_any_lbl.get_rect()
        game_over_rect.center = (SCREEN_WIDTH / 2, 300)
        press_any_rect.center = (SCREEN_WIDTH / 2, 330)
        screen.blit(game_over_lbl, game_over_rect)
        screen.blit(press_any_lbl, press_any_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                turns = 0
                score = 0
                game_over = False
    else:
        line = [(p.center_x, p.center_y), pygame.mouse.get_pos()]

        if shoot:
            if p.y <= 500:
                time_passed += 0.7 * speed
                po = plot_trajectory(p.x, p.y, power, angle, time_passed)
                p.x = po[0]
                p.y = po[1]
            else:
                power = 0
                time_passed = 0
                shoot = False
                p.y = 497
                reset_state = True
                add_score(p.x, p.x + p.width)

        if power_load:
            power += 3 * speed
            power = min(power, POWER_MAX)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         print("-----")
            #         print(p.x)
            #         print(p.x + p.width)
            #         print("-----")
            #         add_score(p.x, p.x + p.width)

            if reset_state and event.type == pygame.KEYDOWN:
                reset_game()
                continue

            if reset_state:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not power_load:
                    pos_mouse_click = pygame.mouse.get_pos()
                power_load = True

            if event.type == pygame.MOUSEBUTTONUP:
                power_load = False
                if not shoot:
                    x = p.x
                    y = p.y
                    mouse_position = pygame.mouse.get_pos()
                    shoot = True
                    # power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][1]) ** 2) / 8
                    angle = findAngle(mouse_position, p)

        # screen.fill((5, 0, 5))
        if power_load or shoot:
            pygame.draw.circle(screen, (0, 100, 0), pos_mouse_click, 10)

        p.update()
        p.draw(screen)
        # screen.blit(floor_img, (0, 341))

        # # Display Info
        score_text = pygame.font.SysFont("Arial", 30)
        score_text_lbl = score_text.render("Score: " + str(score), True, (255, 255, 255))
        score_text_rect = score_text_lbl.get_rect()
        score_text_rect.center = (700, 50)
        screen.blit(score_text_lbl, score_text_rect)

        # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(600, 555, 100, 80))
        #
        # pygame.draw.rect(screen, (150, 0, 0), pygame.Rect(800, 555, 100, 80))
        #
        # pygame.draw.rect(screen, (100, 50, 0), pygame.Rect(1000, 555, 100, 80))
        #
        # pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(1180, 555, 100, 80))
        #
        # score_1 = pygame.font.SysFont("Arial", 64)
        # score_1_lbl = score_1.render(str(available_scores[0]), True, (255, 255, 255))
        # score_1_rect = score_1_lbl.get_rect()
        # score_1_rect.center = (652, 590)
        # screen.blit(score_1_lbl, score_1_rect)
        #
        # score_2 = pygame.font.SysFont("Arial", 64)
        # score_2_lbl = score_2.render(str(available_scores[1]), True, (255, 255, 255))
        # score_2_rect = score_2_lbl.get_rect()
        # score_2_rect.center = (852, 590)
        # screen.blit(score_2_lbl, score_2_rect)
        #
        # score_3 = pygame.font.SysFont("Arial", 64)
        # score_3_lbl = score_3.render(str(available_scores[2]), True, (255, 255, 255))
        # score_3_rect = score_3_lbl.get_rect()
        # score_3_rect.center = (1052, 590)
        # screen.blit(score_3_lbl, score_3_rect)
        #
        # score_4 = pygame.font.SysFont("Arial", 64)
        # score_4_lbl = score_4.render(str(available_scores[3]), True, (255, 255, 255))
        # score_4_rect = score_4_lbl.get_rect()
        # score_4_rect.center = (1232, 590)
        # screen.blit(score_4_lbl, score_4_rect)

        power_level_percent = (power / POWER_MAX)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(160, 38, 300 * power_level_percent, 30))
        for i in range(4):
            pygame.draw.rect(screen, (255, 255, 255), (160 - i, 38 - i, 300, 30), 1)

        # Display Info
        power_level = pygame.font.SysFont("Arial", 30)

        text = power_level.render("Power Level: ",
                                  True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (83, 50)
        screen.blit(text, text_rect)

        turns_left_font = pygame.font.SysFont("Arial", 30)
        turns_left_lbl = turns_left_font.render(str(MAX_TURNS - turns) + " turn(s) left", True, (255, 255, 255))
        turns_left_rect = turns_left_lbl.get_rect()
        turns_left_rect.center = (1000, 50)
        screen.blit(turns_left_lbl, turns_left_rect)

    # text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
    # text_rect = text.get_rect()
    # text_rect.center = (900, 490)
    # screen.blit(text, text_rect)
    pygame.display.flip()
