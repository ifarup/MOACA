#!/usr/bin/env python3

import time     # Just for testing execution time
import copy

class HighlightImage:

    # @para oi Original image to change
    def __init__(self, oi): 
        self.originalImage = oi

            # Edit pixelChangeValue for a lighter hightlighted area and
            # other area darker.
        if oi.dtype == 'float32':
            self.pixelChangeValue = 0.8
        elif oi.dtype == 'float64':
            self.pixelChangeValue = 0.7
        elif oi.dtype == 'uint8':
            self.pixelChangeValue = 100
        elif oi.dtype == 'uint16':
            self.pixelChangeValue = 13107
    
    """
    INPUT:
    @para K: Value that should be search for and hightlight pixel in that position
    @para kvi: 2D image with K values, same size as originalImage
    
    OUTPUT:
    The edited original image
    """
    def highlight(self, K, kvi):
        self.editedimage = copy.copy(self.originalImage)

        starttime = time.time()
            # Checks that kvi is valid
        if len(kvi.shape) > 2:
            return "Expected a 2D array"
        
            # Get colums and rows from kvi
        rows = kvi.shape[0]
        colums = kvi.shape[1]
        
        for j in range(rows):
            for i in range(colums):
                if kvi[j][i] == K:
                    self.highlight_pixel(j, i)
                else:
                    self.darken_pixel(j, i)
        
        print("--- %s seconds ---" % (time.time() - starttime))
        
        return self.editedimage

    def highlight_pixel(self, j, i):
        
        for r in range(3):
            pixelValue = self.editedimage[j][i][r]+self.pixelChangeValue
            
            if self.editedimage.dtype == 'float32':
                if pixelValue > 1:
                    pixelValue = 1
            elif self.editedimage.dtype == 'float64':
                if pixelValue > 1:
                    pixelValue = 1
            elif self.editedimage.dtype == 'uint16':
                if pixelValue > 65535:
                    pixelValue = 65535
            else:
                if pixelValue > 255:
                    pixelValue = 255
            
            self.editedimage[j][i][r] = pixelValue

    def darken_pixel(self, j, i):
        
        for r in range(3):
            pixelValue = self.editedimage[j][i][r]-self.pixelChangeValue
            if pixelValue < 0:
                pixelValue = 0

            self.editedimage[j][i][r] = pixelValue
        