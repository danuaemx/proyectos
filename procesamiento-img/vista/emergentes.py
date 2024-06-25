#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 21:13:26 2024

Clase de emergentes para efectos en la interfaz gráfica.

Este módulo contiene las clases de emergentes utilizadas para aplicar efectos en la interfaz gráfica.
Cada clase de emergente hereda de la clase QDialog de PyQt5 y carga una interfaz de usuario (.ui) correspondiente.

Clases:
- Emergente_efecto: Clase base para los emergentes de efectos. Carga la interfaz de usuario y define los botones aceptar y cancelar.
- Emergente_guardar: Clase de emergente para guardar. Hereda de Emergente_efecto.
- Emergente_HSV: Clase de emergente para el efecto HSV. Hereda de Emergente_efecto.
- Emergente_LAB: Clase de emergente para el efecto LAB. Hereda de Emergente_efecto.
- Emergente_Log: Clase de emergente para el efecto Log. Hereda de Emergente_efecto.
- Emergente_Exp: Clase de emergente para el efecto Exp. Hereda de Emergente_efecto.
"""

from PyQt5.QtWidgets import QDialog, QFileDialog,QLabel, QVBoxLayout, QMainWindow, QAction, QListView, QTreeView, QButtonGroup
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem

class Metadatos(QDialog):
    def __init__(self,window,metadata):
        QDialog.__init__(self)
        uic.loadUi('vista/ui/metadata.ui', self)
        self.__window = window
        self.metadata = metadata
        self.set_metadata()
        self.aceptar.clicked.connect(self.accept)
    def set_metadata(self):
        tag = self.metadata[0]
        des = self.metadata[1]
        self.tabla_metadata.clearContents()
        self.tabla_metadata.setRowCount(len(tag))
        for i in range(len(tag)):
            self.tabla_metadata.setItem(i,0, QTableWidgetItem(str(tag[i])))
            self.tabla_metadata.setItem(i,1, QTableWidgetItem(str(des[i])))
        self.tabla_metadata.resizeColumnsToContents()
        self.tabla_metadata.resizeRowsToContents()
        
class QFileDialogPreview(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QFileDialogPreview, self).__init__(*args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)

        box = QVBoxLayout()

        self.setFixedSize(self.width() + 250, self.height())

        self.mpPreview = QLabel("", self)
        self.mpPreview.setFixedSize(250, 250)
        self.mpPreview.setAlignment(Qt.AlignCenter)
        self.mpPreview.setObjectName("labelPreview")
        box.addWidget(self.mpPreview)

        box.addStretch()

        self.layout().addLayout(box, 1, 3, 1, 1)

        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.onFileSelected)
        self.filesSelected.connect(self.onFilesSelected)

        self._fileSelected = None
        self._filesSelected = None

        # Connect the double click signal to accept the dialog
        for view in self.findChildren(QListView) + self.findChildren(QTreeView):
            view.doubleClicked.connect(self.on_double_click)

    def onChange(self, path):
        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.mpPreview.setText("")
        else:
            self.mpPreview.setPixmap(pixmap.scaled(self.mpPreview.width(), self.mpPreview.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def onFileSelected(self, file):
        self._fileSelected = file

    def onFilesSelected(self):
        self._filesSelected = None

    def getFileSelected(self):
        return self._fileSelected

    def getFilesSelected(self):
        return None

    def on_double_click(self):
        self.accept()

class Emergente_efecto(QDialog):
    def __init__(self,window,nombre):
        """
        Inicializa una instancia de la clase Emergente_efecto.

        Parámetros:
        - window: La ventana principal de la aplicación.
        - nombre: El nombre del archivo de interfaz de usuario (.ui) a cargar.
        """
        QDialog.__init__(self)
        uic.loadUi(f'vista/ui/{nombre}.ui', self)
        self.__window = window
        # Se llama guardar cuando se guarda, pero equivalente en función
        self.aceptar.clicked.connect(self.accept)
        self.cancelar.clicked.connect(self.reject)
        
class Emergente_guardar(Emergente_efecto):
    
    def __init__(self,window):
        """
        Inicializa una instancia de la clase Emergente_guardar.

        Parámetros:
        - window: La ventana principal de la aplicación.
        """
        super().__init__(window,'guardar')
        self.navegar_ruta.clicked.connect(self.abrir_navegador)
        self.cancelar.clicked.connect(self.reject)
        self.aceptar.clicked.connect(self.accept)
        self.formatos = QButtonGroup()

        self.formatos.addButton(self.png)
        self.formatos.addButton(self.jpg)
        self.formatos.addButton(self.jpeg)
        self.formatos.addButton(self.bmp)
        self.formatos.addButton(self.tiff)
        self.formatos.addButton(self.immi)
        self.formatos.setExclusive(True)

        self.colores = QButtonGroup()
        self.colores.addButton(self.rgb)
        self.colores.addButton(self.cmyk)
        self.colores.setExclusive(True)

        self.colores.buttonClicked.connect(self.manejar_formatos)
        self.colores.buttonClicked.connect(self.verificar_seleccion)
        self.formatos.buttonClicked.connect(self.verificar_seleccion)

        
    def abrir_navegador(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Guardar imagen","",
                                                  "Imagenes (*.png *.jpg *.jpeg *.bmp *.tiff *.immi)", 
                                                  options=options)
        if fileName:
            self.ruta_txt.setPlainText(fileName)
            self.aceptar.setEnabled(True)

    def manejar_formatos(self, button):
        """
        Desactiva los formatos de imagen que no sean TIFF cuando se selecciona CMYK.

        Parámetros:
        - button: El botón de opción que fue seleccionado.
        """
        if button == self.cmyk:
            self.png.setEnabled(False)
            self.jpg.setEnabled(False)
            self.jpeg.setEnabled(False)
            self.bmp.setEnabled(False)
            self.immi.setEnabled(False)
            self.tiff.setChecked(True)
        else:
            self.png.setEnabled(True)
            self.jpg.setEnabled(True)
            self.jpeg.setEnabled(True)
            self.bmp.setEnabled(True)
            self.immi.setEnabled(True)
            self.tiff.setEnabled(True)
    
    def verificar_seleccion(self):
        """
        Activa el botón navegar_ruta si hay un modo de color y un formato seleccionados.
        """
        if self.colores.checkedButton() is not None and self.formatos.checkedButton() is not None:
            self.navegar_ruta.setEnabled(True)
        else:
            self.navegar_ruta.setEnabled(False)

    def get_valores(self):
        """
        Obtiene los valores de los controles de la interfaz.

        Retorna:
        Una tupla con la ruta, el formato y el modo de color seleccionados.
        """
        ruta = self.ruta_txt.toPlainText()
        formato = self.formatos.checkedButton().text()
        color = self.colores.checkedButton().text()
        return ruta,formato,color
        
class Emergente_HSV(Emergente_efecto):
    
    def __init__(self,window):
        """
        Inicializa una instancia de la clase Emergente_HSV.

        Parámetros:
        - window: La ventana principal de la aplicación.
        """
        super().__init__(window,'hsv')
    
    def get_valores(self):
        """
        Obtiene los valores de los controles de la interfaz.

        Retorna:
        Una tupla con los valores de h, s y v.
        """
        h = self.h_box.value()
        s = self.s_box.value()
        v = self.i_box.value()
        return h,s,v
        
class Emergente_LAB(Emergente_efecto):
    
    def __init__(self,window):
        """
        Inicializa una instancia de la clase Emergente_LAB.

        Parámetros:
        - window: La ventana principal de la aplicación.
        """
        super().__init__(window,'lab')
        
    def get_valores(self):
        """
        Obtiene los valores de los controles de la interfaz.

        Retorna:
        Una tupla con los valores de l, a y b.
        """
        l = self.l_box.value()
        a = self.a_box.value()
        b = self.b_box.value()
        return l,a,b
        
class Emergente_Log(Emergente_efecto):
    
    def __init__(self,window):
        """
        Inicializa una instancia de la clase Emergente_Log.

        Parámetros:
        - window: La ventana principal de la aplicación.
        """
        super().__init__(window,'log')
    
    def get_valores(self):
        """
        Obtiene los valores de los controles de la interfaz.

        Retorna:
        Una tupla con los valores de c y c_0.
        """
        c = self.const_log.value()
        c_0 = self.origen_log.value()
        return c,c_0
    
class Emergente_Exp(Emergente_efecto):
    
    def __init__(self,window):
        """
        Inicializa una instancia de la clase Emergente_Exp.

        Parámetros:
        - window: La ventana principal de la aplicación.
        """
        super().__init__(window,'exp')
    
    def get_valores(self):
        """
        Obtiene los valores de los controles de la interfaz.

        Retorna:
        Una tupla con los valores de exp, c y c_0.
        """
        exp = self.const_exp.value()
        c = self.const_mul_exp.value()
        c_0 = self.const_org_exp.value()
        return c,exp,c_0

class Emergente_hdr(Emergente_efecto):
    def __init__(self,window):
        
        super().__init__(window,'hdr')
        self.__contador = 0
        self.set_act()
        self.__dict = {1: self.dir_1,
                       2: self.dir_2,
                       3: self.dir_3,
                       4: self.dir_4}
    
    def set_act(self):
        
        self.add.clicked.connect(self.add_dir)
        self.remove.clicked.connect(self.remove_dir)
        self.extra_check.clicked.connect(lambda check: self.extra(check))
        
    
    def add_dir(self):

        dialog =  QFileDialogPreview(self,'Abrir imagen',filter='Imagenes (*.png *.jpg *.jpeg *.bmp *.tiff *.immi)')
        
        if dialog.exec() == QDialog.Accepted:
            ruta = dialog.getFileSelected()
            self.__contador += 1
            self.__dict[self.__contador].setPlainText(ruta)
            
        if self.__contador > 0:
            self.remove.setEnabled(True)
        else:
            self.remove.setEnabled(False)
        
        if self.__contador == 3 and not self.extra_check.isChecked():
            self.aceptar.setEnabled(True)
            self.add.setEnabled(False)
            
        elif self.__contador == 4 and self.extra_check.isChecked():
            self.aceptar.setEnabled(True)
            self.add.setEnabled(False)
        
    def remove_dir(self):
        if self.__contador == 1:
            self.remove.setEnabled(False)
            
        elif self.__contador == 3 and not self.extra_check.isChecked():
            self.aceptar.setEnabled(False)
            self.add.setEnabled(True)
            
        elif self.__contador == 4 and self.extra_check.isChecked():
            self.aceptar.setEnabled(False)
            self.add.setEnabled(True)
        
        self.__dict[self.__contador].setPlainText('')
        self.__contador -= 1
    
    def get_valores(self):
        if self.__contador == 3:
            dir1 = self.__dict[1].toPlainText()
            dir2 = self.__dict[2].toPlainText()
            dir3 = self.__dict[3].toPlainText()
            dir4 = self.__dict[3].toPlainText()
            return dir1,dir2,dir3,dir4
        else:
            dir1 = self.__dict[1].toPlainText()
            dir2 = self.__dict[2].toPlainText()
            dir3 = self.__dict[3].toPlainText()
            dir4 = self.__dict[4].toPlainText()
            return dir1,dir2,dir3,dir4
    
    def extra(self,check):
        if check and self.__contador == 3:

            self.aceptar.setEnabled(False)
            self.add.setEnabled(True)

        elif not check and self.__contador == 4:
            self.remove_dir()

        elif not check and self.__contador == 3:
            self.aceptar.setEnabled(True)
            self.add.setEnabled(False)