




from e_p_1.model import Object, Space


import numpy as np
import pyqtgraph as qt


a = Object(size=(4, 1, 1), position=(0, 0, 0))

b = Object(size=(4, 1, 2), position=(0, 1, 0))

c = Object(size=(4, 1, 3), position=(0, 2, 0))

space = Space(space_limits=[[-5, -5, -5], [5, 5, 5]], objects=[a, b, c])

grids = space.build_grids()

grids = space.ambient_field(grids, direction=[0, 0, 1], magnitude=-100.0)


out = space.solve_grids()

v = out.grid.voltage

z = v[space.grids.single_dim_to_coord(0, 0), :, :]

app = qt.mkQApp()
view = qt.ImageView()
view.setImage(z)
view.show()
qt.exec()

# app = qt.mkQApp()
# plot_window = qt.plot(out.residual, title="Solver residual")
# plot_window.setLabel("bottom", "Iteration")
# plot_window.setLabel("left", "Residual")
# qt.exec()