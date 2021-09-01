import pygame

class Boxex(pygame.Rect):
    def __init__(self, x, y, w, h, color, screen):
        super().__init__(x, y, w, h)
        self.color = color
        self.screen = screen
        self.image = pygame.image.load("Sprites/RockTile16x16.png").convert_alpha()
        self.image_mask = pygame.mask.from_surface(self.image)
        self.obstacle_rect = self.image.get_rect()
        self.ox = self.x
        self.oy = self.y

    def draw_box(self):
        self.screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.w, self.h))


class MapCreator():
    map_Holder = []
    gun_spawner = []

    def __init__(self, map, screen):
        self.map = map
        self.screen = screen

        map_w = pygame.display.get_surface().get_size()[0] / len(map[0])
        map_h = pygame.display.get_surface().get_size()[1] / len(map)

        for index, map_row in enumerate(map):
            for index1, i1 in enumerate(map_row):

                # try:
                #     if int(i1) == 1:
                #         box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 0), self.screen)
                #         MapCreator.map_Holder.append(box_clone)
                #     if int(i1) == 2:
                #         box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 255), self.screen)
                #         MapCreator.map_Holder.append(box_clone)
                # except:
                #
                #     if str(i1) == "s" or str(i1) == "S":
                #         box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 255), self.screen)
                #         MapCreator.gun_spawner.append(box_clone)

                if int(i1) == 1:
                    box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 0), self.screen)
                    MapCreator.map_Holder.append(box_clone)
                if int(i1) == 2:
                    box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 255), self.screen)
                    MapCreator.map_Holder.append(box_clone)

                if int(i1) == 0:
                    # if map_row[index1-1]==0 and map_row[index1+1]==0 and map[index+1][index1]==1:
                    if int(map[index+1][index1])==1 and int(map[index+1][index1+1])==1 and int(map[index+1][index1-1])==1\
                            and int(map_row[index1+1])==0 and int(map_row[index1+2])==0 \
                            and int(map_row[index1-1])==0 and int(map_row[index1-2])==0:
                        box_clone = Boxex(index1 * map_w, index * map_h, map_w, map_h, (0, 0, 255), self.screen)
                        MapCreator.gun_spawner.append(box_clone)