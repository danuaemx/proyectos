#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:37:00 2024

@author: daniel
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt 
from PyQt5 import uic

class Vista():
    def __init__(self):
        pass
    def set_control(self,control):
        print('vista-control')
        self.__app = QApplication([])
        self.__window = Qt_ventana(self)
        self.__control = control
        self.__window.iniciar()
        self.__app.exec()
        
    def botones(self,clave):
        return self.__control.botones(clave)
    
    def pagina(self,clave,pagina):
        self.__window.pagina(clave,pagina)
        
    def abrir(self,ruta):
        self.__control.abrir(ruta)
        
    def interpretar(self):
        self.__control.interpretar()
        
class Qt_ventana(QMainWindow):
    def __init__(self,vista):
        self.__paginas = []
        self.__paginas_fase1 = []
        self.__vista = vista
        super(Qt_ventana,self).__init__()
        uic.loadUi('vista/ui/ensamblador.ui',self)
        self.set_act()
        
    def set_act(self):
        #Acciones
        self.actionSalir.triggered.connect(self.close)
        self.actionAbrir.triggered.connect(self.abrir)
        self.actionInterpretar.triggered.connect(self.interpretar)
        self.anterior_c.clicked.connect(lambda: self.botones(1))
        self.siguiente_c.clicked.connect(lambda: self.botones(2))
        self.anterior_f.clicked.connect(lambda: self.botones(3))
        self.siguiente_f.clicked.connect(lambda: self.botones(4))
        self.anterior_s.clicked.connect(lambda: self.botones(5))
        self.siguiente_s.clicked.connect(lambda: self.botones(6))
        self.anterior_cod.clicked.connect(lambda: self.botones(7))
        self.siguiente_cod.clicked.connect(lambda: self.botones(8))
        
        self.actionInterpretar.setEnabled(False)       
        self.anterior_c.setEnabled(False)
        self.siguiente_c.setEnabled(False)
        self.anterior_f.setEnabled(False)
        self.siguiente_f.setEnabled(False)
        self.anterior_s.setEnabled(False)
        self.siguiente_s.setEnabled(False)
        self.anterior_cod.setEnabled(False)
        self.siguiente_cod.setEnabled(False)
        
        
        
        
    def iniciar(self):
        self.show() 
       
        
    def abrir(self):
        self.__archivo = QFileDialog()
        self.__archivo.setFileMode(QFileDialog.ExistingFile)
        self.__archivo.setNameFilter("Todos los archivos (*)")
        if self.__archivo.exec() :
            self.__ruta = self.__archivo.selectedFiles()[0]
            if self.__ruta.endswith('.ens'):

                self.__vista.abrir(self.__ruta)
                self.anterior_c.setEnabled(True)
                self.siguiente_c.setEnabled(True)
                self.actionInterpretar.setEnabled(True)
            else:
                #Abrir mensaje de invalido
                dialogo = QDialog(self)
                dialogo.setWindowTitle('Invalido')
                #Contenido
                label = QLabel(' X Archivo no valido')
                #Agregar contenido
                layout = QVBoxLayout()
                layout.addWidget(label)
                dialogo.setLayout(layout)

                boton_aceptar = QPushButton('Aceptar')
                boton_aceptar.clicked.connect(dialogo.accept)
                layout.addWidget(boton_aceptar)


                #Botones


                dialogo.setFixedSize(200,100)
                dialogo.setModal(True)
                dialogo.exec()

            
    def botones(self,clave):
        self.__vista.botones(clave)
    
    def set_tabla(self,clave,tabla):
        if clave == 1:
            self.tabla_simbolos.clearContents()
            self.tabla_simbolos.setRowCount(len(tabla))
            for reng, (d,s,t,te,v,ta) in enumerate(tabla):
                self.tabla_simbolos.setItem(reng, 0, QTableWidgetItem(str(d)))
                self.tabla_simbolos.setItem(reng, 1, QTableWidgetItem(str(s)))
                self.tabla_simbolos.setItem(reng, 2, QTableWidgetItem(str(t)))
                self.tabla_simbolos.setItem(reng, 3, QTableWidgetItem(str(te)))
                self.tabla_simbolos.setItem(reng, 4, QTableWidgetItem(str(v)))
                self.tabla_simbolos.setItem(reng, 5, QTableWidgetItem(str(ta)))   
        elif clave == 2:
            self.tabla_code.clearContents()
            self.tabla_code.setRowCount(len(tabla))
            for reng, (d,l,co,c) in enumerate(tabla):
                self.tabla_code.setItem(reng, 0, QTableWidgetItem(str(d)))
                self.tabla_code.setItem(reng, 1, QTableWidgetItem(str(l)))
                self.tabla_code.setItem(reng, 2, QTableWidgetItem(str(co)))
                self.tabla_code.setItem(reng, 3, QTableWidgetItem(str(c)))
                
                
    def pagina(self,clave,pagina):
        if clave in (1,2):
            self.contenido.setText(pagina)
        if clave in (3,4):
            self.fase_1.setText(pagina)
        if clave in (5,6):
            self.set_tabla(1,pagina)
        if clave in (7,8):
            self.set_tabla(2,pagina)
    
    def interpretar(self):
        self.__vista.interpretar()
        self.anterior_f.setEnabled(True)
        self.siguiente_f.setEnabled(True)
        self.anterior_s.setEnabled(True)
        self.siguiente_s.setEnabled(True)
        self.anterior_cod.setEnabled(True)
        self.siguiente_cod.setEnabled(True)
        self.tabla_simbolos.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tabla_code.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
