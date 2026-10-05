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


with open("data.pkl", "rb") as file:
    loaded_data = pickle.load(file)

print(f"Loaded: {[item for item in loaded_data]}")

voltage_view = loaded_data['voltage_view']
charges = loaded_data['charges']

v = voltage_view[0, :, :]

print(charges)

a_charge = charges

app = qt.mkQApp()
view = qt.ImageView()
view.setImage(a_charge)
view.show()
view.getView().invertY(False)
view.setColorMap(parula)
qt.exec()