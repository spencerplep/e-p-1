### Here we want the basic cell, space, and attributes for those objects.

import numpy as np




class Material:
    def __init__(self, Sigma, Epsilon, Mu):
        self.Sigma = Sigma
        self.Epsilon = Epsilon
        self.Mu = Mu
        
    def set_attribute(self, key, value):
        self.attributes[key] = value

    def get_attribute(self, key):
        return self.attributes.get(key, None)

class Geometry:
    def __init__(self, shape, position, material=None):
        self.shape = shape
        self.position = position
        self.material = material

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def get_attribute(self, key):
        return self.attributes.get(key, None)

class Field:
    def __init__(self, E, H, D):
        self.E = E
        self.H = H
        self.D = D

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def get_attribute(self, key):
        return self.attributes.get(key, None)