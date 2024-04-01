import time
from enum import Enum
import pygame
from pygame import Rect
from mine_game import MineGameManager
from craft import CraftManager
from game_assets import *
from game_data import UserInventory
from sprite import GameSprite

pygame.init()
class GameStatus(Enum):
    MiningGame = 1
    Synthesize = 2
    Ranking = 3

CHILD_SCENE_RECT = (0, 70, 420, 370)

pygame.init()
main_scene = pygame.display.set_mode((420, 500))
font = pygame.font.SysFont('arial', 16)
clock = pygame.time.Clock()

user_inventory = UserInventory()
mine_game_manager = MineGameManager(CHILD_SCENE_RECT, user_inventory)
synth_manager = CraftManager(CHILD_SCENE_RECT, user_inventory)

mine_button = GameSprite(button_images["mining"], Rect(70, 455, 79, 35))
synth_button = GameSprite(button_images["synthesize"], Rect(160, 455, 79, 35))
rank_button = GameSprite(button_images["ranking"], Rect(250, 455, 79, 35))

fps = 40
game_status = GameStatus.MiningGame

def draw_recource_icons():
    for i in range(len(user_inventory.recoures)):
        x = 80 + (i % 3) * 100
        y = 5 + (i // 3) * 30
        main_scene.blit(icon_images[i], (x, y))
    draw_resource_amount()

def draw_resource_amount() -> None:
    for i in range(len(user_inventory.recoures)):
        resource = user_inventory.recoures[i]
        text = font.render(str(resource), True, (0, 0, 0))
        x = 120 + (i % 3) * 100
        y = 5 + (i // 3) * 35
        main_scene.blit(text, (x, y))

def draw_buttons() -> None:
    main_scene.blit(mine_button.image, mine_button.rect)
    main_scene.blit(synth_button.image, synth_button.rect)
    main_scene.blit(rank_button.image, rank_button.rect)

def process_button_click(posision: tuple) -> None:
    global game_status
    if mine_button.is_clicked(posision):
        game_status = GameStatus.MiningGame
    elif synth_button.is_clicked(posision):
        synth_manager.refresh_material_rows()
        game_status = GameStatus.Synthesize
    elif rank_button.is_clicked(posision):
        game_status = GameStatus.Ranking

def blit_child_scene(scene: pygame.Surface) -> None:
    main_scene.blit(scene, (CHILD_SCENE_RECT[0], CHILD_SCENE_RECT[1]))

def get_child_scene_position(main_scene_position: tuple) -> tuple:
    return (
        main_scene_position[0] - CHILD_SCENE_RECT[0],
        main_scene_position[1] - CHILD_SCENE_RECT[1] 
    )

running = True
while running:
    main_scene.fill((200, 200, 200))
    draw_recource_icons()
    draw_buttons()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            process_button_click(pos)
            
    if game_status == GameStatus.MiningGame:
        frame = mine_game_manager.process_frame(events)
        blit_child_scene(frame)
    elif game_status == GameStatus.Synthesize:
        frame = synth_manager.process_frame(events)
        blit_child_scene(frame)


    pygame.display.update()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
