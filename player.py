import pygame 
from settings import * 
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):

        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        # tuple (width, height)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS["main"]

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.timers = {
            'tool_use': Timer(350, self.use_tool),
            'tool_switch': Timer(200),
            'seed_use': Timer(350, self.use_seed),
            'seed_switch': Timer(200),
        }

        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        self.seeds = ["corn", "tomato"]
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def update_timers(self):
        
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_hoe': [],
            'down_hoe': [],
            'left_hoe': [],
            'right_hoe': [],
            'up_water': [],
            'down_water': [],
            'left_water': [],
            'right_water': [],
            'up_axe': [],
            'down_axe': [],
            'left_axe': [],
            'right_axe': [],
        }

        for animation in self.animations.keys(): 
            full_path = f"graphics/character/{animation}"
            self.animations[animation] = import_folder(full_path)

        print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt 
        
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):

        keys = pygame.key.get_pressed()

        if not self.timers['tool_use'].active:
            # vertical axis
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else: 
                self.direction.y = 0
            
            # horizontal axis
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else: 
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # pygame counts one keypress as many keypresses
            # hence the timer debounce
            if keys[pygame.K_q] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index = 0 if (self.tool_index == len(self.tools) - 1) else self.tool_index + 1
                self.selected_tool = self.tools[self.tool_index]
                print(self.selected_tool)

            if keys[pygame.K_LCTRL]:
                self.timers['seed_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                print("use seed")
            
            if keys[pygame.K_e] and not self.timers["seed_switch"].active:
                self.timers["seed_switch"].activate()
                self.seed_index = 0 if (self.seed_index == len(self.seeds) - 1) else self.seed_index + 1
                self.selected_seed = self.seeds[self.seed_index]
                print(f"{self.selected_seed}")


    def get_status(self):
        
        # If we aren't moving, we are idle
        if self.direction.magnitude() == 0: 
            self.status = f"{self.status.split('_')[0]}_idle"
        
        if self.timers['tool_use'].active:

            self.status = f"{self.status.split('_')[0]}_{self.selected_tool}"

    def move(self, dt):
        
        # adjust speed for diag movement by normalizing vector
        # AKA 1.4X -> 1X
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt): 

        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
