import pygame


class Tile:
    def __init__(self, letter=None, value=None, modifier=None, color=(197, 197, 210), text_color=(0, 0, 0), font_size=32, border_color=(0, 0, 0)):
        self.letter = letter
        self.value = value
        self.modifier = modifier
        self.color = color # Kolor prostokąta
        self.text_color = text_color  # Kolor tekstu
        self.font_size = font_size  # Rozmiar czcionki
        self.border_color = border_color

        self.tile_width = 40
        self.tile_height = 40

        # Ustawienia czcionki
        pygame.font.init()
        self.font = pygame.font.Font(None, self.font_size)
        self.modifier_font = pygame.font.Font(None, 30)
        self.value_font = pygame.font.Font(None, 16)

        self.shape = self.create_shape()
        self.rect = self.shape.get_rect()


    def create_shape(self):
        # Prostokąt, który opisuje granice obrazu płytki
        surface = pygame.Surface((self.tile_width, self.tile_height))
        surface.fill(self.color) # Wypełnienie powierzchni kolorem prostokąta
        # Rysowanie obramowania
        pygame.draw.rect(surface, self.border_color, surface.get_rect(), 1)
        if self.letter:
            # Utworzenie tekstu na powierzchni dla litery
            text_surface = self.font.render(str(self.letter), True, self.text_color)
            # Ustawienie pozycji tekstu na środku powierzchni
            text_rect = text_surface.get_rect(center=surface.get_rect().center)
            # Narysowanie tekstu na powierzchni
            surface.blit(text_surface, text_rect)
            if self.value is not None:
                # Utworzenie tekstu na powierzchni dla wartości litery
                value_surface = self.value_font.render(str(self.value), True, self.text_color)
                # Ustawienie pozycji tekstu w prawym dolnym rogu
                value_rect = value_surface.get_rect(bottomright=(self.tile_width - 2, self.tile_height - 2))
                # Narysowanie tekstu na powierzchni
                surface.blit(value_surface, value_rect)
        elif self.modifier:
            # Utworzenie tekstu na powierzchni dla modyfikatora
            modifier_surface = self.modifier_font.render(str(self.modifier), True, self.text_color)
            # Ustawienie pozycji tekstu na środku powierzchni
            modifier_rect = modifier_surface.get_rect(center=surface.get_rect().center)
            # Narysowanie tekstu na powierzchni
            surface.blit(modifier_surface, modifier_rect)
        return surface

    def draw(self, screen, pos):
        # Rysowanie płytki na ekranie w określonej pozycji
        self.shape = self.create_shape()
        screen.blit(self.shape, pos)

