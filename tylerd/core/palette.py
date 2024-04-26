import numpy as np
from colr import color as colorf

from tylerd.platform.base import PlatformManager


class Palette:
    
    def __init__(self, colors):
        # if len(colors) > 4:
        #     import pdb; pdb.set_trace()
        # try:
        #     assert len(colors) <= 4
        # except:
        #     import pdb; pdb.set_trace()
        self.colors = colors
        self.__weight = 0

    def __hash__(self):
        return hash(self.colors)
    
    def __str__(self):
        return f"Palette(colors={self.colors})"
    
    def __repr__(self):
        platform = PlatformManager()
        colors = []
        for c in self.colors:
            cc = f'{c}: '
            cc += colorf(
                ' ', 
                back=platform.color_code_to_rgb(c), 
                fore=(255,255,255))
            colors.append(cc)

        return f"Palette(colors={', '.join(colors)})"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Palette):
            return self.colors == value.colors
        elif isinstance(value, list):
            return self.colors == value
        elif isinstance(value, tuple):
            return self.colors == value
        return False

    def has(self, colors):
        return all(i in self.colors for i in colors)
    
    def contains(self, colors):
        return [c for c in colors if c in self.colors]

    def not_contains(self, colors):
        return [c for c in colors if c not in self.colors]
    
    @property
    def weight(self):
        return self.__weight
    
    def set_weight(self, weight):
        self.__weight = weight

    def inc_weight(self):
        self.__weight += 1

    @property
    def can_add_color(self):
        return len(self.colors) < 4

    def add_color(self, color):
        if self.can_add_color:
            colors = list(self.colors)
            colors.append(color)
            self.colors = tuple(colors)


