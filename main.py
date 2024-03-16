import time
import pygame
from mine_game import MineGameManager, MineMapCell, ResourceType
from game_assets import *
from game_data import UserResource

clock = pygame.time.Clock()
fps = 40


pygame.init()
mind_game_canvas = pygame.display.set_mode((420, 550))
font = pygame.font.SysFont('arial', 16)
user_resource = UserResource()
mine_game_manager = MineGameManager()

def draw_recource_icons():
    for i in range(len(user_resource.recoures)):
        x = 80 + (i % 3) * 100
        y = 10 + (i // 3) * 40
        mind_game_canvas.blit(icon_images[i], (x, y))
    draw_resource_amount()

def draw_resource_amount() -> None:
    for i in range(len(user_resource.recoures)):
        resource = user_resource.recoures[i]
        text = font.render(str(resource), True, (0, 0, 0))
        x = 120 + (i % 3) * 100
        y = 20 + (i // 3) * 40
        mind_game_canvas.blit(text, (x, y))

def draw_mine_map(mine_map: list) -> None:
    for tile in mine_map:
        img = tile_images[0] if tile.is_revealed else tile_images[1]
        mind_game_canvas.blit(img, tile.rect)

def reveal_mine_cell(position: tuple) -> MineMapCell:
    for cell in mine_game_manager.mine_map:
        if cell.rect.collidepoint(position):
            cell.is_revealed = True
            mine_game_manager.pickaxe_count -= 1
            # print(cell.rect)
            # print(cell.resource_type)
            # print(cell.recource_level)
            return cell
    return None

def draw_pickaxe(count: int) -> None:
    text = font.render(str(count), True, (0, 0, 0))
    mind_game_canvas.blit(pickaxe_image, (180, 400))
    mind_game_canvas.blit(text, (220, 405))

def draw_card(mine_cell: MineMapCell):
    if mine_cell is None or mine_cell.resource_type == ResourceType.Nothing:
        return
    idx = mine_cell.resource_type.value - 1
    img = card_images[idx]
    mind_game_canvas.blit(img, (80, 80))
    pygame.display.update()
    time.sleep(0.5)

def init_game():
    pass

running = True
while running:
    mind_game_canvas.fill((200, 200, 200))
    ev = pygame.event.get()
    for e in ev:
        if e.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            revealed_cell = reveal_mine_cell(pos)
            draw_card(revealed_cell)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_recource_icons()
    draw_mine_map(mine_game_manager.mine_map)
    draw_pickaxe(mine_game_manager.pickaxe_count)
    pygame.display.update()
    clock.tick(fps)

# Quit Pygame
pygame.quit()
