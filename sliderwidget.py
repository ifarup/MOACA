
import PyQt4.QtGui as qt
import PyQt4.QtCore as qtcore
import colourapp


class SliderWidget(qt.QSlider):

    def __init__(self, o):
        super().__init__(o)

        # Slider initialization values:
        self.minSliderValue = 1
        self.maxSliderValue = 20
        self.defaultSliderValue = 3

        self.setMinimum(self.minSliderValue)
        self.setMaximum(self.maxSliderValue)
        self.setValue(self.defaultSliderValue)
        self.setTickInterval(1)