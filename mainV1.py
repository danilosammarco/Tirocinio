#Import
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    import os
    import glob
    import sys
    import numpy as np 
    import cv2
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
        prevImage = QPushButton('Previously image', cWidget)
        buttonLayout.addWidget(prevImage)
        saveImage = QPushButton('Save image', cWidget)
        buttonLayout.addWidget(saveImage)
        saveImage.clicked.connect(saveImageDef)
        nextImage = QPushButton('Next image', cWidget)
        buttonLayout.addWidget(nextImage)

        cWidget.setLayout(mainLayout)
        self.setCentralWidget(cWidget)

    #A new image is displayed when it is selected from the folder files
    def changeImage(self,item):
        global currentAddress, currentImage
        currentImage=item.text()
        self.label.setPixmap(QPixmap(currentAddress+"/"+item.text()))

    #The image with the name 'name' is displayed. The image must be present in the folder selected in the folder widget    
    def changeImageTemp(self,name):
        global currentAddress
        self.label.setPixmap(QPixmap(currentAddress+"/"+name))

    #The opencv process is started for the selection of points and the determination of the ellipse
    def opticDisc(self,item):
        global img, checkDrawEllipse, positionsPoint, currentImage
        img=cv2.imread(currentAddress+"/"+self.listWidget.currentItem().text(),1)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',draw_ellipse)
        while(1):
            cv2.imshow("image",img)
            key = cv2.waitKey(200)
            if key in [27, 1048603]: # ESC key to abort, close window
                cv2.destroyAllWindows()
                break
            if checkDrawEllipse == True:
                self.changeImageTemp(currentImage)
                cv2.destroyAllWindows()
                break
        positionsPoint=[[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]
        checkDrawEllipse = False

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

#Save the edited image temporarily
def saveTempImage():
    global img, checkDrawEllipse, currentImage
    cv2.imwrite(currentAddress+"/def.jpg",img)
    currentImage="def.jpg"
    checkDrawEllipse = True

#To calculate and draw the ellipse around the Optic Disc
def draw_ellipse(event,x,y,flags,param):
    global img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        for i in range(0,len(positionsPoint)):
            if positionsPoint[i]==[-1,-1]:
                positionsPoint[i]=[x,y]
                print(positionsPoint)
                break
        if positionsPoint[len(positionsPoint)-1]!=[-1,-1]:
            ellipse = cv2.fitEllipse(np.asarray(positionsPoint))
            cv2.ellipse(img,ellipse,(0,255,0),2)
            saveTempImage()
    elif event == cv2.EVENT_MOUSEWHEEL or event == cv2.EVENT_MOUSEHWHEEL:
        if flags > 0:
            #Su
            img = cv2.resize(img,None,fx=0.9, fy=0.9, interpolation = cv2.INTER_CUBIC)
        else:
            #Giù
            img = cv2.resize(img,None,fx=1.1, fy=1.1, interpolation = cv2.INTER_CUBIC)

#Save the edited image definitly
def saveImageDef(self):
    global currentAddress, currentImage
    img=cv2.imread(currentAddress+"/def.jpg")
    cv2.imwrite(currentAddress+"/"+currentImage.split(".")[0]+"OpticDisc.jpg",img)
    os.remove(currentAddress+"/def.jpg")

if __name__ == '__main__':
  app = QApplication(sys.argv)
  main = MainWindow()
  main.show()
  sys.exit(app.exec_())