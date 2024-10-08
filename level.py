import pygame 
from settings import * 
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import * 

class Level: 

    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):

        tmx_data = load_pygame("data/map.tmx")
        for layer in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos=(x*TILE_SIZE, y*TILE_SIZE),
                    surf=surf,
                    groups=self.all_sprites,
                    z=LAYERS["house_bottom"],
                )

        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos=(x*TILE_SIZE, y*TILE_SIZE),
                    surf=surf,
                    groups=self.all_sprites,
                    z=LAYERS["main"],
                )

        for x, y, surf in tmx_data.get_layer_by_name("Fence").tiles():
                Generic(
                    pos=(x*TILE_SIZE, y*TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites, self.collision_sprites],
                    z=LAYERS["main"],
                )

        water_frames = import_folder("graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
                Water(
                    pos=(x*TILE_SIZE, y*TILE_SIZE),
                    frames=water_frames,
                    groups=self.all_sprites,
                    z=LAYERS["main"],
                )

        for obj in tmx_data.get_layer_by_name("Trees"):
                Tree(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    groups=[self.all_sprites, self.collision_sprites],
                    name=obj.name,
                    z=LAYERS["main"],
        )

        for obj in tmx_data.get_layer_by_name("Decoration"):
                WildFlower(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    groups=[self.all_sprites, self.collision_sprites],
                    z=LAYERS["main"],
        )
                
        


        # pos tuple (x, y) on screen
        self.player = Player(
            (640, 360),
            self.all_sprites,
            self.collision_sprites,
        )

        Generic(
            pos=(0,0), 
            surf=pygame.image.load("graphics/world/ground.png").convert_alpha(), 
            groups=self.all_sprites,
            z=LAYERS["ground"]
        )

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()

class CameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    
    def custom_draw(self, player):
    # player is a param bc that is what we want the camera (viewport) to follow
    # we want the player always in the center so all other sprites must offset around it
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer_num in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if layer_num == sprite.z:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)