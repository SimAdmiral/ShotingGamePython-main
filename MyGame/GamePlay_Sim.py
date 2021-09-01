import sys
import pygame
import time
pygame.init()

mainClock = pygame.time.Clock()
win_x,win_y = 800,400
screen = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption("Kill your enemy")
press = False
output = None

jump_stop = True
jump_count = 100
jump_step = 0

def collider(p):
    global output
    output = None
    for box in boxHolder:
        if (p[0] >= box[0]+box[2] or p[0]+p[2]<=box[0]):
            output = box
        else:
            if (p[1] + p[3] <= box[1] or p[1]>=box[1]+box[3]):
                output = box
            else:
                output=box
                return True
    return False

class Boxex(pygame.Rect):
    def __init__(self, x, y, w, h, color):
        self.color = color
        super().__init__(x, y, w, h)

    def draw_box(self):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.w, self.h))


class Player(pygame.Rect):

    def __init__(self, x, y, w, h, vel):
        # Calling the __init__ method of the parent class
        super().__init__(x, y, w, h)
        self.vel = vel
        self.g = vel
        self.move = 4
        self.collid  = None
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.jump=0


    def gravity_move(self):
        self.y += self.vel
        if collider(player) == True:
            self.collid = True
            self.y = output.y-self.h
            self.vel=self.g
        else:
            self.collid = False
            player.vel*=1.0165
            if self.vel>10:self.vel=10

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            player.x+=self.move
            if collider(player) == True:
                player.x -= self.move

        if keys[pygame.K_LEFT]:
            player.x-=self.move
            if collider(player) == True:
                player.x += self.move

        if keys[pygame.K_DOWN]:
            player.y+=self.move
            if collider(player) == True:
                player.y -= self.move

    def player_jump(self):
        global press, jump_count, jump_stop
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and jump_stop and self.jump<2:
            self.vel = 0
            press=True
            jump_stop=False
            jump_count=10
            self.jump+=1
        else:
            if player.collid == True:
                self.jump=0
        if not keys[pygame.K_SPACE]: jump_stop=True

        if press and jump_count >= -10:
            if (abs(jump_count)>5):
                self.y-=jump_count*1.25
                if jump_count>=0 and collider(player)==True:
                    jump_count=-11
                    self.y = output.y+output.h
            else:
                self.y-=jump_count*1.75
                if jump_count>=0 and collider(player)==True:
                    self.y = output.y+output.h
                    jump_count=-11
            jump_count-=1
        else:
            if player.vel!=5:self.vel=10
            jump_count=10
            press=False


    def draw_Player(self):
        pygame.draw.rect(screen,(255,0,0), (self.x,self.y,self.w, self.h))


map = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,2,0,0,2,2,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
       ]

boxHolder = []
map_w = win_x//len(map[0])
map_h = win_y//len(map)

for index, map_row in enumerate(map):
    for index1, i1 in enumerate(map_row):
        if i1==1:
            box_clone = Boxex(index1*map_w,index*map_h,map_w,map_h, (0,0,0))
            boxHolder.append(box_clone)
        if i1==2:
            box_clone = Boxex(index1*map_w,index*map_h,map_w,map_h, (0,0,255))
            boxHolder.append(box_clone)


def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

def quit_game():
    pygame.quit()
    sys.exit()


player = Player(80,0,32,40,5)

while True:
    quit()

    for i in boxHolder:
        i.draw_box()

    player.player_jump()
    player.gravity_move()
    player.move_player()
    player.draw_Player()

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

