from enum import Enum
import pygame
from pygame import Surface, Rect
from game_data import ResourceType, UserResource
from game_assets import sythesize_images
from scene_convert import get_child_scene_position

NUM_MATERIAL_ROW = 3
NUM_MATERIAL_COLUMN = 3
NUM_RESOURCE_TYPES = len(ResourceType)
MATERIAL_CELL_WIDTH = 75
MATERIAL_CELL_HEIGHT = 75

class MaterialType(Enum):
    Nothing = 0
    Resource = 1
    Equipment = 2

class SynthesizeStatus:
    Ready = 1
    SelectMaterial = 2

class MaterialSprite():
    def __init__(self) -> None:
        self.meterial_type = MaterialType.Nothing
        self.resource_type = ResourceType.Nothing
        self.resource_amount = 0
        self.equipment_id = ""
        self.image: Surface = None
        self.rect: Rect = None
        
    def update_sprite(self, synthesize_index: int) -> None:
        self.update_sprite_image()
        self.update_sprite_rect(synthesize_index)

    def update_sprite_image(self) -> None:
        if self.meterial_type == MaterialType.Resource and self.resource_type != ResourceType.Nothing:
            image_index = self.resource_type.value # 0 is empty icon
        elif self.meterial_type == MaterialType.Equipment:
            image_index = NUM_RESOURCE_TYPES + 1 # equipment image start after resources
        else:
            self.image_index = 0
        self.image = sythesize_images[image_index]
    
    def update_sprite_rect(self, index: int) -> None:
        self.rect = Rect(
            10 + (index % NUM_MATERIAL_COLUMN) * MATERIAL_CELL_WIDTH,
            10 + (index // NUM_MATERIAL_COLUMN) * MATERIAL_CELL_HEIGHT,
            MATERIAL_CELL_WIDTH,
            MATERIAL_CELL_HEIGHT
        )
    
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

    def clear(self) -> None:
        self.__init__()

class SynthesizeManager:
    def __init__(self, rect: tuple, user_resources: UserResource) -> None:
        self.meterial_list: list[MaterialSprite] = []
        self.canvas_rect = rect
        self.user_resource = user_resources
        self.canvas = pygame.Surface(
            (self.canvas_rect[2],
             self.canvas_rect[3])
        )
        self.init_meterial_list()
        self.synth_status = SynthesizeStatus.Ready

    def init_meterial_list(self) -> None:
        for i in range(NUM_MATERIAL_ROW * NUM_MATERIAL_COLUMN):
            self.meterial_list.append(MaterialSprite())

    def process_frame(self) -> Surface:
        self.canvas.fill((255, 255, 255))
        for i in range(len(self.meterial_list)):
            self.blit_meterial_image(i, self.meterial_list[i])
        return self.canvas
        
    def blit_meterial_image(self) -> None:
        for m in self.meterial_list:
            self.canvas.blit(m.image, m.rect)

    def process_click(self) -> None:
        main_screen_position = pygame.mouse.get_pos()
        child_scene_position = get_child_scene_position(main_screen_position, self.canvas_rect)

        if self.synth_status == SynthesizeStatus.Ready:
            clicked_material = self.get_clicked_material(child_scene_position)
            if clicked_material:
                self.synth_status = SynthesizeStatus.SelectMaterial

    def process_material_select(self) -> Surface:
        self.canvas.fill((255, 255, 255))
        

    def get_clicked_material(self, position: tuple) -> MaterialSprite:
        for material in self.meterial_list:
            if material.rect.collidepoint(position):
                return material

pygame.quit()