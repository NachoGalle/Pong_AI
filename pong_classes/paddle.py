import pygame

BLANCO = (255,255,255)

class Paddle:
    WIDTH, HEIGHT = 20 , 100
    VEL = 4
    def __init__(self,x,y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def reset(self):
        self.y = self.original_y
        self.x = self.original_x


    def draw(self,win):
        #pygame.draw.rect(surface=win,color=self.color,rect=(self.x,self.y,self.width,self.height),border_radius=12,width=3)   #activa color
        pygame.draw.rect(surface=win,color=BLANCO,rect=(self.x,self.y,self.WIDTH,self.HEIGHT))

    def move(self,up = True):
        if up:
            self.y-= self.VEL
        else:
            self.y += self.VEL