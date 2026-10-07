import pyqtgraph as qt
import numpy as np
import pickle

# for all you MATLAB fans
parula = qt.ColorMap(
    np.linspace(0, 1, 7),
    [
        "#352a87",  # dark blue
        "#0363e1",
        "#1485d4",
        "#06a7c6",
        "#38b99e",
        "#92bf73",
        "#f9e721",  # yellow
    ],
    name="parula",
)


with open("correct_run_1.pkl", "rb") as file:
    loaded_data = pickle.load(file)

print(f"Loaded: {[item for item in loaded_data]}")

voltage_view = loaded_data['voltage_view']
charge_a = loaded_data['charge_a']
charge_b = loaded_data['charge_b']

# v = np.gradient(voltage_view[:, :, :], axis=2)
v = voltage_view[:, :, :]
# print(charge_a, charge_b)

a_charge = charge_a
b_charge = charge_b

# app = qt.mkQApp()
# view = qt.ImageView()
# view.setImage(v)
# view.show()
# view.getView().invertY(False)
# view.setColorMap(parula)
# qt.exec()

app = qt.mkQApp()
qt.setConfigOption('background', 'w')
qt.setConfigOption('foreground', 'k')
win = qt.GraphicsLayoutWidget(show=True)
plot = win.addPlot(title="Voltage for X=0")
image = qt.ImageItem(v[0, :, :], colorMap=parula)

plot.addItem(image)

# plot.setXRange(-0.07, 0.07)
# plot.setYRange(-0.02, 0.024)

nx, ny = v.shape[1], v.shape[2]

plot.getAxis("bottom").setTicks([[
    (0, "-7"),
    (nx, "7")
]])

plot.getAxis("left").setTicks([[
    (0, "-2"),
    (ny, "2.4")
]])

plot.setLabel('left', 'Y Axis', units='cm')
plot.setLabel('bottom', 'X Axis', units='cm')

colorbar = qt.ColorBarItem(values=(0, 1), colorMap=parula, label="Normalized Voltage", interactive=False)
win.addItem(colorbar)


qt.exec()


# pw = qt.plot(title="Sense Plate Charge (Steady State Current) vs. Blocker Plate Position")
# legend = pw.addLegend()
# pw.plot(a_charge, pen="b", name="Plate A")
# pw.plot(b_charge, pen="r", name="Plate B")
# pw.show()
# qt.exec()
