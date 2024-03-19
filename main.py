import time
import pygame
from pygame import Rect
from mine_game import MineGameManager, MineMapCell, ResourceType
from synthesize import SynthesizeManager
from game_assets import *
from game_data import UserResource
from sprite import GameSprite

CHILD_SCENE_RECT = (0, 70, 420, 370)

pygame.init()
main_scene = pygame.display.set_mode((420, 500))
font = pygame.font.SysFont('arial', 16)
clock = pygame.time.Clock()

user_resource = UserResource()
mine_game_manager = MineGameManager(CHILD_SCENE_RECT)
synth_manager = SynthesizeManager()

mine_button = GameSprite(button_images[0], Rect(70, 455, 79, 35))
synth_button = GameSprite(button_images[1], Rect(160, 455, 79, 35))
rank_button = GameSprite(button_images[2], Rect(250, 455, 79, 35))

fps = 40

def draw_recource_icons():
    for i in range(len(user_resource.recoures)):
        x = 80 + (i % 3) * 100
        y = 5 + (i // 3) * 30
        main_scene.blit(icon_images[i], (x, y))
    draw_resource_amount()

def draw_resource_amount() -> None:
    for i in range(len(user_resource.recoures)):
        resource = user_resource.recoures[i]
        text = font.render(str(resource), True, (0, 0, 0))
        x = 120 + (i % 3) * 100
        y = 5 + (i // 3) * 35
        main_scene.blit(text, (x, y))

def draw_buttons() -> None:
    main_scene.blit(mine_button.image, mine_button.rect)
    main_scene.blit(synth_button.image, synth_button.rect)
    main_scene.blit(rank_button.image, rank_button.rect)

def process_button_click(posision: tuple) -> None:
    if synth_button.is_clicked(posision):
        print("debug: 80")
        canvas = synth_manager.get_canvas()
        main_scene.blit(canvas, (0, 0))
        pygame.display.update()
        time.sleep(2)

def init_game():
    pass

running = True
while running:
    main_scene.fill((200, 200, 200))
    draw_recource_icons()
    draw_buttons()

    events = pygame.event.get()
    frame = mine_game_manager.process_frame(events)
    main_scene.blit(frame, (CHILD_SCENE_RECT[0], CHILD_SCENE_RECT[1]))

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
