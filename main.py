
#Import libraries and check if the required packages are installeted
try:
    from opticdisc import *
    from settings import *
    from macula import *
    from vessel import *
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

#Global variables
checkDrawEllipse = False
currentAddress=os.getcwd()
currentImage=""

class MainWindow(QMainWindow):
    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE')

        # || GRAPHICS || - MENU -
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        settingsAction=QAction(QIcon('settings.png'), '&Open settings', self)     
        settingsAction.setShortcut("Ctrl+S")
        settingsAction.triggered.connect(self.openSettings)
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(settingsAction)
        fileMenu.addAction(exitAction)
        helpMenu = mainMenu.addMenu('Help')

        cWidget = QWidget(self)
        mainLayout = QHBoxLayout()
        
        # || GRAPHICS || - FIRST COLUMN: FOLDER -
        boxFolderLayout = QVBoxLayout()
        folder = QPushButton('Change folder', cWidget)
        self.listWidget = QListWidget()
        self.listWidget.setMinimumSize(200,100)
        boxFolderLayout.addWidget(folder)
        boxFolderLayout.addWidget(self.listWidget)
        mainLayout.addLayout(boxFolderLayout)

        # || GRAPHICS || - SECOND COLUMN: IMAGE -
        buttonImageLayout = QVBoxLayout()
        imageLayout = QHBoxLayout()
        od = QPushButton('Optic Disc', cWidget)
        macula = QPushButton('Macula', cWidget)
        vessel = QPushButton('Vessel', cWidget)
        imageLayout.addWidget(od)
        imageLayout.addWidget(macula)
        imageLayout.addWidget(vessel)
        buttonImageLayout.addLayout(imageLayout)
        self.label = QLabel(self)
        self.pixmap = QPixmap('ellisse.png')
        self.label.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(),self.pixmap.height())
        buttonImageLayout.addWidget(self.label)
        mainLayout.addLayout(buttonImageLayout)

        # || GRAPHICS || -THIRD COLUMN: BUTTON -
        buttonLayout = QVBoxLayout()
        buttonLayout.setSpacing(2)
        mainLayout.addLayout(buttonLayout)
        self.prevImageButton = QPushButton('Previous image', cWidget)
        buttonLayout.addWidget(self.prevImageButton)
        self.nextImageButton = QPushButton('Next image', cWidget)
        buttonLayout.addWidget(self.nextImageButton)
        
        #WIDGET SIGNALS
        folder.clicked.connect(self.changeFolder)
        od.clicked.connect(self.opticDisc)
        macula.clicked.connect(self.macula)
        vessel.clicked.connect(self.vessel)
        self.prevImageButton.clicked.connect(self.prevImage)
        self.nextImageButton.clicked.connect(self.nextImage)
        self.listWidget.currentItemChanged.connect(self.changeImage)

        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)
        self.loadImage()

    def openSettings(self):
        self.settingsWindow = Settings()
        self.settingsWindow.show()        

    #A new image is displayed when it is selected from the folder files
    def changeImage(self,item):
        global currentAddress, currentImage
        self.checkPrevNextButton()
        currentImage=QListWidgetItem(item).text()
        self.label.setPixmap(QPixmap(currentAddress+"/"+QListWidgetItem(item).text()))

    #The image with the name 'name' is displayed. The image must be present in the folder selected in the folder widget    
    def changeImageTemp(self,name):
        global currentAddress
        self.label.setPixmap(QPixmap(currentAddress+"/"+name))

    #Open Optic Disc
    def opticDisc(self,item):
        self.opticDiscWindow = OpticDiscWindow(currentAddress+"/"+currentImage)
        self.opticDiscWindow.show()

    # Disabled nextImageButton if the selected item is the last one, 
    # disabled prevImageButton if the selected item is the first 
    # and enable both button in the other case
    def checkPrevNextButton(self):
        row=self.listWidget.currentRow()
        if self.listWidget.count() < 2:
            self.prevImageButton.setEnabled(False)
            self.nextImageButton.setEnabled(False)
        elif row == 0:
            self.prevImageButton.setEnabled(False)
        elif row == self.listWidget.count()-1:
            self.nextImageButton.setEnabled(False)
        else:
            self.prevImageButton.setEnabled(True)
            self.nextImageButton.setEnabled(True)

    def prevImage(self,event):
        row=self.listWidget.currentRow()-1
        self.listWidget.setCurrentRow(row)
        #self.checkPrevNextButton()
    
    def nextImage(self,event):
        row=self.listWidget.currentRow()+1
        self.listWidget.setCurrentRow(row)
        #self.checkPrevNextButton()

    #Open Macula
    def macula(self,item):
        self.maculaWindow = Macula()
        self.maculaWindow.show()

    #Open Vessel
    def vessel(self,item):
        self.vesselWindow = Vessel()
        self.vesselWindow.show()

    #To change the current folder
    def changeFolder(self):
        global currentAddress
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        currentAddress = file
        self.loadImage()

    #To load all the images in the selected folder
    def loadImage(self):
        global currentAddress
        self.listWidget.clear()
        possibleExtensions=["bmp","cdp","djvu","djv","eps","gif","gpd","jpd","jpg","jpeg","pict","png","tga","tiff","pcx","psd","webp"]
        files=os.listdir(currentAddress+"/")
        files.sort()
        for i in files:
            extension=i.split(".")
            if len(extension)>1 and extension[1] in possibleExtensions:
                item = QListWidgetItem(i)
                self.listWidget.addItem(item)     
        if self.listWidget.count()!= 0:
            self.listWidget.setCurrentRow(0)


class StartSession(QMainWindow):

    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE - Session')

        cWidget = QWidget(self)
        mainLayout = QVBoxLayout()

        label = QLabel(self)
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('vampire.gif')
        label.setPixmap(pixmap)
        mainLayout.addWidget(label)

        nameLayout=QHBoxLayout()
        name = QLabel("NAME: ")
        self.nameEdit = QLineEdit()
        self.nameEdit.textEdited.connect(self.checkData)
        surname = QLabel("SURNAME: ")
        self.surnameEdit = QLineEdit()
        self.surnameEdit.textEdited.connect(self.checkData)
        nameLayout.addWidget(name)
        nameLayout.addWidget(self.nameEdit)
        nameLayout.addWidget(surname)
        nameLayout.addWidget(self.surnameEdit)
        mainLayout.addLayout(nameLayout)

        clinicianLayout=QHBoxLayout()
        version = QLabel("VERSION: ")
        self.versionEdit = QLineEdit()
        self.versionEdit.textEdited.connect(self.checkData)
        clinician = QLabel("CLINICIAN: ")
        self.clinYes = QRadioButton("YES")
        self.clinNo = QRadioButton("NO")
        self.clinYes.clicked.connect(self.checkData)
        self.clinNo.clicked.connect(self.checkData)
        clinicianLayout.addWidget(version)
        clinicianLayout.addWidget(self.versionEdit)
        clinicianLayout.addWidget(clinician)
        clinicianLayout.addWidget(self.clinYes)
        clinicianLayout.addWidget(self.clinNo)
        mainLayout.addLayout(clinicianLayout)

        boxFolderLayout = QHBoxLayout()
        folder = QLabel("SAVE ANNOTATION IN: ")
        folderButton = QPushButton('Change folder', cWidget)
        boxFolderLayout.addWidget(folder)
        boxFolderLayout.addWidget(folderButton)
        mainLayout.addLayout(boxFolderLayout)

        self.startButton = QPushButton('START SESSION', cWidget)
        self.startButton.setEnabled(False)
        self.startButton.clicked.connect(self.startSession)
        mainLayout.addWidget(self.startButton)

        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)            

    def startSession(self):
        self.MainWindow = MainWindow()
        self.MainWindow.show()
        folder=time.strftime("%Y-%m-%d&%H:%M:%S")
        os.mkdir(folder)
        with open (folder+'/annotationDetails.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['NOME',self.nameEdit.text()])
            employee_writer.writerow(['SURNAME',self.surnameEdit.text()])
            employee_writer.writerow(['VERSION',self.versionEdit.text()])
            employee_writer.writerow(['CLINICIAN',str(self.clinYes.isChecked())])
        self.close()

    def checkData(self,event):
        check=True
        if self.nameEdit.text()=="":
            check=False
        elif self.surnameEdit.text()=="":
            check=False
        elif self.versionEdit.text()=="":
            check=False
        elif self.clinYes.isChecked()==False and self.clinNo.isChecked()==False:
            check=False
        self.startButton.setEnabled(check)





if __name__ == '__main__':
  app = QApplication(sys.argv)
  main = MainWindow()
  #main = StartSession()
  main.show()
  sys.exit(app.exec_())