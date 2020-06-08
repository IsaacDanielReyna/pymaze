import pygame
from Vector2 import *

class GameObject:
    def __init__(self, image=None, x=0, y=0):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        size = self.image.get_rect().size
        self.width = size[0]
        self.height = size[1]
        self.speed = 0.2
        self.start_time = 0
        self.delta = 0
        self.surface = pygame.display.get_surface()
        self.previous = Vector2(x, y)
        
    def update(self):
        self.updateDelta()
        self.movement()
        self.blit()

    def blit(self):
        self.surface.blit(self.image, (self.x, self.y))

    def updateDelta(self):
        self.delta = pygame.time.get_ticks() - self.start_time
        self.start_time = pygame.time.get_ticks()

    def movement(self):
        x_axis = 0
        y_axis = 0
        velocity = Vector2(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_axis -= 1
        if keys[pygame.K_RIGHT]:
            x_axis += 1
        if keys[pygame.K_UP]:
            y_axis -= 1
        if keys[pygame.K_DOWN]:
            y_axis += 1

        
        
        # X-AXIS
        if x_axis != 0:
            velocity.x = x_axis * self.speed
        elif velocity.x > 0:
            velocity.x = self.velocity.x - 0.05 * self.delta
            if velocity.x < 0:
                velocity.x = 0
        elif velocity.x < 0:
            velocity.x = velocity.x + 0.05 * self.delta
            if velocity.x > 0:
                velocity.x = 0

        # Y-AXIS
        if y_axis != 0:
            velocity.y = y_axis * self.speed
        elif velocity.y > 0:
            velocity.y = velocity.y - 0.06 * self.delta
            if velocity.y < 0:
                velocity.y = 0
        elif velocity.y < 0:
            velocity.y = velocity.y + 0.06 * self.delta
            if velocity.y > 0:
                velocity.y = 0

        new_position = Vector2(self.x, self.y)
        new_position = new_position.add( velocity.scale( self.delta ) )
        self.x = new_position.x
        self.y = new_position.y

    def checkBounds(self):
        boundary = self.surface.get_size()
        if self.y < 0:
            self.y = 0
        elif self.y > boundary[1] - self.height:
            self.y = boundary[1] - self.height
        if self.x < 0:
            self.x = 0
        elif self.x > boundary[0] - self.width:
            self.x = boundary[0] - self.width

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def collide(self, objects):
        collided = False
        rect = self.getRect();
        for o in objects:
            if rect.colliderect(o.getRect()) == 1:
                collided = True
        if collided == False:
            self.previous = Vector2(self.x, self.y)
        return collided

    def move(self, location):
        self.x = location.x
        self.y = location.y
