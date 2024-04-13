
from pygame import Rect, font
from common.sprite import GameSprite
from assets.game_assets import button_images, coin_image

class ConfirmCraftComponent:
    def __init__(self) -> None:
        self.show = False
        self.cost_font = font.Font('assets/msjh.ttf', 16)
        self.sprites: dict[str, GameSprite] = {}
        self.init_sprites()

    def init_sprites(self) -> None:   
        self.sprites["message_sprite"] = GameSprite(
            self.cost_font.render("發現配方！", True, (0, 0, 0)),
            Rect(50, 330, 150, 40)
        )
        self.sprites["coin_icon_sprite"] = GameSprite(
            coin_image,
            Rect(200, 330, 30, 30)
        )
        self.sprites["cost_amount_sprite"] = GameSprite(
            self.cost_font.render("0", True, (0, 0, 0)),
            Rect(230, 330, 50, 40)
        )
        self.sprites["craft_button_sprite"] = GameSprite(
            button_images["confirm_craft"],
            Rect(300, 330, 30, 30)
        )

    def update_message(self, message: str) -> None:
        self.sprites["message_sprite"].image = self.cost_font.render(message, True, (0, 0, 0))
    
    def update_cost(self, amount: int) -> None:
        self.sprites["cost_amount_sprite"].image = self.cost_font.render(str(amount), True, (0, 0, 0))

    def is_craft_button_clicked(self, child_scene_position: tuple) -> bool:
        if not self.show:
            return False
        return self.sprites["craft_button_sprite"].is_clicked(child_scene_position)
