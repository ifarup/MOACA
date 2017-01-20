#!/usr/bin/env python3

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
