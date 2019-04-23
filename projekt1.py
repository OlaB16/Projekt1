# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit, QGridLayout, QColorDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg 

class Window(QWidget):
    def __init__(self):

        QWidget.__init__(self)
        
        Window.setWindowTitle(self, "Przecięcie odcinków")  # nazwa aplikacji      
        self.rysujbutton = QPushButton('Rysuj', self)       # utworzenie pól
        self.clrChoose = QPushButton('Wybierz kolor', self)
        self.XAlabel = QLabel("XA", self)
        self.XAEdit = QLineEdit()
        self.YAlabel = QLabel("YA", self)
        self.YAEdit = QLineEdit()
        self.XBlabel = QLabel("XB", self)
        self.XBEdit = QLineEdit()
        self.YBlabel = QLabel("YB", self)
        self.YBEdit = QLineEdit()
        self.XClabel = QLabel("XC", self)
        self.XCEdit = QLineEdit()
        self.YClabel = QLabel("YC", self)
        self.YCEdit = QLineEdit()
        self.XDlabel = QLabel("XD", self)
        self.XDEdit = QLineEdit()
        self.YDlabel = QLabel("YD", self)
        self.YDEdit = QLineEdit()
        self.XPlabel = QLabel("XP", self)
        self.XPEdit = QLineEdit()
        self.YPlabel = QLabel("YP", self)
        self.YPEdit = QLineEdit()
        self.punktEdit = QLineEdit()
        self.punktCDAEdit = QLineEdit()
        self.punktCDBEdit = QLineEdit()
        self.sprEdit = QLineEdit()
        
        self.zapisbutton = QPushButton('Zapisz do pliku', self)         # utworzenie przycisków
        self.obliczPbutton = QPushButton('Oblicz punkt przecięcia', self)
        self.cleanbutton = QPushButton('Wyczysc wszystko', self)
        
        self.figure = plt.figure()          
        self.canvas = FigureCanvas(self.figure)
        
        # ladne ustawienie i wysrodkowanie
        layout =  QGridLayout(self)
        
        layout.addWidget(self.XAlabel, 1, 1) 
        layout.addWidget(self.XAEdit, 1, 2)
        layout.addWidget(self.YAlabel, 1, 3)
        layout.addWidget(self.YAEdit, 1, 4)
        layout.addWidget(self.XBlabel, 2, 1)
        layout.addWidget(self.XBEdit, 2, 2)
        layout.addWidget(self.YBlabel, 2, 3)
        layout.addWidget(self.YBEdit, 2, 4)
        layout.addWidget(self.XClabel, 3, 1)
        layout.addWidget(self.XCEdit, 3, 2)
        layout.addWidget(self.YClabel, 3, 3)
        layout.addWidget(self.YCEdit, 3, 4)
        layout.addWidget(self.XDlabel, 4, 1)
        layout.addWidget(self.XDEdit, 4, 2)
        layout.addWidget(self.YDlabel, 4, 3)
        layout.addWidget(self.YDEdit, 4, 4)
        layout.addWidget(self.XPlabel, 7, 1)
        layout.addWidget(self.XPEdit, 7, 2)
        layout.addWidget(self.YPlabel, 7, 3)
        layout.addWidget(self.YPEdit, 7, 4)
        layout.addWidget(self.punktEdit, 8, 2, 1,3)
        layout.addWidget(self.sprEdit, 6 , 2)
        layout.addWidget(self.punktCDAEdit, 5, 2)
        layout.addWidget(self.punktCDBEdit, 5, 4)
        
        layout.addWidget(self.obliczPbutton, 10, 2)
        layout.addWidget(self.rysujbutton, 11, 2)
        layout.addWidget(self.zapisbutton, 10, 4)
        layout.addWidget(self.canvas, 12, 1, 1, -1)
        layout.addWidget(self.clrChoose, 13, 2)
        layout.addWidget(self.cleanbutton, 13, 4)
        self.obliczPbutton.setFixedWidth(200)
        self.zapisbutton.setFixedWidth(200)
        
        # połączenie przycisku (signal) z akcją (slot)
        self.rysujbutton.clicked.connect(self.handleButton)
        self.clrChoose.clicked.connect(self.clrChooseF)
        self.zapisbutton.clicked.connect(self.zapisz)
        self.obliczPbutton.clicked.connect(self.oblicz)
        self.cleanbutton.clicked.connect(self.cleanall)
        
    # sprawdzenie czy podana wartosć jest liczbą i zamiana jej na float
    def chceckValues(self, lineE):
        if lineE.text().lstrip("-").replace('.', '').isdigit():
            return float(lineE.text())
        else:
            return None

    def oblicz(self):
        XA = self.chceckValues(self.XAEdit) 
        YA = self.chceckValues(self.YAEdit)
        XB = self.chceckValues(self.XBEdit)
        YB = self.chceckValues(self.YBEdit)
        XC = self.chceckValues(self.XCEdit)
        YC = self.chceckValues(self.YCEdit)
        XD = self.chceckValues(self.XDEdit)
        YD = self.chceckValues(self.YDEdit)
        
        if XA!=None and YA!=None and XB!=None and YB!=None and XC!=None and YC!=None and XD!=None and YD!=None:
            
            CDA=np.array([[XC,YC,1],[XD,YD,1],[XA,YA,1]])  # sprawdzenie położenia punktu A względem odcinka CD
            wyznacznikCDA=np.linalg.det(CDA)
            if wyznacznikCDA>0:
                self.punktCDAEdit.setText("Punkt A leży po prawej stronie CD")
            elif wyznacznikCDA<0:
                self.punktCDAEdit.setText("Punkt A leży po lewej stronie CD")
            else:
                self.punktCDAEdit.setText("Punkty A, C, D są współliniowe")
            
            CDB=np.array([[XC,YC,1],[XD,YD,1],[XB,YB,1]])   # sprawdzenie położenia punktu B względem odcinka CD
            wyznacznikCDB=np.linalg.det(CDB)
            if wyznacznikCDB>0:
                self.punktCDBEdit.setText("Punkt B leży po prawej stronie CD")
            elif wyznacznikCDB<0:
                self.punktCDBEdit.setText("Punkt B leży po lewej stronie CD")
            else:
                self.punktCDBEdit.setText("Punkty B, C, D są współliniowe")
            
            if abs(wyznacznikCDA-wyznacznikCDB)<0.000000001:    # sprawdzenie czy odcinki się przecinają za pomocą wyznaczników (warunek <0.000000001 wynika z niestosowania przybliżeń i zaokrągleń)
                self.sprEdit.setText('Odcinki nie przecinają się')
            else:
                self.sprEdit.setText('Odcinki przecinają się')
            
            # obliczenie współrzędnych punktu P
            dx_AB=XB-XA
            dy_AB=YB-YA
            dx_CD=XD-XC
            dy_CD=YD-YC
            dx_AC=XC-XA
            dy_AC=YC-YA

            t1=((dx_AC*dy_CD)-(dy_AC*dx_CD))/((dx_AB*dy_CD)-(dy_AB*dx_CD))
            t2=((dx_AC*dy_AB)-(dy_AC*dx_AB))/((dx_AB*dy_CD)-(dy_AB*dx_CD))

            if 0<=t1 and t1<=1 and 0<=t2 and t2<=1:             # sprawdzenie gdzie jest położony punkt P
                self.punktEdit.setText('Punkt P należy do obu odcinków')
            elif t1==0:
                self.punktEdit.setText('Punkt P znajduje się w punkcie A')
            elif t1==1:
                self.punktEdit.setText('Punkt P znajduje się w punkcie B')
            elif t2==0:
                self.punktEdit.setText('Punkt P znajduje się w punkcie C')
            elif t2==1:
                self.punktEdit.setText('Punkt P znajduje się w punkcie D') 
            else:
                self.punktEdit.setText('Punkt P znajduje się na przedłużeniu odcinka/odcinków')
            
            XP=XA+t1*dx_AB
            YP=YA+t1*dy_AB
            
            self.XPEdit.setText(str("{:.3f}".format(XP)))       # wyswietlenie obliczonych współrzędnych punktu P z odpowiednią dokładnoscią
            self.YPEdit.setText(str("{:.3f}".format(YP)))
        else:
            msg_err=QMessageBox()       # komunikat w przypadku błędnie wpisanych danych lub ich nie wpisanie
            msg_err.setWindowTitle('Komunikat')
            msg_err.setStandardButtons(QMessageBox.Ok)
            msg_err.setText('Podane współrzędne są niepoprawne')
            msg_err.exec_()

    def rysuj(self, clr='g'):
        XA = self.chceckValues(self.XAEdit)
        YA = self.chceckValues(self.YAEdit)
        XB = self.chceckValues(self.XBEdit)
        YB = self.chceckValues(self.YBEdit)
        XC = self.chceckValues(self.XCEdit)
        YC = self.chceckValues(self.YCEdit)
        XD = self.chceckValues(self.XDEdit)
        YD = self.chceckValues(self.YDEdit)
        XP = self.XPEdit
        YP = self.YPEdit
        XP = self.chceckValues(self.XPEdit)
        YP = self.chceckValues(self.YPEdit)
        
        if XA!=None and YA!=None and XB!=None and YB!=None and XC!=None and YC!=None and XD!=None and YD!=None:
            if XP!=None and YP!=None:   # rysowanie odcinków wraz z istniejącym punktem P
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot((XA, XB),(YA, YB),color=clr)    # rysowanie odcinka
                ax.plot((XC, XD),(YC, YD),color=clr)
                ax.plot((XA,XP),(YA,YP),'--',color=clr)  # rysowanie linii przerywanej w przypadku gdy punkt P znajduję się na przedłużeniu odcinka
                ax.plot((XC,XP),(YC,YP),'--',color=clr)
                ax.plot(XP,YP,color=clr,marker='o')     # zaznaczenie punktu kółeczkiem
                ax.plot(XA,YA,color=clr,marker='o')
                ax.plot(XB,YB,color=clr,marker='o')
                ax.plot(XC,YC,color=clr,marker='o')
                ax.plot(XD,YD,color=clr,marker='o')
                ax.text(XA,YA, u"A \n")                 # wyswitlenie opisu punktu
                ax.text(XA, YA, '({:.3f}, {:.3f})'.format(XA, YA))   # wyswietlenie współrzędnych punktu             
                ax.text(XB,YB, u"B \n")
                ax.text(XB, YB, '({:.3f}, {:.3f})'.format(XB, YB))
                ax.text(XC,YC, u"C \n")
                ax.text(XC, YC, '({:.3f}, {:.3f})'.format(XC, YC))
                ax.text(XD,YD, u"D \n")
                ax.text(XD, YD, '({:.3f}, {:.3f})'.format(XD, YD))
                ax.text(XP,YP, u"P \n")
                ax.text(XP, YP, '({:.3f}, {:.3f})'.format(XP, YP))
                self.canvas.draw()
            else:       # rysowanie odcinków w przypadku gdy nie istnieje punkt P
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot((XA, XB),(YA, YB),color=clr)    # rysowanie odcinka
                ax.plot((XC, XD),(YC, YD),color=clr)
                ax.plot(XA,YA,color=clr,marker='o')     # zaznaczenie punktu kółeczkiem
                ax.plot(XB,YB,color=clr,marker='o')
                ax.plot(XC,YC,color=clr,marker='o')
                ax.plot(XD,YD,color=clr,marker='o')
                ax.text(XA,YA, u"A \n")             # wyswitlenie opisu punktu
                ax.text(XA, YA, '({:.3f}, {:.3f})'.format(XA, YA))     # wyswietlenie współrzędnych punktu           
                ax.text(XB,YB, u"B \n")
                ax.text(XB, YB, '({:.3f}, {:.3f})'.format(XB, YB))
                ax.text(XC,YC, u"C \n")
                ax.text(XC, YC, '({:.3f}, {:.3f})'.format(XC, YC))
                ax.text(XD,YD, u"D \n")
                ax.text(XD, YD, '({:.3f}, {:.3f})'.format(XD, YD))
                self.canvas.draw()
        else:
            msg_err=QMessageBox()
            msg_err.setWindowTitle('Komunikat')
            msg_err.setStandardButtons(QMessageBox.Ok)
            msg_err.setText('Podane współrzędne są niepoprawne')
            msg_err.exec_()
            self.figure.clear()
            self.canvas.clear()

    def handleButton(self):
        self.rysuj()
           
    def zapisz(self):
        XP=self.XPEdit
        YP=self.YPEdit
        XP = self.chceckValues(self.XPEdit)
        YP = self.chceckValues(self.YPEdit)
        if  XP!=None and YP!=None:
            plik=open('wyniki.txt','a') # zapis do pliku
            plik.write("Współrzędne punktu przecięcia") 
            plik.write("\n| {:^10} | {:^10} |\n".format('X', 'Y'))   # utworzenie górnej częsci tabeli
            plik.write("| {:^10.3f} | {:^10.3f} |".format(XP,YP))   # zapis wartosci z odpowiednią dokładnoscią przy pomocy funkcji format
        else:
            plik=open('wyniki.txt','a') # zapis do pliku
            plik.write("Współrzędne punktu przecięcia") 
            plik.write("\n| {:^10} | {:^10} |\n".format('X', 'Y'))   # utworzenie górnej częsci tabeli
            plik.write("| {:^23} |".format('punkt nie istnieje'))

    def clrChooseF(self):
        color=QColorDialog.getColor()
        if color.isValid():
            self.rysuj(color.name())
        else:
            pass
    
    def cleanall(self):
        self.XAEdit.clear() # wyczyszczenie każdego z pól
        self.YAEdit.clear()
        self.XBEdit.clear()
        self.YBEdit.clear()
        self.XCEdit.clear()
        self.YCEdit.clear()
        self.XDEdit.clear()
        self.YDEdit.clear()
        self.XPEdit.clear()
        self.YPEdit.clear()
        self.punktEdit.clear()
        self.punktCDAEdit.clear()
        self.punktCDBEdit.clear()
        self.sprEdit.clear()
    
if __name__ == '__main__':
    if not QApplication.instance():
        app=QApplication(sys.argv)
    else:
        app=QApplication.instance()
    window = Window()
    window.show()
    sys.exit(app.exec_())