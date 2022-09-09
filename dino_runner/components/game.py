import pygame

from dino_runner.components.text_utils import get_score_element
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstaculomanager import ObstacleManager
from dino_runner.components.power_up.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0

        self.death_count = 0

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()

 
    def run(self):
        # Game loop: events - update - draw
        self.create_comment()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def create_comment(self):
        self.power_up_manager.reset_power_ups(self.points)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score()

        pygame.display.update()
        pygame.display.flip()
        # pygame.mixer.Sound()#.wav

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1

        if self.points % 100 == 0:
            self.game_speed += 1
        score, score_rect = get_score_element(self.points)
        self.player.check_visibility(self.screen)
        self.screen.blit(score, score_rect)