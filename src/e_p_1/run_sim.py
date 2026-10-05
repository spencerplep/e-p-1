"""Sim for Project 1 in Electrodynamics. The code below runs the cartesian field mill
simulation. All inputs are in m or V/m. Outputs are in Coulomb or V"""


from e_p_1.model import Object, Space, Materials

import pickle
import numpy as np


# import pyqtgraph as qt

# # for all you MATLAB fans
# parula = qt.ColorMap(
#     np.linspace(0, 1, 7),
#     [
#         "#352a87",  # dark blue
#         "#0363e1",
#         "#1485d4",
#         "#06a7c6",
#         "#38b99e",
#         "#92bf73",
#         "#f9e721",  # yellow
#     ],
#     name="parula",
# )



materials = Materials()

voxel_size = 0.001/4 # side length of 0.1 mm

low_ground_plate = Object(size=(0.05, 0.12, 0.001), position=(-0.025, -0.06, -0.001)) # bottom ground plate

sense_plate_a = Object(size=(0.05, 0.05, 0.001), position=(-0.025, -0.05, 0.001))
sense_plate_b = Object(size=(0.05, 0.05, 0.001), position=(-0.025, voxel_size, 0.001))

voltage_view = []

charges = []

print(f"Iterations:{0.12/voxel_size}")

points = 100

iterations = 1 #int(floor(0.12/(voxel_size*points)))

for i in range(iterations):
    blocker_plate = Object(size=(0.05, 0.05, 0.001), position=(-0.025, -0.06 + i*voxel_size, 0.003))

    space = Space(objects=[low_ground_plate, sense_plate_a, sense_plate_b, blocker_plate],
                  dx=voxel_size, extend_distance=0.2)

    grids = space.build_grids()

    grids = space.ambient_field(grids, direction=[0, 0, 1], magnitude=-100.0) # 100 V/m in Z direction

    print("Starting iteration {i}/{0.12/voxel_size}")

    out = space.solve_grids(epsilon=1e-2, v=True)

    voltage_view.append(-1 * out.grid.voltage[space.grids.single_dim_to_coord(0, 0), :, :])

    charges.append(space.get_object_charge()[1, 2])

voltage_view = np.array(voltage_view)
charges = np.array(charges)

print("Run complete: Saving now")

data = {
    "voltage_view": voltage_view,
    "charges": charges
}

with open("data.pkl", "wb") as file:
    pickle.dump(data, file)

# app = qt.mkQApp()
# view = qt.ImageView()
# view.setImage(voltage_view)
# view.show()
# view.getView().invertY(False)
# view.setColorMap(parula)
# qt.exec()


# app = qt.mkQApp()
# plot_window = qt.plot(out.residual, title="Solver residual")
# plot_window.setLabel("bottom", "Iteration")
# plot_window.setLabel("left", "Residual")
# qt.exec()