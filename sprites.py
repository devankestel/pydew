import pygame 
from settings import *
from settings import LAYERS 

class Generic(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups, z=LAYERS["main"]):
        
        super().__init__(groups)

        self.image = surf 
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.2, -self.rect.height*0.75)
        self.z = z

class Water(Generic):
    
    def __init__(self, pos, frames, groups, z=LAYERS["main"]):
        
        self.frames = frames
        self.frame_index = 0 

        
        super().__init__(
            pos=pos, 
            surf=self.frames[self.frame_index], 
            groups=groups, 
            z=LAYERS["water"],
        )

    def animate(self, dt):
        
        self.frame_index += 5 * dt 
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):

    def __init__(self, pos, surf, groups, z=LAYERS["main"]):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height*0.9)


class Tree(Generic):

    def __init__(self, pos, surf, groups, name, z=LAYERS["main"]):
        super().__init__(pos, surf, groups, z)
