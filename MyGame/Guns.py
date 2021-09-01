import pygame
import random
from particles import *
from MapGenerator import *
from Player_module import *

shot_Holder = []
guns_Chest = []
stopp = False
shot_box_collid = None
map_Holder = MapCreator.map_Holder


def particle_creater(x,y,n, w):
    for i in range(n):
        particl = Particles(pygame.display.get_surface(),x, y, w)


def shot_collider(shot, boxes, offset = 0):
    global shot_box_collid
    for box in boxes:
        if (shot.x >= box.x + box.w or shot.x + shot.w <= box.x):
            shot_box_collid = box
        else:
            if (shot.y + shot.h <= box.y or shot.y >= box.y + box.h):
                shot_box_collid = box
            else:
                shot_box_collid = box
                shot_Holder.remove(shot)
                particle_creater(shot_box_collid.x+offset, shot.y, 100, 3)
                shot_soud()
                return True
    return False


def shot_player_collider(shot, offset = 0):
    global shot_box_collid
    for p in Player.player_Hodler:
        if shot.index!=p.player:
            if (shot.x >= p.x + p.w or shot.x + shot.w <= p.x):
                shot_box_collid = p
            else:
                if (shot.y + shot.h <= p.y or shot.y >= p.y + p.h):
                    shot_box_collid = p
                else:
                    shot_box_collid = p
                    if shot in shot_Holder:
                        shot_Holder.remove(shot)

                    if shot.direstion and p.isFlip:
                        particle_creater(shot_box_collid.x+shot_box_collid.image_col, shot.y, 100, 3)
                    elif shot.direstion:
                        particle_creater(shot_box_collid.x+32, shot.y, 100, 3)
                    else:
                        particle_creater(shot_box_collid.x, shot.y, 100, 3)

                    shot_soud()
                    return True
    return False


def gunChest_Creator():
    global stopp, guns_Chest
    guns_type = ["Revolver", "Bazooka", "Pistol"]
    if len(guns_Chest)<2 and stopp == False:
        value = random.choice(MapCreator.gun_spawner)
        new_value = False
        for i in guns_Chest:
            if i.x==value.x and i.y==value.y:
                new_value = True
                break
        if not new_value:
            gunInChest = Gun_in_Chest(value.x, value.y, random.choice(guns_type))
            guns_Chest.append(gunInChest)


def draw_GunInChest():
    for i in guns_Chest:
        i.draw_Chest()
        if i.open == True:
            i.draw_Gun()


def shot_creator(x,y,direction, index):
    new_Shot = Gun_shot(x,y,direction, index)
    shot_Holder.append(new_Shot)


def shot_draw():
    for shot in shot_Holder:
        shot.draw_GunShot()


def chest_collider(p, holder, action=None):
    for item in holder:
        if (p[0] >= item.Chx + item.Chw or p[0] + p[2] <= item.Chx):
            pass
        else:
            if (p[1] + p[3] <= item.Chy or p[1] >= item.Chy + item.Chh):
                pass
            else:
                if action:
                    action(item, p)
    return False

def spriteChange(item, p):
    item.chest = pygame.image.load("Sprites/Assets/Chests/chest-wood-open.png").convert_alpha()
    item.open = True

def SetPlayer(item, p):
    p.playerPath = "Sprites/Player{}/Pistol/".format(p.player)
    p.image_col = 40
    p.player_shot = True
    p.spriteX = 0
    # item.open = False
    guns_Chest.remove(item)

def shot_soud():
    shot = pygame.mixer.Sound("Sounds/GunSounds/pistolShot.wav")
    shot.set_volume(.02)
    shot.play()




class Gun_in_Chest:
    def __init__(self, x,y, name):
        self.x = x
        self.y = y
        #Chest
        self.Chx = x
        self.Chy = y
        self.chest = pygame.image.load("Sprites/Assets/Chests/chest-wood-close.png").convert_alpha()
        self.Chw = self.chest.get_rect().w
        self.Chh = self.chest.get_rect().h
        self.open = False
        #Gun
        self.Gx = x
        self.Gy = y
        self.gun_name = "{}.png".format(name)
        self.gun_type = pygame.image.load("Sprites/Guns/{}.png".format(name)).convert_alpha()
        self.Gw = self.gun_type.get_rect().w
        self.Gh = self.gun_type.get_rect().h

    def draw_Chest(self):
        pygame.display.get_surface().blit(self.chest, (self.Chx, self.Chy-self.Chh+16), (0, 0, self.Chw, self.Chh))

    def draw_Gun(self):
        pygame.display.get_surface().blit(self.gun_type, (self.Gx, self.Gy - self.Gh+16), (0, 0, self.Gw, self.Gh))


class Gun_shot:

    def __init__(self, x,y, direction, index):
        self.x = x
        self.y = y
        self.direstion = direction
        self.shot_sprite = pygame.image.load("Sprites/Shot/Shot.png")
        self.path = "Sounds/GunSounds/"
        self.w = self.shot_sprite.get_rect().w
        self.h = self.shot_sprite.get_rect().h
        self.index = index

    def draw_GunShot(self):
        global shot_box_collid
        if self.direstion == True:
            self.x -= 15
            if shot_collider(self, map_Holder,16) or shot_player_collider(self):
                self.x+=15

        else:
            self.x += 15
            if shot_collider(self, map_Holder) or shot_player_collider(self):
                self.x-=15


        self.y+=0.15
        if shot_collider(self, map_Holder,16) or shot_player_collider(self):
            self.y -= 0.15

        pygame.display.get_surface().blit(self.shot_sprite, (self.x, self.y), (0, 0, self.w, self.h))