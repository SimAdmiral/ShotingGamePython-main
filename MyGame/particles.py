import random
import pygame

class Particles():
    particle_Holder = []
    def __init__(self,screen,x,y,w):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.color = [255,0,0]
        Particles.particle_Holder.append(self)

    def particle_round_draw(self):
        self.color[1]+=random.randint(5,10)
        if self.color[1]<0:self.color= [self.color[0],0,0]
        if self.color[1] > 255: self.color = [self.color[0], 255, 0]

        pygame.draw.circle(self.screen, self.color, (int(self.x),int(self.y)), int(self.w))
        self.x-=random.randint(-2,2)
        self.y-=random.randint(-2,2)
        self.w -=random.uniform(.2,.4)
        if self.w<=0.1:
            Particles.particle_Holder.remove(self)

    def particle_gravity_draw(self, g_x, g_y):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.w))

        self.w -= .1
        if type(g_y)==list:
            self.y+=random.randint(g_y[0],g_y[1])
        else:
            self.y+=g_y

        if type(g_x)==list:
            self.x+=random.randint(g_x[0],g_x[1])
        else:
            self.x+=g_x

        self.color[1]+=random.randint(-5,10)
        if self.color[1]<0:self.color= [self.color[0],0,0]
        if self.color[1] > 255: self.color = [self.color[0], 255, 0]

        if self.w <=0:
            Particles.particle_Holder.remove(self)