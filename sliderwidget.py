
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
import colourapp


class SliderWidget(qt.QSlider):


    def __init__(self):
        # Slider initialization values:
        self.minSliderValue = 1
        self.maxSliderValue = 20
        self.defaultSliderValue = 3


        super(qtcore.Qt.Horizontal, self)
        self.initializeSlider(self)


    def initializeSlider(self):
        self.setMinimum(self.minSliderValue)
        self.setMaximum(self.maxSliderValue)
        self.setValue(self.defautSliderValue)
        self.setTickInterval(1)

        self.sliderReleased()

