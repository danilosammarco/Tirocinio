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


class Settings(QMainWindow):

    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE - Setting')

        tabs = QTabWidget()
        self.tabGeneral = QWidget()
        self.tabOD = QWidget()
        self.tabMacula = QWidget()
        self.tabVessel = QWidget()

        self.createTabGeneralLayout()
        self.createTabODLayout()
        self.createTabMaculaLayout()
        self.createTabVesselLayout()

        tabs.addTab(self.tabGeneral,"General settings")
        tabs.addTab(self.tabOD,"Optic disc settings")
        tabs.addTab(self.tabMacula,"Macula settings")
        tabs.addTab(self.tabVessel,"Vessel settings")
        
        self.setCentralWidget(tabs)           
        self.resize(tabs.width(),tabs.height())

    def createTabGeneralLayout(self):        
        sessionDataLayout=QVBoxLayout()
        sessionDataLabel= QLabel("Automatic compilation of session data")
        sessionDataLayout.addWidget(sessionDataLabel)
        nameLayout=QHBoxLayout()
        name = QLabel("NAME: ")
        self.nameEdit = QLineEdit()
        surname = QLabel("SURNAME: ")
        self.surnameEdit = QLineEdit()
        nameLayout.addWidget(name)
        nameLayout.addWidget(self.nameEdit)
        nameLayout.addWidget(surname)
        nameLayout.addWidget(self.surnameEdit)
        sessionDataLayout.addLayout(nameLayout)

        clinicianLayout=QHBoxLayout()
        version = QLabel("VERSION: ")
        self.versionEdit = QLineEdit()
        clinician = QLabel("CLINICIAN: ")
        self.clinYes = QRadioButton("YES")
        self.clinNo = QRadioButton("NO")
        clinicianLayout.addWidget(version)
        clinicianLayout.addWidget(self.versionEdit)
        clinicianLayout.addWidget(clinician)
        clinicianLayout.addWidget(self.clinYes)
        clinicianLayout.addWidget(self.clinNo)
        sessionDataLayout.addLayout(clinicianLayout)

        boxFolderLayout = QHBoxLayout()
        folder = QLabel("SAVE ANNOTATION IN: ")
        folderButton = QPushButton('Change folder')
        boxFolderLayout.addWidget(folder)
        boxFolderLayout.addWidget(folderButton)
        sessionDataLayout.addLayout(boxFolderLayout)
        self.tabGeneral.setLayout(sessionDataLayout)

    def createTabODLayout(self):
        print()

    def createTabMaculaLayout(self):
        print()

    def createTabVesselLayout(self):
        print()



 
