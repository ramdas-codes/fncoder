import pygame


GLOWING = [pygame.image.load("assets/rock.png")]


class Player:

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
        self.image = self.glow_img[0]
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
