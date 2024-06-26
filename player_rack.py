import pygame


class PlayerRack:
    def __init__(self, bag):
        self.rack = []
        self.bag = bag
        self.tile_width = 40
        self.tile_height = 40
        self.tile_spacing = 5

    def add_tile_to_rack(self, tile):
        if tile.value == 0:
            tile.letter = '_'
        self.rack.append(tile)

    def refill_rack(self):
        while len(self.rack) < 7:
            new_tile = self.bag.take_tile()
            if new_tile:
                self.rack.append(new_tile)
            else:
                break #wychodzi z petli jak bag jest pusty

    def get_tile_at_position(self, position):
        x, y = position
        for tile in self.rack:
            if tile.rect.collidepoint(x, y):
                return tile
        return None

    def remove_tile(self, tile):
        if tile in self.rack:
            self.rack.remove(tile)

    def draw(self, screen):
        rack_width = 850
        rack_height = 200
        rack_margin = 20

        pygame.draw.rect(screen, (240, 255, 240), [0, 600, rack_width, rack_height])

        total_tiles_width = len(self.rack) * self.tile_width
        total_spacing_width = (len(self.rack) - 1) * self.tile_spacing
        total_width = total_tiles_width + total_spacing_width

        x_offset = rack_margin + (560 - total_width) / 2
        y_offset = 670

        for tile in self.rack:
            tile.color = (255, 165, 0)
            tile.rect.topleft = (x_offset, y_offset)
            tile.draw(screen, (x_offset, y_offset))
            x_offset += self.tile_width + self.tile_spacing
