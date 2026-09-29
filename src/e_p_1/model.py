### Here we want the basic cell, space, and attributes for those objects.

import numpy as np




class Material:
    def __init__(self, Sigma, Epsilon, Mu):
        self.Sigma = Sigma
        self.Epsilon = Epsilon
        self.Mu = Mu

Metal = Material(Sigma=np.inf, Epsilon=1.0, Mu=1.0)

Boundary = Material(Sigma=0.0, Epsilon=1.0, Mu=1.0)
        

class Object:
    def __init__(self, size, position, material=Metal):
        # only rectangular for now

        self.size = np.array(size)
        self.position = np.array(position)
        self.material = material

        if self.size.shape != self.position.shape:
            raise ValueError("Size and position must have the same number of dimensions.")

    @property
    def bounds(self):
        return self.position, (self.position + self.size)



class Fields:
    def __init__(self, E, D, C):
        self.E = E
        self.C = C
        self.D = D



class Space:
    def __init__(self, objects=None):
        self.objects = [] if objects is None else list(objects)
        self.fields = []
        self.object_limits = None
        self.extend_distance = 10.0

        self.space_limits = None

        self.update_object_limits()

    def add_object(self, obj):
        self.objects.append(obj)
        self.update_object_limits()

    def update_object_limits(self):
        if len(self.objects) == 0:
            self.object_limits = None
            print("No objects in space.")

        else:
            self.object_limits = np.inf, -np.inf
            for obj in self.objects:
                c1 = obj.position
                c2 = obj.position + obj.size

                obj_min = np.minimum(c1, c2)
                obj_max = np.maximum(c1, c2)
                
                self.object_limits = (np.minimum(obj_min, self.object_limits[0]),
                                      np.maximum(obj_max, self.object_limits[1]))

        self.space_limits = self.extend_distance * (self.object_limits[0], self.object_limits[1])

    



