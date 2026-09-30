### Here we want the basic cell, space, and attributes for those objects.

import numpy as np


class out:
    pass


class Material:
    def __init__(self, Sigma, Epsilon, boundary=False, grounded=False):
        self.Sigma = Sigma
        self.Epsilon = Epsilon
        # self.Mu = Mu
        self.boundary = boundary
        self.grounded = grounded



Metal = Material(Sigma=np.inf, Epsilon=1.0)

Boundary = Material(Sigma=0.0, Epsilon=1.0, boundary=True)

Grounded = Material(Sigma=np.inf, Epsilon=1.0, grounded=True)

class Object:
    def __init__(self, size, position, material=Grounded):
        # only rectangular for now
        # all of these dimensions are in units, and grid sizes are determined later.

        self.size = np.array(size)
        self.position = np.array(position)
        self.material = material

        if self.size.shape != self.position.shape:
            raise ValueError("Size and position must have the same number of dimensions.")

    @property
    def bounds(self):
        return self.position, (self.position + self.size)

class Grids:
    # you really do need to initialize the grids with a specific voxel size
    def __init__(self, dx):
        self.voltage = None
        self.charge = None
        self.boundary = None
        self.pec = None
        self.gnd = None
        self.dx = dx
        self.space_limits = None

    def dim_to_coords(self, dim):
        return (dim - self.space_limits[0]) / self.dx

    def single_dim_to_coord(self, dim, axis):
        return int(round((dim - self.space_limits[0][axis]) / self.dx))

class Space:
    def __init__(self, objects=None, space_limits=None, ):
        self.objects = objects
        self.fields = []
        self.object_limits = None
        self.smallest_feature = None
        self.extend_distance = 0.5

        self.space_limits = space_limits
        self.space_limits_flag = False
        if space_limits:
            self.space_limits_flag = True

        self.grids = None

        self.update_object_limits()

    def add_object(self, obj):
        if not self.objects:
            self.objects = []

        self.objects.append(obj)
        self.update_object_limits()

    def update_object_limits(self):
        if not self.objects:
            print("No objects in space.")
            return None

        else:
            self.object_limits = np.inf, -np.inf
            for obj in self.objects:
                c1 = obj.position
                c2 = obj.position + obj.size

                smallest_feature = np.min(obj.size)
                if self.smallest_feature is None or smallest_feature < self.smallest_feature:
                    self.smallest_feature = smallest_feature

                obj_min = np.minimum(c1, c2)
                obj_max = np.maximum(c1, c2)
                
                self.object_limits = (np.minimum(obj_min, self.object_limits[0]),
                                      np.maximum(obj_max, self.object_limits[1]))

        self.object_limits_size = max(self.object_limits[1] - self.object_limits[0])

        # set the sim limits if we didnt define them earlier
        if not self.space_limits_flag:
            self.space_limits = -1 * self.extend_distance * self.object_limits_size + self.object_limits[0], self.extend_distance * self.object_limits_size + self.object_limits[1]


    def build_grids(self, dx=1/4):
        # Build the whole simulation grid, with some voxel size determined by smallest feature.

        if dx is None:
            dx = self.smallest_feature / 10.0  # So that the smallest feature is well resolved

        
        if self.space_limits is None:
            print("Space limits not initialized.")
            return None

        whole_grid = np.mgrid[self.space_limits[0][0]:self.space_limits[1][0]:dx,
                              self.space_limits[0][1]:self.space_limits[1][1]:dx,
                              self.space_limits[0][2]:self.space_limits[1][2]:dx]

        # Scalar grids
        # sigma_grid = whole_grid[0] * 0  # Initialize with zeros
        # epsilon_grid = whole_grid[0] * 1 # coefficient of e0
        voltage_grid = whole_grid[0] * 0
        charge_grid = whole_grid[0] * 0

        boundary_grid = whole_grid[0] * 0
        # set true for boundary voxels
        boundary_grid[0, :, :] = 1
        boundary_grid[-1, :, :] = 1
        boundary_grid[:, 0, :] = 1
        boundary_grid[:, -1, :] = 1
        boundary_grid[:, :, 0] = 1
        boundary_grid[:, :, -1] = 1

        pec_grid = whole_grid[0] * 0
        gnd_grid = whole_grid[0] * 0

        grids = Grids(dx=dx)

        grids.space_limits = self.space_limits
        
        
        if self.objects:

            for obj in self.objects:
                pos1, pos2 = obj.bounds # the min and max corners of the object

                pos1 = grids.dim_to_coords(pos1)
                pos2 = grids.dim_to_coords(pos2)

                # slice out the volume of our object; slice throught the object
                object_vol = (slice(int(pos1[0]), int(pos2[0])), 
                            slice(int(pos1[1]), int(pos2[1])), 
                            slice(int(pos1[2]), int(pos2[2])))

                # object voltage shouldnt be anything
                voltage_grid[object_vol] = 0

                if obj.material.grounded:
                    gnd_grid[object_vol] = 1
                elif obj.material.Sigma == np.inf:
                    pec_grid[object_vol] = 1

        # would be useful for having voltage sources inside my space
        # grids.sources = source_grid
        # grids.source_vals = source_vals_grid
        grids.voltage = voltage_grid
        grids.charge = charge_grid
        grids.boundary = boundary_grid
        grids.pec = pec_grid
        grids.gnd = gnd_grid
        
        self.grids = grids

        return grids

    def set_object_vols_to(self, v = 0, grids = None):
            if grids is None:
                self.grids = self.set_object_vols_to(v, self.grids)
                return
            
            if self.objects:

                for obj in self.objects:
                    pos1, pos2 = obj.bounds # the min and max corners of the object

                    pos1 = grids.dim_to_coords(pos1)
                    pos2 = grids.dim_to_coords(pos2)

                    # slice out the volume of our object; slice throught the object
                    object_vol = (slice(int(pos1[0]), int(pos2[0])), 
                                slice(int(pos1[1]), int(pos2[1])), 
                                slice(int(pos1[2]), int(pos2[2])))

                    # set and keep the residual
                    obj.res_voltage = np.sum(grids.voltage[object_vol])
                    grids.voltage[object_vol] = v

                return grids

    def ambient_field(self, grids, direction, magnitude, ground_plane = None):
        """Set the ambient electric field in the simulation space.
        Currently only works for a single direction of field."""
        if ground_plane is None:
            axis = np.argmax(np.abs(direction))
            sign = np.sign(direction[axis])

        # horrible cursed indexing; for some dimension, I am setting the faces at those edges 
        # to the voltage values that will giveme my ambient field.

        index = [slice(None)] * grids.voltage.ndim

        for i in range(grids.voltage.shape[axis]):
            index[axis] = i
            grids.voltage[tuple(index)] += sign * magnitude * grids.dx * i

        index[axis] = 0                 # lower face; use -1 for upper face
        grids.gnd[tuple(index)] = 1

        return grids


    def step_grid(self, grids):
        # we will only solve votage and set charge and etc off of that. Assume field form +z direction:
        v_next = grids.voltage * 0

        v_next[:-1, :, :] += grids.voltage[1:, :, :]
        v_next[1:, :, :] += grids.voltage[:-1, :, :]

        v_next[:, :-1, :] += grids.voltage[:, 1:, :]
        v_next[:, 1:, :] += grids.voltage[:, :-1, :]

        v_next[:, :, :-1] += grids.voltage[:, :, 1:]
        v_next[:, :, 1:] += grids.voltage[:, :, :-1]

        v_next = 1/6 * v_next

        _grids = grids

        # set boundaries to earlier values
        v_next = v_next * ((grids.boundary * -1) + 1) + grids.boundary * grids.voltage
        
        _grids.voltage = v_next
        
        _grids = self.set_object_vols_to(0, _grids)

        return _grids

    def solve_grids(self, epsilon=1e-4):

        residual = []
        _grid_last = self.grids
        r = np.inf
        # while r > epsilon:
        for _ in range(1000):
            v_last = _grid_last.voltage.copy()
            _grid_next = self.step_grid(_grid_last)
            r = np.sqrt(np.sum(np.abs(v_last - _grid_next.voltage)**2))
            residual.append(r)
            _grid_last = _grid_next
            print(r, "\n")


        out.residual = residual
        out.grid = _grid_next

        return out