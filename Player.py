import pygame as pyg
from pygame import Surface
from pygame.sprite import Sprite, RenderUpdates, Group
from Constants import *
from XY import XY
from TileView import TileView
from Tile import Tile
import os
from itertools import takewhile, count, cycle

countdown = lambda x: xrange(x-1,-1,-1)

def counter(period):
    current = period
    while True:
        current -= 1
        current %= period
        yield current


def animation(folder):
        names = (os.path.join(folder, "{:04}.png".format(i)) for i in count(1))
        names = takewhile(os.path.isfile , names)
        return [TileView.resize_ressource(name) for name in names]


class Player(Tile):
    def __init__(self, player_id, pos, mp):
        Tile.__init__(self, *pos)
        self.map = mp
        self.view = PlayerView(player_id, pos, self.map.get_id(pos))
        self.dir = 1,0
        self.id = player_id

    def action(self):
        target = self.map.projection(self.id)[-1]
        self.x = target[0]
        self.y = target[1]
        self.update_view()

    def update_view(self):
        self.view.board_pos = pos = XY(self.x, self.y)
        TileView.layer_container.change_layer(self.view, self.map.get_id(pos))

    def rotate(self, hat):
        self.dir = hat
        self.view.set_animaion(hat)



class PlayerView(TileView):

    folder_dict = {(-1,  0) : "red_player_ne",
                   ( 0,  1) : "red_player_se",
                   ( 0, -1) : "red_player_nw",
                   ( 1,  0): "red_player_sw"}

    ressource_dict = {key: animation(name) for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())
    print(len_animation)

    def __init__(self, player_id, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(PlayerView, self).__init__(self.board_pos, board_id)
        self.dirty = 2
        self.animation = self.ressource_dict[0,1]
        self.counter = counter(self.len_animation)
        self.image = self.animation[next(self.counter)]
        self.id = player_id

    def set_animation(self, hat):
        self.animation = self.ressource_dict[hat]

    def convert(self, pos):
        pos = XY(pos.y-pos.x, pos.x+pos.y)
        factor_y = (self.width-4)/(2*3**0.5)
        pos *= (self.width-4)*0.5, factor_y
        pos += self.width*self.nb_lines/2, 0
        return XY(*map(int,pos))

    def update(self):
        self.image = self.animation[next(self.counter)]
        self.rect = self.image.get_rect(topleft=self.convert(self.board_pos))


