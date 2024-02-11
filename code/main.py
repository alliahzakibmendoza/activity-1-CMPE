import pygame, sys
from button import Button
from settings import *
from level import Level
from intro import intro
from battle_capacitor import *
from battle_potentiometer import *
from battle_rectifier_diode import *
from battle_resistor import *
from battle_transformer import *
from battle_transistor import *
from battle_voltmeter import *


SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("LEON ECE JOURNEY")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/ngger.ttf", 100)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('LEON ECE JOURNEY')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('#71ddee')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

def play():
        intro()
        battle_voltmeter()
        pygame.quit()
        game = Game()
        game.run()
        pygame.display.update()
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        #main menu buttons
        MENU_TEXT = get_font(100).render("LEON ECE JOURNEY", True, "Black")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))
        shadow1 = get_font(100).render('LEON ECE JOURNEY', True, "#F9A825")
        shadow_rect1 = shadow1.get_rect(center=(644, 204))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                            text_input="PLAY", font=get_font(100), base_color="#F9A825", hovering_color="White")
        shadow2 = get_font(100).render('PLAY', True, "Black")
        shadow_rect2 = shadow2.get_rect(center=(636, 396))


        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
        text_input="QUIT", font=get_font(100), base_color="#F9A825", hovering_color="White")
        shadow3 = get_font(100).render('QUIT', True, "Black")
        shadow_rect3 = shadow3.get_rect(center=(636, 546))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(shadow1, shadow_rect1)
        SCREEN.blit(shadow2, shadow_rect2)
        SCREEN.blit(shadow3, shadow_rect3)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()