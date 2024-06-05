import pygame

class Tile:
    def __init__(self, letter, value, color=(255, 255, 255), text_color=(0, 0, 0), font_size=24):
        self.letter = letter
        self.value = value
        self.color = color  # Kolor prostokąta
        self.text_color = text_color  # Kolor tekstu
        self.font_size = font_size  # Rozmiar czcionki

        # Ustawienia czcionki
        self.font = pygame.font.Font(None, self.font_size)

        # Utwórz obraz płytki
        self.image = self.create_image()

        # Prostokąt, który opisuje granice obrazu płytki
        self.rect = self.image.get_rect()

    def create_image(self):
        # Utwórz powierzchnię o wymiarach 40x40 pikseli
        surface = pygame.Surface((40, 40))
        surface.fill(self.color)  # Wypełnij powierzchnię kolorem prostokąta

        # Utwórz tekst na powierzchni
        text_surface = self.font.render(self.letter, True, self.text_color)
        # Ustaw pozycję tekstu na środku powierzchni
        text_rect = text_surface.get_rect(center=surface.get_rect().center)
        # Narysuj tekst na powierzchni
        surface.blit(text_surface, text_rect)

        return surface

    def draw(self, screen, pos):
        screen.blit(self.image, pos)  # Rysowanie płytki na ekranie w określonej pozycji



