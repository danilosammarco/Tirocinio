
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

class OpticDiscWindow(QMainWindow):
    def __init__(self, file):
        # || GRAPHICS ||
        QMainWindow.__init__(self)  
        self.checkEllipse=False 
        cWidget = QWidget(self)
        self.painter=OpticDiscPaint(file)
        self.setGeometry(10, 10, self.painter.pixmap.width()+20, self.painter.pixmap.height()+50+100) 
        mainLayout = QVBoxLayout()
        buttonLayout=QHBoxLayout()
        drawEllipse = QPushButton('Draw ellipse', cWidget)
        drawEllipse.clicked.connect(self.drawEllipse)
        buttonLayout.addWidget(drawEllipse)
        saveAnnotation = QPushButton('Save annotation', cWidget)
        saveAnnotation.clicked.connect(self.saveAnnotation)
        buttonLayout.addWidget(saveAnnotation)
        mainLayout.addLayout(buttonLayout)
        self.instructions=QLabel("Instructions:\n1. You must select at least 5 points\n2. If you want to move an already drawn point click on it. When the point becomes red, click on the new location of the point.\n3. When you have finished selecting the points click on 'Draw ellipse'\n4. If the ellipse meets your criteria, save the annotation with the corresponding button.")
        self.instructions.setFixedHeight(100)
        mainLayout.addWidget(self.painter)
        mainLayout.addWidget(self.instructions)
        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)

    def drawEllipse(self):
        if self.painter.numberOfPoints() > 4:
            self.painter.drawEllipse()
            self.checkEllipse = True
        else:
            msgBox=QMessageBox.warning(None,"WARNING","You must select at least 5 points!")
    def saveAnnotation(self):
        if self.checkEllipse == True:
            self.painter.saveAnnotation
        else:
            msgBox=QMessageBox.warning(None,"WARNING","You must draw the ellipse first!")

class OpticDiscPaint(QWidget):

    def __init__(self, file):
        # || GRAPHICS ||
        self.drawEllipseFlag=False
        QWidget.__init__(self)
        self.pixmap = QPixmap(file) 
        self.file=file   
        self.point=[]
        self.pointToMove=[-1,-1]

    def paintEvent(self, e):
        self.painter=QPainter(self)
        self.painter.drawPixmap(QRect(0, 0, self.pixmap.width(), self.pixmap.height()), self.pixmap)
        self.penBlack=QPen(Qt.black,3)
        self.penGreen=QPen(Qt.green,3)
        self.painter.setPen(self.penBlack)
        if self.drawEllipseFlag == False:
            for pointToDraw in self.point:
                self.painter.drawPoint(pointToDraw[0], pointToDraw[1])
            if self.pointToMove != [-1,-1]:
                self.painter.setPen(self.penGreen)
                self.painter.drawPoint(self.pointToMove[0],self.pointToMove[1])
                self.painter.setPen(self.penBlack)
                self.pointToMove=[-1,-1]
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
            for i in range(-5,5):
                for j in range(-5,5):
                    p=[newPoint[0]+i,newPoint[1]+j]
                    if p in self.point:
                        self.pointToMove=p
            if self.pointToMove == [-1,-1]:
                self.point.append(newPoint)
            else:
                self.point.remove([self.pointToMove[0],self.pointToMove[1]])
            self.update()

    def drawEllipse(self):
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

    def numberOfPoints(self):
        return len(self.point)

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
  #main = StartSession()
  main.show()
  sys.exit(app.exec_())