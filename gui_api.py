import pygame

class Button:
    def __init__(self,x,y,width,height,color,onclick,app,sprite=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.app = app
        self.onclick = onclick
        self.sprite = None
        self.half_transparent = pygame.Surface((width,height),pygame.SRCALPHA)
        pygame.draw.rect(self.half_transparent,(255,255,255,100),pygame.Rect(0,0,width,height))
    def update(self):
        if self.sprite == None: pygame.draw.rect(self.app.ui_surface,self.color,self.rect)
        else: self.app.ui_surface.blit(self.sprite,self.rect)
        if pygame.Rect.colliderect(self.rect,pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)):
            self.app.ui_surface.blit(self.half_transparent,self.rect)
            if pygame.mouse.get_pressed()[0]:
                self.onclick(self.app)