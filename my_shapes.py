"""
    Cada forma deve ter uma classe, no entanto essa classe não deve extender shape.
    As classes individuais servirão para definir o número de rotações que cada peça pode 
    dar e para avaliar se um movimento é possível ou não.
"""
from constants import *
from shape import *

class MyShape:

    def __init__(self, shape):
        self.shape = shape

    def get_min_x(self):
        return min([x for x, y in self.shape.positions])

    def get_max_x(self):
        return max([x for x, y in self.shape.positions])