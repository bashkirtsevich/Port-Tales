# this file is part of Port Tales
# Copyright (C) 2014
# Yann Asset <shinra@electric-dragons.org>,
# Vincent Michel <vxgmichel@gmail.com>,
# Cyril Savary <cyrilsavary42@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from XY import XY
import pygame as pyg
from pygame import Surface, Rect
from pygame.sprite import DirtySprite, Sprite
from itertools import takewhile, count, cycle, dropwhile
from Common import check_exit, load_image, isfile
import os
from Constants import *


countdown = lambda x: xrange(x-1,-1,-1)

def counter(period, reverse= False, cyclic = False):
    current = period-1 if reverse else 0
    inc = -1 if reverse else +1
    while True:
        arg = yield current
        if arg is not None:
            inc = arg
        current += inc
        if not cyclic and current < 0:
            break
        current %= period
        if not cyclic and not current:
            break
    if reverse:
        yield 0

def animation(folder):
        isnotfile = lambda x: not isfile(x)
        names = (os.path.join(folder, IMG_FORMAT.format(i)) for i in count())
        valid_names = takewhile(isfile , dropwhile(isnotfile, names))
        return [TileView.resize_ressource(name) for name in valid_names]

class TileView(DirtySprite):

    width = SPRITE_WIDTH
    layer_container = None
    nb_lines = 0

    @classmethod
    def resize_ressource(cls, name):
        # Load ressource
        ressource = load_image(name).convert_alpha()
        # Get corresponding size
        factor = float(cls.width)/ressource.get_width()
        size = XY(*ressource.get_size())*(factor,factor)
        size = map(int, size)
        # Keep the window from not repsonding
        check_exit()
        # Scale the ressource
        return pyg.transform.smoothscale(ressource, size)

    def __init__(self, board_pos, layer=0):
        # Init
        super(TileView, self).__init__()
        self.layer_container.add(self, layer=layer)
        self.pos = self.convert(board_pos)
        self.rect = Rect(self.pos, (0, 0))
        self.image = Surface(self.rect.size)
        self.dirty = 2

    def convert(self, pos):
        pos = XY(pos.y-pos.x, pos.x+pos.y)
        factor_y = (self.width)/(2*3**0.5)
        pos *= (self.width)*0.5, factor_y
        pos += self.width*self.nb_lines/2, Y_OFFSET
        return XY(*map(int,pos))

class BlockView(TileView):

    ressource_name = "block.png"
    ressource = TileView.resize_ressource(ressource_name)

    def __init__(self, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(BlockView, self).__init__(self.board_pos, board_id)
        self.image = self.ressource

class HoleView(TileView):

    folder_dict = {0:"black_hole_repos"}
    ressource_dict = {key: animation(name) for key, name in folder_dict.items()}
    len_animation = len(ressource_dict[0])

    def __init__(self, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(HoleView, self).__init__(self.board_pos, board_id)
        self.counter = counter(self.len_animation, cyclic=True)
        self.animation = self.ressource_dict[0]
        self.image = None

    def update(self):
        self.image = self.animation[next(self.counter)]

class FloorView(TileView):

    filename_dict = {0: "floor.png",
                     1: "floor_red.png",
                     2: "floor_green.png",
                     3: "floor_yellow.png"}
    ressource_dict = {key:TileView.resize_ressource(name)
                          for key, name in filename_dict.items()}

    def __init__(self, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(FloorView, self).__init__(self.board_pos, board_id)
        self.image = self.ressource_dict[0]

    def set_color(self, color):
        self.image = self.ressource_dict[color]


class BorderView(TileView):

    ressource_name = "border.png"
    ressource = TileView.resize_ressource(ressource_name)

    def __init__(self, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(BorderView, self).__init__(self.board_pos, board_id)
        self.image = self.ressource


class MovingPlayerView(TileView):

    folder_dict = {}
    ressource_dict = {}
    len_animation = 0

    def __init__(self, board_pos, board_id, direction, delay, callback=None):
        # Init view
        self.board_pos = XY(*board_pos)
        super(MovingPlayerView, self).__init__(self.board_pos, board_id)
        # Init attributes
        self.image = Surface((0,0))
        self.delay = delay
        # Get animation
        if direction in self.ressource_dict:
            self.counter = counter(self.len_animation)
            self.ressource = self.ressource_dict[direction]
        else:
            self.counter = counter(self.len_animation, reverse = True)
            self.ressource = self.ressource_dict[XY(*direction)*(-1,-1)]
        self.animation = (self.ressource[i] for i in self.counter)
        self.callback = callback

    def update(self):
        # Delay control
        if self.delay:
            self.delay -= 1
            return
        # Animation
        self.image = next(self.animation, None)
        if self.image is None:
            if callable(self.callback):
                self.callback()
            self.kill()

class TeleportingPlayerView(MovingPlayerView):

    folder_dict = {(0,1) : "dep_general_se_ne",
                   (-1,0) : "dep_general_sw_nw"}
    ressource_dict = {key: animation(name) for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())

class MinimizingPlayerView(MovingPlayerView):

    folder_dict = {(-1,0) : "red_moving_ne",
                   (0,-1) : "red_moving_nw",
                   (0,1) : "red_moving_se",
                   (1,0) : "red_moving_sw"}
    ressource_dict = {key: animation(name)[3:]
                      for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())

class MaximizingPlayerView(MovingPlayerView):

    folder_dict = {(1,0) : "red_moving_ne",
                   (0,1) : "red_moving_nw",
                   (0,-1) : "red_moving_se",
                   (-1,0) : "red_moving_sw"}
    ressource_dict = {key: animation(name)[:3-1:-1]
                      for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())

class FallingPlayerView(MovingPlayerView):

    folder_dict = {(1,0) : "black_hole_sucking_ne",
                   (0,1) : "black_hole_sucking_nw",
                   (0,-1) : "black_hole_sucking_se",
                   (-1,0) : "black_hole_sucking_sw"}
    ressource_dict = {key: animation(name)[2:-1]
                      for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())




class GoalView(TileView):

    folder_dict = {1 : "goal_red",
                   2 : "goal_green"}

    ressource_dict = {key: animation(name) for key, name in folder_dict.items()}
    len_animation = min(len(x) for x in ressource_dict.values())

    def __init__(self, goal_id, board_pos, board_id):
        self.board_pos = XY(*board_pos)
        super(GoalView, self).__init__(self.board_pos, board_id)
        self.id = goal_id
        self.animation = self.ressource_dict[self.id]
        self.counter = None
        self.image = self.animation[0]
        self.moving = False
        self.deployed = False

    def set_active(self, active):
        if active ^ self.deployed:
            self.moving = True
        self.deployed = active


    def update_image(self):
        if not self.moving:
            return
        elif not self.counter:
            self.counter = counter(self.len_animation, not self.deployed)
            next(self.counter)
        try:
            inc = 1 if self.deployed else - 5
            self.image = self.animation[self.counter.send(inc)]
        except StopIteration:
            self.moving = False
            self.counter = None

    def update(self):
        self.update_image()
        self.rect = self.image.get_rect(topleft=self.convert(self.board_pos))
