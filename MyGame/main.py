import sys
import pygame
import time
import random
from particles import *
from MapGenerator import *
from Player_module import *
from Guns import *
from pygame.locals import *
pygame.init()

mainClock = pygame.time.Clock()
win_x,win_y = 960,480                           #992x480-60X30/880,432-25*15 |16X16-Tiles|      800x400
screen = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption("Kill your enemy")

#----------------------MAP-BULDING--------------
map = []
mapa = open("Maps/Map2.txt")
mapa1 = mapa.readlines()

for i in mapa1:
    map.append(i.split('|'))

for m in map:
    del m[0]
    del m[len(m)-1]

run_map = MapCreator(map, screen)

def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

def quit_game():
    pygame.quit()
    sys.exit()

def particle_creater(n, w):
    for i in range(n):
        particl = Particles(screen,pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], w)

player = Player(32,400,32,32,5)
player1 = Player(900,400,32,32,5)

players = [player, player1]

# pygame.mixer.music.load("Sounds/JumpSounds/jump1.wav")
# pygame.mixer.music.play(-1)

while True:
    quit()

    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    mous = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()

    for i in MapCreator.map_Holder:
        i.draw_box()

    for p in players:
        p.player_jump()
        p.gravity_move()
        p.move_player()
        p.draw_Player()

        chest_collider(p, guns_Chest, spriteChange)
        if (keys[pygame.K_DOWN] and p.player == 1) or (keys[pygame.K_s] and p.player==2):
            chest_collider(p, guns_Chest, SetPlayer)

        if ((keys[pygame.K_m] and p.player==1) or (keys[pygame.K_e] and p.player==2)) and p.player_shot == True and not p.isShoting:
            shot_creator(p.x + 8, p.y+p.h/2 ,p.player_move_left, p.player)
            p.isShoting = True
            shot = pygame.mixer.Sound("Sounds/GunSounds/pistolShot.wav")
            shot.set_volume(.05)
            shot.play()
        else:
            if ((not keys[pygame.K_m] and p.player==1) or (not keys[pygame.K_e] and p.player==2)) and p.isShoting:
                p.isShoting= False



    gunChest_Creator()
    draw_GunInChest()
    shot_draw()

    for i in Particles.particle_Holder:
        # i.particle_gravity_draw(1,[-2,2])
        i.particle_round_draw()

    # press_m = pygame.mouse.get_pressed()
    # if press_m[0]==1 and not m_press:
    #     particle_creater(100,3)
    #     # particle_creater(10,5)
    #     m_press=True
    # if press_m[0]!=1 and m_press:m_press=False

    pygame.display.update()
    pygame.display.flip()
    mainClock.tick(60)
    screen.fill((255,255,255))









def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf",50)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

