#!/usr/bin/env python3
# coding=utf-8

"""
MOACA: Python GUI app for colour visualisation

Copyright (C) 2016 Håvard Ola Eggen, Ivar Farup, Tarjei Holtskog, Rolf
Arne Myraunet, Lars Niebuhr, Amund Faller Råheim, Jakob Voigt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import cluster
import sys
import numpy as np
import matplotlib.pyplot as plt
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
from skimage.transform import resize
import math
from HighlightImage import HighlightImage

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
        
        # Defining stuff here to counter some trouble later on
        self.legend_view = qt.QGraphicsView()
        self.legend_view.setFixedHeight(20)    # Matching height with pixmap
        self.legend_view.setFrameStyle(0)               # Don't want any scrollbar
        self.local_scene = qt.QGraphicsScene()
        self.legend_view.setScene(self.local_scene)
        
        # Constants
        self.minKValue = 2
        self.maxKValue = 30
        

        self.setWindowTitle('MOACA')
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

        # Picture
        self.image_label = qt.QLabel()
        self.load_image('images/map.png')
        layout.addWidget(self.image_label, 0, 0, 2, 2)
        
        # Slider
        self.slider = qt.QSlider(qtcore.Qt.Horizontal)
        self.slider.sliderReleased.connect(self.on_slider_released)
        self.initialize_slider(self.slider)
        layout.addWidget(self.slider, 2, 0)

        # Spinbox?
        self.spin_box = qt.QSpinBox()
        self.spin_box.valueChanged.connect(self.on_spin_box_changed)
        self.initialize_spin_box()
        layout.addWidget(self.spin_box, 2, 1)
        
        # Legend
        self.create_legend_colors(self.slider.value())
        layout.addWidget(self.legend_view)

        self.main_frame = qt.QWidget()
        self.main_frame.setLayout(layout)

        self.setCentralWidget(self.main_frame)
        """
        Legge inn resten av widgets
        """



    def display_image(self, im):
        image = qt.QImage((im * 255).astype('uint8').flatten(),
                          np.shape(im)[1],
                          np.shape(im)[0],
                          qt.QImage.Format_RGB888)
        pixmap = qt.QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)

    def load_image(self, filename):
        self.image = plt.imread(filename)[..., :3] # remove possible alpha channel
        if self.image.dtype == 'uint8':
            self.image = self.image.astype(float) / 255
        else:
            self.image = self.image.astype(float) # in case it is 'float32', not 'float42'
        self.get_cluster()
        self.display_image(self.image)
        self.hl = HighlightImage(self.image)

    def on_close(self):
        self.close()

    def on_load_image(self):
        filename = qt.QFileDialog.getOpenFileName(self, 'Open image',
                                                  filter='All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif);;PNG (*.png)')
        if filename != '':
            self.load_image(filename)
            self.get_cluster(self.slider.value())
            self.create_legend_colors(self.slider.value())

    # Creates the needed legend, one color for each value av the k-array
    def create_legend_colors(self, k):
        k_reshape = self.k_elements.reshape(1, k, 3)    # Reshape the list of color elements for
                                                        # collecting and making them horisontal
        k_resize = resize(k_reshape, (20, self.im_array.shape[1]), order=0) # Resize the reshaped list to make the colors
                                                                            # more defined and solid
        self.colorBar = qt.QImage((k_resize * 255).astype('uint8').flatten(),    # Pure copy and paste from 
                            np.shape(k_resize)[1],                               # ivarh
                            np.shape(k_resize)[0],
                            qt.QImage.Format_RGB888)
        pixmap = qt.QGraphicsPixmapItem(qt.QPixmap.fromImage(self.colorBar), None, self.local_scene)
        pixmap.mousePressEvent = self.click_color_bar     # Reacting to a click, but not to release?
                                                          # Not a big problem, but feels a bit strange
                                                          # when trying it out
 
        
    # Event for making magic when user clicks a color in the color bar
    # Inspiration from this page: http://stackoverflow.com/questions/3522701/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image
    def click_color_bar(self, event):

        pos = qtcore.QPoint(event.pos().x(), event.pos().y())   # Finds the position of cursor
        
        # Finding the index value
        index = math.floor(pos.x() / self.im_array.shape[1] * self.slider.value())

        hli = self.hl.highlight(index, self.im_array)
        self.display_image(hli)
        
    # Calls the clustering function with loaded image and value of slider:
    def on_slider_released(self):
        self.spin_box.setValue(self.slider.value())
        self.get_cluster(self.slider.value())
        self.create_legend_colors(self.slider.value())


    def on_spin_box_changed(self):
        self.slider.setValue(self.spin_box.value())
        self.get_cluster(self.spin_box.value())
        self.create_legend_colors(self.slider.value())

    def get_cluster(self, k = 3):
        self.im_array, self.k_elements = cluster.cluster(self.image, k)


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
