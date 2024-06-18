import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font1 = pygame.font.Font(None, 120)
        self.font2 = pygame.font.Font(None, 50)
        self.start_button_rect = pygame.Rect(300, 360, 200, 80)
        self.instructions_button_rect = pygame.Rect(300, 460, 200, 80)
        self.background_image = pygame.image.load('menu_tlo.png')  # Załaduj obraz tła
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))  # Dopasuj obraz do rozmiarów ekranu

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))  # Narysuj obraz tła

        title_text = self.font1.render('Scrabble'.upper(), True, (123, 104, 238))
        title_rect = title_text.get_rect(center=(self.screen.get_width() / 2, 150))
        self.screen.blit(title_text, title_rect)

        pygame.draw.rect(self.screen, (255, 182, 193), self.start_button_rect)
        pygame.draw.rect(self.screen, (255, 182, 193), self.instructions_button_rect)  # Narysuj przycisk instrukcji

        start_text = self.font2.render('Start', True, (255, 255, 255))
        start_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_rect)

        instructions_text = self.font2.render('Instrukcja', True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=self.instructions_button_rect.center)
        self.screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()

    def check_start_button_click(self, pos):
        return self.start_button_rect.collidepoint(pos)

    def check_instructions_button_click(self, pos):
        return self.instructions_button_rect.collidepoint(pos)


class Instructions:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 25)
        self.font_title = pygame.font.Font(None, 50)
        self.background_color = (255, 228, 225)

    def draw_instructions(self):
        self.screen.fill(self.background_color)
        instructions_title_text = self.font_title.render('Instrukcja gry Scrabble', True, (0, 0, 0))
        title_rect = instructions_title_text.get_rect(center=(self.screen.get_width() / 2, 50))
        self.screen.blit(instructions_title_text, title_rect)

        instructions_text = '''                         
1. W czasie tury masz do dyspozycji 7 liter, z których musisz ułożyć poprawne słowo.
2. Słowo zatwierdzasz naciskając ENTER lub przycisk 'Zatwierdź'
   UWAGA! Za niepoprawne słowo dostaniesz ujemne punkty.
3. Jeżeli chcesz usunąć literę z planszy, po prostu na nią kliknij,
   bądź naciśnij przycisk 'Usuń', który usunie wszystkie litery z planszy z danej tury.
   UWAGA! Nie możesz usunąć liter z poprzednich rund.
4. Możesz wymienić wszystkie swoje litery na nowe,
   jednak będzie Cię to kosztowało 20 punktów.
5. Gra zakończy się, jeżeli naciśniesz przycisk 'Zakończ' lub wykorzystasz wszystkie litery.

Naciśnij ESC, aby wrócić do menu.
'''

        y = 120
        for line in instructions_text.splitlines():
            rendered_text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(rendered_text, (20, y))
            y += 40

        pygame.display.flip()
