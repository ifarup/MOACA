#!/usr/bin/env python3

import numpy as np


class HighlightImage:

            # @para oi Original image
    def __init__(self, oi): 
        self.originalImage = oi

            # Edit pixelChangeValue for a lighter hightlighted area and
            # other area darker.
        self.pixelChangeValue = 0.7

    """
    INPUT:
    @para K: Value that should be search for and hightlight pixel in that position
    @para kvi: 2D array with K values, same size as originalImage
    
    OUTPUT:
    The edited original image
    """
    def highlight(self, K, kvi):

                # Changes dtype to float64 and saves a copy of array
        self.edit = self.originalImage.astype(np.float64)
                
        mask1 = (kvi == K)
        mask2 = (kvi != K)

        self.edit[mask1, :] += self.pixelChangeValue
        self.edit[self.edit > 1] = 1
        self.edit[mask2, :] -= self.pixelChangeValue
        self.edit[self.edit < 0] = 0

        return self.edit
