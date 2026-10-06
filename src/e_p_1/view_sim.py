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


with open("full_run_parr_data.pkl", "rb") as file:
    loaded_data = pickle.load(file)

print(f"Loaded: {[item for item in loaded_data]}")

voltage_view = loaded_data['voltage_view']
charges = loaded_data['charges']

v = voltage_view[:, :, :]

print(charges)

# a_charge = charges[:, 0]
# b_charge = charges[:, 1]

app = qt.mkQApp()
view = qt.ImageView()
view.setImage(v)
view.show()
view.getView().invertY(False)
view.setColorMap(parula)
qt.exec()

# 
# pw = qt.plot(title="Sense Plate Charge vs. Blocker Plate Position")
# legend = pw.addLegend()
# pw.plot(a_charge, pen="b", name="A")
# pw.plot(b_charge, pen="r", name="B")
# pw.show()
