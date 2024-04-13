from pygame import Surface, Rect

class GameSprite:
    def __init__(self, image: Surface, rect: Rect) -> None:
        self.image = image
        self.rect = rect

    def is_clicked(self, position: tuple) -> bool:
        return self.rect.collidepoint(position)
    