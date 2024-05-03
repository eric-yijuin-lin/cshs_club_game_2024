from enum import Enum
import pygame
from pygame import Rect
from mine_game.manager import MineGameManager
from craft_game.manager import CraftManager
from assets.game_assets import *
from common.inventory import UserInventory
from common.sprite import GameSprite

pygame.init()
class GameScenes(Enum):
    MiningGame = 1
    Craft = 2
    Ranking = 3

CHILD_SCENE_RECT = (0, 70, 420, 370)

pygame.init()
main_scene = pygame.display.set_mode((420, 500))
font = pygame.font.SysFont('arial', 16)
clock = pygame.time.Clock()

user_id = "ae2285392767a655cba42b5a84512560"
user_inventory = UserInventory(user_id)
mine_game_manager = MineGameManager(CHILD_SCENE_RECT, user_inventory)
craft_manager = CraftManager(CHILD_SCENE_RECT, user_inventory)

mine_button = GameSprite(button_images["mining_menu"], Rect(70, 455, 79, 35))
synth_button = GameSprite(button_images["craft_menu"], Rect(160, 455, 79, 35))
rank_button = GameSprite(button_images["rank_menu"], Rect(250, 455, 79, 35))

fps = 40
activated_scene = GameScenes.MiningGame

def draw_recource_icons():
    for i in range(len(user_inventory.resources)):
        x = 65 + (i % 4) * 75
        y = 5 + (i // 4) * 30
        main_scene.blit(icon_images[i], (x, y))
        main_scene.blit(coin_image, (215, 35))
    draw_resource_amount()

def draw_resource_amount() -> None:
    for i in range(len(user_inventory.resources)):
        resource = user_inventory.resources[i]
        text = font.render(str(resource), True, (0, 0, 0))
        x = 105 + (i % 4) * 75
        y = 10 + (i // 4) * 30
        main_scene.blit(text, (x, y))
    text = font.render(str(user_inventory.coins), True, (0, 0, 0))
    main_scene.blit(text, (255, 40))

def draw_buttons() -> None:
    main_scene.blit(mine_button.image, mine_button.rect)
    main_scene.blit(synth_button.image, synth_button.rect)
    main_scene.blit(rank_button.image, rank_button.rect)

def process_button_click(posision: tuple) -> None:
    global activated_scene
    if mine_button.is_clicked(posision):
        craft_manager.hide()
        mine_game_manager.activate()
        activated_scene = GameScenes.MiningGame
    elif synth_button.is_clicked(posision):
        mine_game_manager.hide()
        craft_manager.activate()
        craft_manager.refresh_material_rows()
        activated_scene = GameScenes.Craft
    elif rank_button.is_clicked(posision):
        activated_scene = GameScenes.Ranking

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
            
    if activated_scene == GameScenes.MiningGame:
        frame = mine_game_manager.process_frame(events)
        blit_child_scene(frame)
    elif activated_scene == GameScenes.Craft:
        frame = craft_manager.process_frame(events)
        blit_child_scene(frame)


    pygame.display.update()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
