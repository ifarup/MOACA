#!/usr/bin/env python3

import cluster # to be made by group 2
import sys
import numpy as np
import matplotlib.pyplot as plt
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
import sliderwidget as slider
import cluster

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
        layout = qt.QVBoxLayout()

        self.image_label = qt.QLabel()
        self.load_image('images/map.png')
        layout.addWidget(self.image_label)

        # Utprøving av slider:
        self.slider = slider.SliderWidget(qtcore.Qt.Horizontal)
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        layout.addWidget(self.slider)

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
        self.display_image()

    def on_close(self):
        self.close()

    def on_load_image(self):
        self.load_image(qt.QFileDialog.getOpenFileName(self, 'Open image',
                                                       filter='All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif);;PNG (*.png)'))
    
    # Creates the needed legend, one element for each value av the k-array
    def create_legend(slef):
        for k_element in self.k:
            self.legend.add(k_element)
            

    # Calls the clustering function with loaded image and value of slider:
    def on_slider_value_changed(self):
        # imagearray, k = cluser."" clusterfunksjonen_til_noobsa ""(self.image, self.slider.value(self))
        self.slider.value()


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
