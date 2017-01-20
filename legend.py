# -*- coding: utf-8 -*-

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

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    
    l1 = QLabel()
    l2 = QLabel()
    l3 = QLabel()
    l4 = QLabel()
    
    l1.setText("Hello World")
    l4.setText("TutorialsPoint")
    l2.setText("Welcome to Python GUI Programming")
    
    l1.setAlignment(Qt.AlignCenter)
    l3.setAlignment(Qt.AlignCenter)
    l4.setAlignment(Qt.AlignRight)
    l3.setPixmap(QPixmap('./images/map.png'))
    
    vbox = QVBoxLayout()
    vbox.addWidget(l1)
    vbox.addStretch()
    vbox.addWidget(l2)
    vbox.addStretch()
    vbox.addWidget(l3)
    vbox.addStretch()
    vbox.addWidget(l4)
	
    l1.setOpenExternalLinks(True)
    l4.linkActivated.connect(clicked)
    l2.linkHovered.connect(hovered)
    l1.setTextInteractionFlags(Qt.TextSelectableByMouse)
    win.setLayout(vbox)
	
    win.setWindowTitle("QLabel Demo")
    win.show()
    sys.exit(app.exec_())
	
def hovered():
   print ("hovering")
def clicked():
   print ("clicked")
	
if __name__ == '__main__':
   window()
