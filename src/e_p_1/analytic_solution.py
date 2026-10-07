"""Plotting and generation of analytic solution given our assumptions."""

import numpy as np
import pickle
import pyqtgraph as qt


E = 100.0 # V/m
e0 = 8.854e-12
w = 0.05 # 5 cm in m

# for our simulation
voxel_size = 0.001/2
sim_points = 50

t = np.linspace(0, 1, sim_points)

l_tot = np.arange(sim_points) * (0.05 + voxel_size)/sim_points

# v_a = e0 * E * l_a * w
# v_b = e0 * E * l_b * w
# v_tot_anal = np.array(e0 * E * w * (2*l_tot)) # 2*w*l_tot is deltaA

v_tot_anal = np.gradient(np.array(e0 * E * w * (2*l_tot)), t) # 2*w*l_tot is deltaA

# now we do our actual numerical solution

with open("final.pkl", "rb") as file:
    loaded_data = pickle.load(file)

charge_a = loaded_data['charge_a']
charge_b = loaded_data['charge_b']
# v_num = np.array(charge_a - charge_b)
v_num = np.gradient(np.array(charge_a - charge_b), t)






app = qt.mkQApp()
qt.setConfigOption('background', 'w')  # set background to white
qt.setConfigOption('foreground', 'k')  # set foreground (axes, labels) to black

plot = qt.plot()
plot.addLegend()

plot.plot(t, v_tot_anal, pen='r', name='Analytic Solution')
plot.plot(t, v_num, pen='b', name='Numerical Solution')

t0, t1 = 0, t[-1]

plot.getAxis("bottom").setTicks([[
    (t0, "0"),
    (t1, "1")
]])

plot.setLabel('bottom', 'Time', units='s')
plot.setLabel('left', 'Voltage', units='V')



plot.show()
qt.exec()