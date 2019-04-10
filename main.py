<<<<<<< HEAD
#Import
=======
#Import libraries and check if the required packages are installeted
>>>>>>> d33efba341b5279080ce5dafe00cd305a9a6b477
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
except ImportError:
    print("Please install the required packages.")
    sys.exit()

#Global variables
positionsPoint=[[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]
img=cv2.imread("")
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
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        cWidget = QWidget(self)
        mainLayout = QHBoxLayout()
        
        # || GRAPHICS || - FIRST COLUMN: FOLDER -
        boxFolderLayout = QVBoxLayout()
        folder = QPushButton('Change folder', cWidget)
        folder.clicked.connect(self.changeFolder)
        self.listWidget = QListWidget()
        self.listWidget.setMinimumSize(200,100)
        self.listWidget.currentItemChanged.connect(self.changeImage)
        boxFolderLayout.addWidget(folder)
        boxFolderLayout.addWidget(self.listWidget)
        self.loadImage()
        mainLayout.addLayout(boxFolderLayout)

        # || GRAPHICS || - SECOND COLUMN: IMAGE -
        buttonImageLayout = QVBoxLayout()
        imageLayout = QHBoxLayout()
        od = QPushButton('Optic Disc', cWidget)
        od.clicked.connect(self.opticDisc)
        macula = QPushButton('Macula', cWidget)
        macula.clicked.connect(self.macula)
        vessel = QPushButton('Vessel', cWidget)
        vessel.clicked.connect(self.vessel)
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
        self.prevImageButton.clicked.connect(self.prevImage)
        buttonLayout.addWidget(self.prevImageButton)
        self.nextImageButton = QPushButton('Next image', cWidget)
        self.nextImageButton.clicked.connect(self.nextImage)
        buttonLayout.addWidget(self.nextImageButton)

        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)

    #A new image is displayed when it is selected from the folder files
    def changeImage(self,item):
        global currentAddress, currentImage
        self.checkPrevNextButton()
        currentImage=item.text()
        self.label.setPixmap(QPixmap(currentAddress+"/"+item.text()))

    #The image with the name 'name' is displayed. The image must be present in the folder selected in the folder widget    
    def changeImageTemp(self,name):
        global currentAddress
        self.label.setPixmap(QPixmap(currentAddress+"/"+name))

    #Open Optic Disc
    def opticDisc(self,item):
        self.opticDiscWindow = Prova(currentAddress+"/"+currentImage)
        self.opticDiscWindow.show()

    # Disabled nextImageButton if the selected item is the last one, 
    # disabled prevImageButton if the selected item is the first 
    # and enable both button in the other case
    def checkPrevNextButton(self):
        row=self.listWidget.currentRow()
        if row == 0:
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

class Prova(QMainWindow):
    def __init__(self, file):
        # || GRAPHICS ||
        QMainWindow.__init__(self)   
        cWidget = QWidget(self)
        painter=OpticDisc(file)
        self.setGeometry(10, 10, painter.pixmap.width(), painter.pixmap.height()+50) 
        mainLayout = QVBoxLayout()
        buttonLayout=QHBoxLayout()
        drawEllipse = QPushButton('Draw ellipse', cWidget)
        drawEllipse.clicked.connect(painter.drawEllipse)
        buttonLayout.addWidget(drawEllipse)
        saveAnnotation = QPushButton('Save annotation', cWidget)
        saveAnnotation.clicked.connect(painter.saveAnnotation)
        buttonLayout.addWidget(saveAnnotation)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(painter)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)

class OpticDisc(QWidget):
    def __init__(self, file):
        # || GRAPHICS ||
        self.drawEllipseFlag=False
        QWidget.__init__(self)
        self.pixmap = QPixmap(file) 
        self.file=file   
        self.point=[]

    def paintEvent(self, e):
        self.painter=QPainter(self)
        self.painter.drawPixmap(QRect(0, 0, self.pixmap.width(), self.pixmap.height()), self.pixmap)
        self.pen=QPen()
        self.pen.setWidth(3)
        self.painter.setPen(self.pen)
        if self.drawEllipseFlag == False:
            for pointToDraw in self.point:
                self.painter.drawPoint(pointToDraw[0], pointToDraw[1])
        else:
            ellipse = cv2.fitEllipse(np.asarray(self.point))
            print(ellipse)
            self.painter.drawEllipse(QPoint(ellipse[0][0],ellipse[0][1]),ellipse[1][0]/2,ellipse[1][1]/2)
        self.painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            newPoint=[0,0]
            newPoint[0]=event.pos().x()
            newPoint[1]=event.pos().y()
            self.point.append(newPoint)
            self.update()

    def drawEllipse(self, event):
        print("DRAW")
        ellipse = cv2.fitEllipse(np.asarray(self.point))
        self.drawEllipseFlag=True
        self.update()

    def saveAnnotation(self, event):
        print("SAVE")
        with open ('annotation.csv', mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            textToWrite=self.file+";"
            for i in self.point:
                textToWrite=textToWrite+"("+str(i[0])+","+str(i[1])+"),"
            #textToWrite=textToWrite+";"+ellipse
            employee_writer.writerow(textToWrite)



class Macula(QMainWindow):

    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE - Macula')

class Vessel(QMainWindow):

    def __init__(self):
        # || GRAPHICS ||
        QMainWindow.__init__(self)
        self.setWindowTitle('VAMPIRE - Vessel')

if __name__ == '__main__':
  app = QApplication(sys.argv)
  main = MainWindow()
  main.show()
  sys.exit(app.exec_())