import sys
import numpy as np
from scipy.interpolate import make_interp_spline
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSlider, QLabel
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PID:
    def __init__(self, kp, ki, kd, setpoint, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.dt = dt
        self.clear()

    def clear(self):
        self.integral = 0.0
        self.pre_err = 0.0
        self.feedback_value = 0.0
        self.yp = 0.0

    def compute(self, feedback_value=None):
        if feedback_value is not None:
            self.feedback_value = feedback_value

        error = self.setpoint - self.feedback_value
        self.integral += error * self.dt
        derivative = (error - self.pre_err) / self.dt
        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )
        self.pre_err = error
        self.feedback_value = output
        return output

    def lowpass_filter(self, x, beta):
        y = beta * x + (1 - beta) * self.yp
        self.yp = y
        return y


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化 PID 控制器
        self.pid = PID(kp=1.0, ki=10.0, kd=0.001, setpoint=1, dt=0.1)

        # 提前宣告屬性，讓 IDE 不會跳警告
        self.kp_slider = None
        self.ki_slider = None
        self.kd_slider = None
        self.figure = None
        self.canvas = None

        # 建立 UI
        self.init_ui()
        self.update_plot()

    def init_ui(self):
        self.setWindowTitle('PID Controller Tuning')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        sliders_layout = QVBoxLayout()

        self.kp_slider = self.create_slider('Kp', 0, 30, 10, sliders_layout)
        self.ki_slider = self.create_slider('Ki', 0, 200, 100, sliders_layout)
        self.kd_slider = self.create_slider('Kd', 0, 100, 1, sliders_layout)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addLayout(sliders_layout)
        layout.addWidget(self.canvas)

        self.kp_slider.valueChanged.connect(self.update_plot)
        self.ki_slider.valueChanged.connect(self.update_plot)
        self.kd_slider.valueChanged.connect(self.update_plot)

    @staticmethod
    def create_slider(label, min_val, max_val, init_val, layout):
        container = QHBoxLayout()

        text_label = QLabel(f"{label}:")
        container.addWidget(text_label)

        value_label = QLabel()
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        value_label.setMinimumWidth(80)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(init_val)

        if label == 'Kd':
            slider.valueChanged.connect(lambda v: value_label.setText(f"{v / 1000:.3f}"))
        else:
            slider.valueChanged.connect(lambda v: value_label.setText(f"{v / 10:.1f}"))

        container.addWidget(slider)
        container.addWidget(value_label)
        layout.addLayout(container)

        return slider

    def update_plot(self):
        self.pid.kp = self.kp_slider.value() / 10.0
        self.pid.ki = self.ki_slider.value() / 10.0
        self.pid.kd = self.kd_slider.value() / 1000.0
        self.pid.clear()

        y_list = [0]
        x = 0
        for _ in range(29):
            x = self.pid.compute(x)
            x = self.pid.lowpass_filter(x, 0.5)
            y_list.append(x)

        x_list = range(30)
        x_smooth = np.linspace(0, 29, 300)
        y_smooth = make_interp_spline(x_list, y_list)(x_smooth)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_smooth, y_smooth, label='System Response')
        ax.axhline(y=self.pid.setpoint, color='r', linestyle='--', label='Set Point')
        ax.set_title('PID Controller Response')
        ax.set_xlabel('Time')
        ax.set_ylabel('Output')
        ax.legend()
        ax.grid(True)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
