
class Player1(pygame.Rect):

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
        self.press = False
        self.jump_count = 10
        self.jump_stop = 0
        self.jump=0


    def gravity_move(self):
        self.y += self.vel
        if collider(self) == True:
            self.collid = True
            self.y = output.y-self.h
            self.vel=self.g
        else:
            self.collid = False
            self.vel*=1.0165
            if self.vel>10:self.vel=10

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.x+=self.move
            if collider(self) == True:
                self.x -= self.move

        if keys[pygame.K_LEFT]:
            self.x-=self.move
            if collider(self) == True:
                self.x += self.move

        if keys[pygame.K_DOWN]:
            self.y+=self.move
            if collider(self) == True:
                self.y -= self.move

    def player_jump(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.jump_stop and self.jump<2:
            self.vel = 0
            self.press=True
            self.jump_stop=False
            self.jump_count=10
            self.jump+=1
        else:
            if self.collid == True:
                self.jump=0
        if not keys[pygame.K_SPACE]: self.jump_stop=True

        if self.press and self.jump_count >= -10:
            if (abs(self.jump_count)>5):
                self.y-=self.jump_count*1.25
                if self.jump_count>=0 and collider(self)==True:
                    self.jump_count=-11
                    self.y = output.y+output.h
            else:
                self.y-=self.jump_count*1.75
                if self.jump_count>=0 and collider(self)==True:
                    self.y = output.y+output.h
                    self.jump_count=-11
            self.jump_count-=1
        else:
            if self.vel!=5:self.vel=10
            self.jump_count=10
            self.press=False


    def draw_Player(self):
        pygame.draw.rect(screen,(255,0,0), (self.x,self.y,self.w, self.h))

