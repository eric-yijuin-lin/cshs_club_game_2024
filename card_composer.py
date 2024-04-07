from pygame import Surface, Rect, font
from pygame.font import Font
from game_assets import card_teamplates, card_images, icon_images, coin_image
from game_data import CardType, Card
from sprite import GameSprite

CARD_WIDTH = 265
CARD_HEIGHT = 370
GLOBAL_MARGIN = 3
CARD_RECTS = {
    "resource": {
        "name": Rect(45, 18, 180, 25),
        "image": Rect(30, 55, 205, 130),
        "description": Rect(30, 220, 195, 85),
        "resource_icon": Rect(15, 330, 30, 25),
        "resource_amount": Rect(70, 325, 50, 28),
        "coin_icon": Rect(218, 330, 30, 25),
        "coin_amount": Rect(145, 325, 50, 28),
    },
    "item": {
        "name": Rect(36, 12, 188, 25),
        "image": Rect(25, 55, 215, 145),
        "description": Rect(20, 250, 200, 85),
        "coin_icon": Rect(5, 342, 25, 25),
        "coin_amount": Rect(30, 350, 70, 17),
    }
}

font.init()
large_font = Font('./msjh.ttf', 18)
medium_font = Font('./msjh.ttf', 14)
small_font = Font('./msjh.ttf', 12)
# large_font.bold = True
# medium_font.bold = True

def get_template(card: Card) -> Surface:
    template: Surface = None
    if card.type == CardType.Item:
        level_key = "lv_" + str(card.level)
        template = card_teamplates["item"][level_key]
    else:
        if card.type == CardType.Stone:
            template = card_teamplates["resource"]["stone"]
        elif card.type == CardType.Water:
            template = card_teamplates["resource"]["water"]
        elif card.type == CardType.Wood:
            template = card_teamplates["resource"]["wood"]
        elif card.type == CardType.Food:
            template = card_teamplates["resource"]["food"]
        elif card.type == CardType.Metal:
            template = card_teamplates["resource"]["metal"]
        elif card.type == CardType.Jewel:
            template = card_teamplates["resource"]["jewel"]
        else:
            raise ValueError("failed to get card template: unsupported card type")
        surface = Surface(template.get_size())
        surface.blit(template, (0, 0))
        return surface
    
def get_surface_rect(card_type: CardType, region_key: str) -> Rect:
    if card_type == CardType.Item:
        rects = CARD_RECTS["item"]
    else:
        rects = CARD_RECTS["resource"]
    return rects[region_key]
    
def select_font(rect: Rect, text: str, max_line: int) -> Font:
    if is_rect_fit_text(large_font, text, rect, max_line):
        return large_font
    if is_rect_fit_text(medium_font, text, rect, max_line):
        return medium_font
    return small_font

def is_rect_fit_text(font: Font, text: str, rect: Rect, max_line: int) -> bool:
    rect_widt = rect[2]
    rect_height = rect[3]
    font_width = font.size(text)[0]
    font_height = font.size(text)[1]
    return font_width < rect_widt * max_line and font_height < rect_height * max_line

def get_folded_text_lines(font: Font, text: str, rect_width: int) -> list[str]:
    text_lines = []
    temp_line = ""
    temp_width = 0
    for c in text:
        temp_line += c
        temp_width += font.size(c)[0]
        if temp_width > rect_width:
            text_lines.append(temp_line)
            temp_line = ""
            temp_width = 0
    text_lines.append(temp_line)
    return text_lines

def render_text(font: Font, text: str, rect: Rect, canvas: Surface, align_center:bool = True) -> None:
    text_lines = get_folded_text_lines(font, text, rect[2])
    line_height = font.size(text)[1] + GLOBAL_MARGIN
    for i in range(len(text_lines)):
        line = text_lines[i]
        line_surface = font.render(line, True, (0, 0, 0))
        x = get_x_after_align(line_surface, rect, align_center)
        y = rect[1] + i * line_height
        canvas.blit(line_surface, (x, y))

def get_x_after_align(text_surface: Surface, rect: Rect, align_center: bool) -> int:
    if not align_center:
        return rect[0] + GLOBAL_MARGIN
    if text_surface.get_size()[0] >= rect[2]:
        return rect[0] + GLOBAL_MARGIN
    return rect.center[0] - text_surface.get_width() // 2

def get_y_after_align(text_surface: Surface, rect: Rect, align_center: bool) -> int:
    if not align_center:
        return rect[1] + GLOBAL_MARGIN
    if text_surface.get_size()[1] >= rect[3]:
        return rect[1] + GLOBAL_MARGIN
    return rect.center[1] - text_surface.get_height() // 2

def render_name(card: Card, canvas: Surface) -> GameSprite:
    rect = get_surface_rect(card.type, "name")
    font = select_font(rect, card.name, 1)
    text_surface = render_text(font, card.name, rect, canvas)
    return GameSprite(text_surface, rect)

def render_description(card: Card, canvas: Surface) -> GameSprite:
    rect = get_surface_rect(card.type, "description")
    font = select_font(rect, card.description, 3)
    text_surface = render_text(font, card.description, rect, canvas)
    return GameSprite(text_surface, rect)

def get_image_sprite(card: Card, align_center = True) -> GameSprite:
    place_rect = get_surface_rect(card.type, "image")
    if card.id in card_images:
        image = card_images[card.id]
    else:
        image = card_images["secret"]
    sprite =  GameSprite(image, place_rect)
    if not align_center:
        return sprite
    sprite.rect = Rect(
        get_x_after_align(image, place_rect, True),
        get_y_after_align(image, place_rect, True),
        image.get_width(),
        image.get_height()
    )
    return sprite

def get_resource_icon_sprite(card: Card) -> GameSprite:
    rect = get_surface_rect(card.type, "resource_icon")
    image = icon_images[card.type.value - 1]
    return GameSprite(image, rect)

def render_resource_amount(card: Card, canvas: Surface) -> GameSprite:
    rect = get_surface_rect(card.type, "resource_amount")
    amount_text = str(card.resource_amount)
    font = select_font(rect, amount_text, 1)
    amount_surface = render_text(font, amount_text, rect, canvas)
    return GameSprite(amount_surface, rect)

def get_coin_icon_sprite(card: Card) -> GameSprite:
    rect = get_surface_rect(card.type, "coin_icon")
    image = coin_image
    return GameSprite(image, rect)

def render_coin_amount(card: Card, canvas: Surface) -> GameSprite:
    rect = get_surface_rect(card.type, "coin_amount")
    amount_text = str(card.sell_coin)
    font = select_font(rect, amount_text, 1)
    amount_surface = render_text(font, amount_text, rect, canvas)
    return GameSprite(amount_surface, rect)

def compose_resource_card(card: Card) -> Surface:
    template = get_template(card)
    image_sprite = get_image_sprite(card)
    resource_icon= get_resource_icon_sprite(card)
    coin_icon = get_coin_icon_sprite(card)
    template.blit(image_sprite.image, image_sprite.rect)
    template.blit(resource_icon.image, resource_icon.rect)
    template.blit(coin_icon.image, coin_icon.rect)
    render_name(card, template)
    render_resource_amount(card, template)
    render_coin_amount(card, template)
    render_description(card, template)
    return template

def compose_item_card(card: Card) -> Surface:
    template = get_template(card)
    image_sprite = get_image_sprite(card)
    coin_icon = get_coin_icon_sprite(card)
    template.blit(image_sprite.image, image_sprite.rect)
    template.blit(coin_icon.image, coin_icon.rect)
    render_name(card, template)
    render_coin_amount(card, template)
    render_description(card, template)
    return template

def compose_card_surface(card: Card) -> Surface:
    if card.type == CardType.Item:
        return compose_item_card(card)
    return compose_resource_card(card)
