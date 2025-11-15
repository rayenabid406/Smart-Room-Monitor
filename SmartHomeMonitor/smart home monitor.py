import sys
import serial
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

# ----------------- CONFIG -----------------
ARDUINO_PORT = 'COM4'  # Arduino USB
STM32_PORT = 'COM3'    # STM32 UART
BAUD_RATE = 115200
MAX_POINTS = 100
# ------------------------------------------

arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
stm32 = serial.Serial(STM32_PORT, BAUD_RATE)

# ----------------- GUI -----------------
app = QtWidgets.QApplication(sys.argv)
win = QtWidgets.QWidget()
win.setWindowTitle("Smart Room Monitor")
layout = QtWidgets.QVBoxLayout()
win.setLayout(layout)

# Graphs
plot_widget = pg.PlotWidget(title="Sensor Values")
plot_widget.addLegend()
layout.addWidget(plot_widget)

ldr_curve = plot_widget.plot(pen='y', name='Photoresistor')
flame_curve = plot_widget.plot(pen='r', name='Flame')
sound_curve = plot_widget.plot(pen='b', name='Sound')

# Numeric labels
ldr_label = QtWidgets.QLabel("LDR: 0")
flame_label = QtWidgets.QLabel("Flame: 0")
sound_label = QtWidgets.QLabel("Sound: 0")
layout.addWidget(ldr_label)
layout.addWidget(flame_label)
layout.addWidget(sound_label)

# Alert box
alert_box = QtWidgets.QLabel("Status: COMFY")
alert_box.setStyleSheet("font-size:20px; background-color: lightgreen;")
layout.addWidget(alert_box)

# Data buffers
ldr_vals, flame_vals, sound_vals = [], [], []

# ----------------- UPDATE FUNCTION -----------------
def update():
    global ldr_vals, flame_vals, sound_vals
    try:
        line = arduino.readline().decode().strip()
        parts = line.split(',')
        ldr = int(parts[0].split(':')[1])
        flame = int(parts[1].split(':')[1])
        sound = int(parts[2].split(':')[1])

        ldr_vals.append(ldr)
        flame_vals.append(flame)
        sound_vals.append(sound)

        if len(ldr_vals) > MAX_POINTS:
            ldr_vals.pop(0)
            flame_vals.pop(0)
            sound_vals.pop(0)

        # Update graphs
        ldr_curve.setData(ldr_vals)
        flame_curve.setData(flame_vals)
        sound_curve.setData(sound_vals)

        # Update numeric labels
        ldr_label.setText(f"LDR: {ldr}")
        flame_label.setText(f"Flame: {flame}")
        sound_label.setText(f"Sound: {sound}")

        # Decide status & send warning to STM32
        if flame > 63:
            status = "!! FIRE ALERT !!"
            color = "red"
            stm32.write(b'FLAME\n')    # Red LED
        elif sound > 85:
            status = "Room too loud"
            color = "orange"
            stm32.write(b'SOUND\n')    # Yellow LED
        elif ldr > 400:
            status = "Room too bright"
            color = "yellow"
            stm32.write(b'LIGHT\n')    # Green LED
        else:
            status = "Room is comfy"
            color = "lightgreen"
            stm32.write(b'OK\n')       # All LEDs off

        alert_box.setText(f"Status: {status}")
        alert_box.setStyleSheet(f"font-size:20px; background-color: {color};")

    except Exception as e:
        pass  # ignore bad lines

# ----------------- TIMER -----------------
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)  # update every 50ms (~20Hz)

# ----------------- RUN APP -----------------
win.show()
sys.exit(app.exec_())
