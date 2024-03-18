from enum import Enum
import pygame
from pygame import Surface, Rect
from game_data import ResourceType
from game_assets import sythesize_images

NUM_MATERIAL_ROW = 3
NUM_MATERIAL_COLUMN = 3
NUM_RESOURCE_TYPES = len(ResourceType)
MATERIAL_CELL_WIDTH = 75
MATERIAL_CELL_HEIGHT = 75

class MaterialType(Enum):
    Nothing = 0
    Resource = 1
    Equipment = 2

class SynthesizeMaterial:
    def __init__(self) -> None:
        self.meterial_type = MaterialType.Nothing
        self.resource_type = ResourceType.Nothing
        self.resource_amount = 0
        self.equipment_id = ""
        self.image_index = 0
    
    def set_resource(self, resource_type: ResourceType, amount: int) -> None:
        self.meterial_type = MaterialType.Resource
        self.resource_type = resource_type
        self.resource_amount = amount
        self.equipment_id = ""
        self.set_image_index()

    def set_equipment(self, equipment_id: str) -> None:
        self.meterial_type = MaterialType.Equipment
        self.resource_type = ResourceType.Nothing
        self.resource_amount = 0
        self.equipment_id = equipment_id
        self.set_image_index()

    def set_image_index(self) -> None:
        if self.meterial_type == MaterialType.Resource and self.resource_type != ResourceType.Nothing:
            self.image_index = self.resource_type.value # 0 is empty icon
        elif self.meterial_type == MaterialType.Equipment:
            self.image_index = NUM_RESOURCE_TYPES + 1
        else:
            self.image_index = 0

    def clear(self) -> None:
        self.__init__()

class SynthesizeManager:
    def __init__(self) -> None:
        self.meterial_list = []
        self.init_meterial_list()
        # self.canvas = pygame.display.set_mode((420, 300))
        self.canvas = Surface((420, 300))

    def init_meterial_list(self) -> None:
        for i in range(NUM_MATERIAL_ROW * NUM_MATERIAL_COLUMN):
            self.meterial_list.append(SynthesizeMaterial())

    def get_canvas(self) -> Surface:
        for i in range(len(self.meterial_list)):
            self.blit_meterial_image(i, self.meterial_list[i])
        return self.canvas
        
    def blit_meterial_image(self, list_index: int, meterial: SynthesizeMaterial) -> None:
        image = sythesize_images[meterial.image_index]
        rect = self.get_meterial_rect(list_index)
        self.canvas.blit(image, rect)
    
    def get_meterial_rect(self, index: int) -> Rect:
        return Rect(
            (index % NUM_MATERIAL_COLUMN) * MATERIAL_CELL_WIDTH,
            (index // NUM_MATERIAL_COLUMN) * MATERIAL_CELL_HEIGHT,
            MATERIAL_CELL_WIDTH,
            MATERIAL_CELL_HEIGHT
        )

# screen = pygame.display.set_mode((420, 300))
# manager = SynthesizeManager()
# clock = pygame.time.Clock()
# running = True
# while running:
#     canvas = manager.get_canvas()
#     screen.blit(canvas, (0, 0))
#     ev = pygame.event.get()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     pygame.display.update()
#     clock.tick(40)

# Quit Pygame
pygame.quit()