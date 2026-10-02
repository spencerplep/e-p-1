




from e_p_1.model import Object, Space, Materials


import numpy as np
import pyqtgraph as qt


materials = Materials()

a = Object(size=(20, 20, 1), position=(-10, -10, 0), material=materials.grounded)

# b = Object(size=(1, 8, 2), position=(0, -4, 1.55), material=materials.metal)

c = Object(size=(20, 20, 1), position=(-10, -10, 5), material=materials.grounded)

space = Space( objects=[a, c], dx=0.5, extend_distance=1)

grids = space.build_grids()

grids = space.ambient_field(grids, direction=[0, 0, 1], magnitude=-100.0)


out = space.solve_grids(epsilon=1e-2)

v = out.grid.voltage

z = -1 * v[space.grids.single_dim_to_coord(0, 0), :, :]

z = np.gradient(z, axis=1)

print(z.shape)

app = qt.mkQApp()
view = qt.ImageView()
view.setImage(z)
view.show()
view.getView().invertY(False)
qt.exec()

# app = qt.mkQApp()
# plot_window = qt.plot(out.residual, title="Solver residual")
# plot_window.setLabel("bottom", "Iteration")
# plot_window.setLabel("left", "Residual")
# qt.exec()