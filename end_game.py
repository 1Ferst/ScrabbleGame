import pygame

class EndGameScreen:
    def __init__(self, screen, player_score):
        self.screen = screen
        self.player_score = player_score
        self.font = pygame.font.Font(None, 110)
        self.running = True

        self.background_image = pygame.image.load('end_game_img.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))  # Dopasowanie obrazka do rozmiaru ekranu

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        game_over_text = self.font.render("Koniec gry", True, (75, 0, 130))
        score_text = self.font.render(f"Twoje punkty: {self.player_score}", True, (75, 0, 130))

        self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)))
        self.screen.blit(score_text, score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)))

        pygame.display.flip()
