import pygame 
from settings import * 

class Overlay: 

    def __init__(self, player) -> None:
        
        self.display_surface = pygame.display.get_surface()
        self.player = player 

        overlay_path = "graphics/overlay/"
        self.tools_surface = { 
            tool: pygame.image.load(f"{overlay_path}{tool}.png").convert_alpha() for tool in player.tools 
        }
        self.seeds_surface = {
            seed: pygame.image.load(f"{overlay_path}{seed}.png").convert_alpha() for seed in player.seeds
        }

        print(self.tools_surface)
        print(self.seeds_surface)