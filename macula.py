#Import libraries and check if the required packages are installeted
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    import os
    import glob
    import sys
    import numpy as np 
    import cv2
    import csv
    import time
except ImportError:
    print("Please install the required packages.")
    sys.exit()

class Macula(QMainWindow):

    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE - Macula')
