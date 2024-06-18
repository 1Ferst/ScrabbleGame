import pygame


class Tile:
    def __init__(self, letter=None, value=None, color=(197, 197, 210), text_color=(0, 0, 0), font_size=32, border_color=(0, 0, 0), modifier=None):
        self.letter = letter
        self.value = value
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.border_color = border_color
        self.modifier = modifier

        self.tile_width = 40
        self.tile_height = 40

        pygame.font.init()
        self.font = pygame.font.Font(None, self.font_size)
        self.value_font = pygame.font.Font(None, 16)

        self.shape = self.create_shape()
        self.rect = self.shape.get_rect()

    def create_shape(self):
        surface = pygame.Surface((self.tile_width, self.tile_height))
        surface.fill(self.color)
        pygame.draw.rect(surface, self.border_color, surface.get_rect(), 1)
        if self.letter:
            text_surface = self.font.render(str(self.letter), True, self.text_color)
            text_rect = text_surface.get_rect(center=surface.get_rect().center)
            surface.blit(text_surface, text_rect)
            if self.value is not None:
                value_surface = self.value_font.render(str(self.value), True, self.text_color)
                value_rect = value_surface.get_rect(bottomright=(self.tile_width - 2, self.tile_height - 2))
                surface.blit(value_surface, value_rect)
        return surface

    def draw(self, screen, pos):
        self.shape = self.create_shape()
        screen.blit(self.shape, pos)


class SpecialTile(Tile):
    def __init__(self, letter=None, value=None, modifier=None, color=(197, 197, 210), text_color=(0, 0, 0), font_size=32, border_color=(0, 0, 0)):
        super().__init__(letter, value, color, text_color, font_size, border_color)
        self.modifier = modifier
        self.modifier_font = pygame.font.Font(None, 30)

    def create_shape(self):
        surface = super().create_shape()
        if self.modifier:
            modifier_surface = self.modifier_font.render(str(self.modifier), True, self.text_color)
            modifier_rect = modifier_surface.get_rect(center=surface.get_rect().center)
            surface.blit(modifier_surface, modifier_rect)
        return surface
