import pygame
import time
from MapGenerator import *

pygame.mixer.pre_init(20000, 16, 1, 100)
pygame.init()
# pygame.mixer.init(2000)


def collider(p):
    global output
    output = None
    for box in MapCreator.map_Holder:
        if (p[0] >= box[0]+box[2] or p[0]+p[2]<=box[0]):
            output = box
        else:
            if (p[1] + p[3] <= box[1] or p[1]>=box[1]+box[3]):
                output = box
            else:
                output= box
                return True
    return False


pygame.mixer.set_num_channels(8)
voice = pygame.mixer.Channel(5)

class Player(pygame.Rect):
    player_count = 1
    player_Hodler = []
    def __init__(self, x, y, w, h, vel):
        super().__init__(x, y, w, h)
        self.vel = vel
        self.g = vel
        self.jumpSound = pygame.mixer.Sound("Sounds/JumpSounds/jump1.wav")
        self.jumpSound.set_volume(0.5)

        self.jump=0
        self.move = 4
        self.jump_stop = 0
        self.jump_count = 10
        self.heart_count = 6
        self.t1 = time.time()
        self.t2 = time.time()
        self.player = Player.player_count
        self.isFlip = False

        self.spritesCols = 2
        self.spriteX = 0
        self.isShoting = False
        self.player_shot = False
        self.collid = None
        self.press = False
        self.flipSprite = False
        self.player_stop = False
        self.player_move_left = False
        self.playerIsJumping = False


        self.heart = pygame.image.load("Sprites/Heart.png")
        self.heart_rect = self.heart.get_rect()
        self.playerPath = "Sprites/Player{}/".format(Player.player_count)
        self.spritePath = "Stop"

        self.defaultSprite = pygame.image.load("{}{}.png".format(self.playerPath,self.spritePath)).convert_alpha()
        self.currentSprite = self.defaultSprite

        self.image_col = 32
        self.image_x = 0
        self.player_mask = pygame.mask.from_surface(self.currentSprite)

        Player.player_count+=1
        Player.player_Hodler.append(self)


    def gravity_move(self):
        global output

        self.y += self.vel
        self.playerIsJumping = True
        if collider(self) == True:
            self.playerIsJumping = False
            self.collid = True
            self.y = output.y-self.h
            self.vel=self.g
        else:
            self.collid = False
            self.vel*=1.0165
            if self.vel>10:self.vel=10


    def move_player(self):
        self.player_stop = True

        keys = pygame.key.get_pressed()
        self.spritePath = "Stop"

        if (self.player == 1 and keys[pygame.K_RIGHT]) or (self.player == 2 and keys[pygame.K_d]):
            self.player_move_left = False
            self.player_stop = False
            self.flipSprite = False
            self.spritePath = "Move"

            self.x+=self.move
            self.image_x+=self.image_col
            if self.image_x>self.image_col:
                self.image_x=0

            if collider(self) == True:
                self.x -= self.move

            self.isFlip = False

        if (self.player == 1 and keys[pygame.K_LEFT]) or (self.player == 2 and keys[pygame.K_a]):
            self.player_move_left = True
            self.player_stop = False
            self.spritePath = "Move"

            self.x-=self.move
            self.image_x+=self.image_col

            if self.image_x>self.image_col:
                self.image_x=0

            if collider(self) == True:
                self.x += self.move

            self.isFlip = True


    def player_jump(self):
        keys = pygame.key.get_pressed()

        if ((self.player==2 and keys[pygame.K_w]) or (self.player == 1 and keys[pygame.K_UP])) and self.jump_stop and self.jump<2:

            if voice.get_busy()==0:
                voice.play(self.jumpSound)
            # self.jumpSound.play() #do zatovrky sa dava kolkokrát sa ma prehran sound0

            self.spritePath = "Jump"
            self.vel = 0
            self.press=True
            self.jump_stop=False
            self.jump_count=10

            if not self.collid:
                self.jump+=2
            else:
                self.jump+=1
        else:
            if self.collid == True:
                self.jump=0

        if not keys[pygame.K_UP] and self.player==1: self.jump_stop=True
        if not keys[pygame.K_w] and self.player==2: self.jump_stop = True

        if self.press and self.jump_count >= -10:
            self.playerIsJumping = True
            if (abs(self.jump_count)>5):
                self.y-=self.jump_count*1.1
                if self.jump_count>=0 and collider(self)==True:
                    self.jump_count=-11
                    self.y = output.y+output.h
            else:
                self.y-=self.jump_count*1.1
                if self.jump_count>=0 and collider(self)==True:
                    self.y = output.y+output.h
                    self.jump_count=-11
            self.jump_count-=1
        else:
            if self.vel!=5:self.vel=10
            self.jump_count=10
            self.press=False
            self.playerIsJumping = False


    def draw_Player(self):
        self.t1 = time.time()

        if not self.player_stop:
            self.spritePath = "Move"

        if self.playerIsJumping:
            self.spritePath = "Jump"

        self.currentSprite = pygame.image.load("{}{}.png".format(self.playerPath, self.spritePath)).convert_alpha()

        if self.spriteX > self.currentSprite.get_rect().w-self.image_col:self.spriteX=0

        if self.player_move_left:
            if self.playerPath == "Sprites/Player1/Pistol/":
                pygame.display.get_surface().blit(pygame.transform.flip(self.currentSprite, True, False),(self.x-8, self.y), (self.spriteX, 0, self.image_col, 32))
            else:
                pygame.display.get_surface().blit(pygame.transform.flip(self.currentSprite, True, False), (self.x, self.y), (self.spriteX, 0, self.image_col, 32))
        else:
            pygame.display.get_surface().blit(self.currentSprite, (self.x, self.y), (self.spriteX, 0, self.image_col, 32))

        if self.t2+.25<self.t1:
            self.t2=time.time()
            self.spriteX += self.image_col
            if self.spriteX > self.currentSprite.get_rect().w-self.image_col:self.spriteX=0

        self.draw_Heart()
        # pygame.draw.rect(pygame.display.get_surface(),(255,0,0), (self.x,self.y,self.w, self.h))
        # pygame.display.get_surface().blit(self.playerSprite,(self.x,self.y))

    def draw_Heart(self):

        for i in range(self.heart_count):
            screen = pygame.display.get_surface()
            if self.player == 2:
                screen.blit(self.heart,
                            ((screen.get_rect().w) - 18 - i * (self.heart_rect.w + 2) - self.heart_rect.w, 18),
                            self.heart_rect)
            else:
                screen.blit(self.heart, (18+i*(self.heart_rect.w+2), 18), self.heart_rect)
