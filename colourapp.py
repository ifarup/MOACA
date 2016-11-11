#!/usr/bin/env python3
# coding=utf-8

import cluster # to be made by group 2
import sys
import numpy as np
import matplotlib.pyplot as plt
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
from scipy import misc

class AppForm(qt.QMainWindow):
    """
    The main application window.

    Attributes of AppForm:
    image
    menu file_menu
    QAction action
    QLabel main_frame ( needs to be a container for multiple widgets )
    """


    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self.minKValue = 2
        self.maxKValue = 30

        self.setWindowTitle('ColourApp')
        self.create_menu()
        self.create_main_frame()

    def create_action(self, text, slot=None, shortcut=None,
                      tip=None, signal="triggered()"):
        action = qt.QAction(text, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, qtcore.SIGNAL(signal), slot)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_image_action = self.create_action(
            "&Load image", shortcut="Ctrl+L",
            slot=self.on_load_image, tip="Load a new image")
        quit_action = self.create_action(
            "&Quit", slot=self.on_close, shortcut="Ctrl+Q",
            tip="Close the application")

        self.add_actions(
            self.file_menu, (load_image_action, None, quit_action))

    def create_main_frame(self):
        layout = qt.QGridLayout()

        self.image_label = qt.QLabel()
        self.load_image('images/map.png')
        layout.addWidget(self.image_label, 0, 0, 2, 2)

        self.slider = qt.QSlider(qtcore.Qt.Horizontal)
        self.slider.sliderReleased.connect(self.on_slider_released)
        self.initialize_slider(self.slider)
        layout.addWidget(self.slider, 2, 0)

        self.spin_box = qt.QSpinBox()
        self.spin_box.valueChanged.connect(self.on_spin_box_changed)
        self.initialize_spin_box()
        layout.addWidget(self.spin_box, 2, 1)

        self.main_frame = qt.QWidget()
        self.main_frame.setLayout(layout)

        self.setCentralWidget(self.main_frame)
        """
        Legge inn resten av widgets
        """



    def display_image(self):
        image = qt.QImage((self.image * 255).astype('uint8').flatten(),
                          np.shape(self.image)[1],
                          np.shape(self.image)[0],
                          qt.QImage.Format_RGB888)
        pixmap = qt.QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

    def load_image(self, filename):
        self.image = plt.imread(filename)[..., :3] # remove possible alpha channel
        if self.image.dtype == 'uint8':
            self.image = self.image.astype('float') / 255
        self.get_cluster()
        self.display_image()

    def on_close(self):
        self.close()

    def on_load_image(self):
        self.load_image(qt.QFileDialog.getOpenFileName(self, 'Open image',
                                                       filter='All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif);;PNG (*.png)'))

    # Creates the needed legend, one element for each value av the k-array
    def create_legend(self, k):
        kReS = self.k_elements.reshape(k, 1, 3)
        kReS = misc.imresize(kReS, (100, 100), interp='nearest')
        # Now we got the clustered colors, what to do later on?         

    # Calls the clustering function with loaded image and value of slider:
    def on_slider_released(self):
        self.spin_box.setValue(self.slider.value())
        self.get_cluster(self.slider.value())

    def on_spin_box_changed(self):
        self.slider.setValue(self.spin_box.value())
        self.get_cluster(self.spin_box.value())

    def get_cluster(self, k = 3):
        self.im_array, self.k_elements = cluster.cluster(self.image, k)
        self.create_legend(k) # Just a thought on how this could work

    def initialize_slider(self, slider):
        k_value = self.k_elements.shape[0]

        slider.setMinimum(self.minKValue)
        slider.setMaximum(self.maxKValue)
        slider.setTickInterval(1)
        slider.setValue(k_value)
        slider.setPageStep(1)


    def initialize_spin_box(self):
        self.spin_box.setMinimum(self.minKValue)
        self.spin_box.setMaximum(self.maxKValue)
        self.spin_box.setSingleStep(1)
        self.spin_box.setValue(self.slider.value())



def main():
    """
    Run the ColourApp application.
    """
    app = qt.QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
