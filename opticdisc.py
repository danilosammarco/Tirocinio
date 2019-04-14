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

    #def wheelEvent(self, event):
    #    print("X")
    #    if event.angleDelta().y() > 0:
    #        #GIU
    #        elf.pixmap=self.pixmap.scaled(int(self.pixmap.width())+1,int(self.pixmap.height())+1,Qt.KeepAspectRatio)
    #    elif event.angleDelta().y() < 0:
    #        #SU
    #        self.pixmap=self.pixmap.scaled(int(self.pixmap.width())-1,int(self.pixmap.height())-1,Qt.KeepAspectRatio)
    #    self.update()

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