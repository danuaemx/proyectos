#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 21:16:07 2024

@author: daniel
"""
from PyQt5.QtWidgets import QMainWindow,QDialog,QColorDialog, QMessageBox
from PyQt5 import uic
from .emergentes  import Emergente_Exp,Emergente_Log,Emergente_guardar,Emergente_hdr,Emergente_hdr, QFileDialogPreview,Metadatos
import pyqtgraph as pg
import numpy as np

class Qt_ventana(QMainWindow):
    def __init__(self,vista):
        self.__vista = vista
        QMainWindow.__init__(self)
        uic.loadUi('vista/ui/vista1.ui',self)
        self._l = False
        self.set_act()
        
    def set_act(self):
        #Ocultar docks
        self.dock_herramientas.hide()
        self.dock_hist.hide()
        #Configurar vista con Image View
        self.visor = pg.ImageView()
        self.box = pg.ViewBox()

        self.grafico = pg.PlotItem(viewBox=self.box,
                                   enableMenu=False)
        self.grafico.getViewBox().setLimits(xMin=-50,
                                            yMin=-50)
        self.visor = pg.ImageView(view=self.grafico, levelMode='rgba')
        self.visor.ui.graphicsView.setBackground((30,30,30))
        

        #Ocultar histograma por defecto
        self.visor.ui.histogram.hide()
        #Configurar histograma hotizontal
        self.histograma = pg.HistogramLUTWidget(image=self.visor.imageItem,
                                                        fillHistogram=True,
                                                          levelMode='rgba',
                                                            gradientPosition='bottom',
                                                              orientation='horizontal')
        self.histograma.setBackground((30, 30, 30))
        #Insertar histograma
        self.visor.ui.histogram= self.histograma
        self.l_hist.addWidget(self.visor.ui.histogram)
        self.layout_vista.addWidget(self.visor)
        #Oculta partes no usadas
        self.visor.ui.roiBtn.hide()
        self.visor.ui.menuBtn.hide()
     
        #Acciones barra
        self.actionAbrirH.triggered.connect(self.abrir)
        self.actionGuardarH.triggered.connect(self.guardar)
        self.actionSalirH.triggered.connect(self.close_el)
        self.actionDeshacerH.triggered.connect(lambda:self.filtro('deshacer'))
        self.actionRehacerH.triggered.connect(lambda:self.filtro('rehacer'))
        self.actionMetadataH.triggered.connect(self.__vista.get_metadata)

        #Shortucts
        self.actionAbrirH.setShortcut('Ctrl+A')
        self.actionGuardarH.setShortcut('Ctrl+G')
        self.actionSalirH.setShortcut('Ctrl+Q')
        self.actionDeshacerH.setShortcut('Ctrl+Z')
        self.actionRehacerH.setShortcut('Ctrl+Y')

       
        #Se eliminan para evitar errores y se van a avanzados
        #self.actionModo_L.triggered.connect(self.modo_L)
        #self.actionAdd_Color.triggered.connect(self.mapear)
        
        #Posición Espacial
        self.espejo_h.clicked.connect(lambda:self.filtro('espejo_h'))
        self.espejo_v.clicked.connect(lambda:self.filtro('espejo_v'))
        self.rotar90.clicked.connect(lambda:self.filtro('rotar90'))
        self.rotar90neg.clicked.connect(lambda:self.filtro('rotar90neg'))
        self.roi_bt.clicked.connect(self.roi_swt)
        self.copiar_roi_bt.clicked.connect(lambda: self.cp_swt('copiar'))
        self.pegar_roi_bt.clicked.connect(lambda: self.cp_swt('pegar'))
        self.eliminar_roi_bt.clicked.connect(lambda: self.cp_swt('eliminar'))
        self.aplicar_redim.clicked.connect(lambda:self.filtro_arg('redim',
                                                                  (self.sp_ancho_redim.value(),
                                                                    self.sp_alto_redim.value())))
        self.aplicar_crop.clicked.connect(lambda:self.filtro_arg('crop_rect',
                                                                (self.x1_esq.value(),
                                                                self.y1_esq.value(),
                                                                self.x2_esq.value(),
                                                                self.y2_esq.value())))
        #Spinnners
        self.sp_alto_redim.valueChanged.connect(lambda:self.redim('alto'))
        self.sp_ancho_redim.valueChanged.connect(lambda:self.redim('ancho'))
        self.x1_esq.valueChanged.connect(lambda:self.crop('x1'))
        self.y1_esq.valueChanged.connect(lambda:self.crop('y1'))
        self.x2_esq.valueChanged.connect(lambda:self.crop('x2'))
        self.y2_esq.valueChanged.connect(lambda:self.crop('y2'))
        #Frecuencia
        self.promedio_f.clicked.connect(lambda:self.filtro('promedio_f'))
        self.centrar.clicked.connect(lambda:self.filtro('centrar_f'))
        self.ecualizar.clicked.connect(lambda:self.filtro('ecualizar'))
        self.aplicar_del_ran.clicked.connect(lambda:self.filtro_arg('del_ran_hist',
                                                                        (self.sp_r_min.value(),
                                                                        self.sp_r_max.value())))
        self.aplicar_comp_exp.clicked.connect(lambda:self.filtro_arg('com_exp',
                                                                    (self.sp_ce_min.value(),
                                                                    self.sp_ce_max.value())))
        
        self.aplicar_crop_sel.clicked.connect(lambda:self.filtro_arg('cp_sel_hist',
                                                                    (self.sp_x1_ch.value(),
                                                                    self.sp_x2_ch.value(),
                                                                    self.sp_n1_ch.value(),
                                                                    self.sp_n2_ch.value())))
        
        #Spinners
        self.sp_r_max.valueChanged.connect(lambda:self.del_rango_hist('max'))
        self.sp_r_min.valueChanged.connect(lambda:self.del_rango_hist('min'))
        self.sp_ce_max.valueChanged.connect(lambda:self.exp_comp_r_hist('max'))
        self.sp_ce_min.valueChanged.connect(lambda:self.exp_comp_r_hist('min'))
        self.sp_x1_ch.valueChanged.connect(lambda:self.cp_hist('x1'))
        self.sp_x2_ch.valueChanged.connect(lambda:self.cp_hist('x2'))
        self.sp_n1_ch.valueChanged.connect(lambda:self.cp_hist('n1'))
        self.sp_n2_ch.valueChanged.connect(lambda:self.cp_hist('n2'))

        
        #Filtros Mask
        self.promedio_ms.clicked.connect(lambda:self.filtro('promedio'))
        self.blur_ms.clicked.connect(lambda:self.filtro('blur'))
        self.definir_ms.clicked.connect(lambda:self.filtro('definir'))
        self.borde_ms.clicked.connect(lambda:self.filtro('borde'))
        self.nitidez_ms.clicked.connect(lambda:self.filtro('nitidez'))
        self.relieve_ms.clicked.connect(lambda:self.filtro('relieve'))
        self.nitidez_1_ms.clicked.connect(lambda:self.filtro('nitidezl'))
        self.def_r_ms.clicked.connect(lambda:self.filtro('definir1'))
        
        #Color
        self.brillo_neg.clicked.connect(lambda:self.filtro_arg('brillo',
                                                               -1*int(self.sp_brillo.value())))
        
        self.brillo_pos.clicked.connect(lambda:self.filtro_arg('brillo',
                                                               int(self.sp_brillo.value())))
        
        self.contraste_mul.clicked.connect(lambda:self.filtro_arg('contraste',
                                                                self.contraste_sp.value()/100))
        
        self.hue_neg.clicked.connect(lambda:self.filtro_arg('hue',
                                                            [-1*int(self.sp_hue.value()),
                                                            1,
                                                            1]))
        
        self.hue_pos.clicked.connect(lambda:self.filtro_arg('hue',
                                                            [int(self.sp_hue.value()),
                                                            1,
                                                            1]))

        self.sat_pos.clicked.connect(lambda:self.filtro_arg('sat',
                                                            (0,
                                                             float(self.sp_sat.value()/100),
                                                             1)))
        
        
        self.inten_pos.clicked.connect(lambda:self.filtro_arg('val',
                                                            (0,
                                                             1,
                                                             float(self.sp_inten.value()/100))))
                                        
        self.lum_neg.clicked.connect(lambda:self.filtro_arg('lum',
                                                            (-1*int(self.sp_lum.value()),
                                                             0,
                                                             0)))
        self.lum_pos.clicked.connect(lambda:self.filtro_arg('lum',
                                                            (int(self.sp_lum.value()),
                                                             0,
                                                             0)))
        self.a_neg.clicked.connect(lambda:self.filtro_arg('a',
                                                          (0,
                                                          0,
                                                          -1*int(self.sp_a.value()))))
        self.a_pos.clicked.connect(lambda:self.filtro_arg('a',
                                                          (0,
                                                          0,
                                                          int(self.sp_a.value()))))
        self.b_neg.clicked.connect(lambda:self.filtro_arg('b',
                                                         (0,
                                                          -1*int(self.sp_b.value()),
                                                          0)))
        self.b_pos.clicked.connect(lambda:self.filtro_arg('b',
                                                          (0,
                                                          int(self.sp_b.value()),
                                                          0)))

        self.sepia1.clicked.connect(lambda:self.filtro('sepia1'))
        self.sepia2.clicked.connect(lambda:self.filtro('sepia2'))
        self.sepia3.clicked.connect(lambda:self.filtro('sepia3'))
        self.negativo.clicked.connect(lambda:self.filtro('negativo'))
        self.loga.clicked.connect(lambda: self.filtro_emergente('log',Emergente_Log))
        self.expo.clicked.connect(lambda: self.filtro_emergente('exponencial',Emergente_Exp))
        
        self.acept_tr.clicked.connect(self.transformar_custom)
        self.acept_mask.clicked.connect(self.mascara_custom)
        #Ruido
        self.fft_reconstruir_r.clicked.connect(lambda:self.filtro('ruido_fft2_95'))
        self.fft90_r.clicked.connect(lambda:self.filtro('ruido_fft2_90'))
        self.gauss_s_r.clicked.connect(lambda:self.filtro('gaussian_4'))
        self.gauss_c_r.clicked.connect(lambda:self.filtro('gaussian_9'))
        self.bilateral_r.clicked.connect(lambda:self.filtro('bilaterals'))
        self.bil_com_r.clicked.connect(lambda:self.filtro('bilateralc'))
        self.aplicar_fft.clicked.connect(lambda:self.filtro_arg('ruido_fft2',self.sp_fft.value()))
        self.aplicar_bilateral.clicked.connect(lambda:self.filtro_arg('bilateral_custom',
                                                                      (self.sp_suav.value(),
                                                                       self.sp_bord.value())))
        self.mediana_r.clicked.connect(lambda:self.filtro('mediana'))
        self.mediana_amplio_r.clicked.connect(lambda:self.filtro('mediana_amplio'))
        
        #Morfoloógicos
        self.erode_morf.clicked.connect(lambda:self.filtro('erode'))
        self.dilate_morf.clicked.connect(lambda:self.filtro('dilate'))
        self.open_morf.clicked.connect(lambda:self.filtro('open'))
        self.close_morf.clicked.connect(lambda:self.filtro('close'))
        self.grad_morf.clicked.connect(lambda:self.filtro('grad_morf'))
        self.grad_neg_morf.clicked.connect(lambda:self.filtro('grad_neg_morf'))
        self.close_open_morf.clicked.connect(lambda:self.filtro('close_open_morf'))
        self.open_close_morf.clicked.connect(lambda:self.filtro('open_close_morf'))
        #Avanzados
        self.hdr_r_a.clicked.connect(lambda:self.filtro_emergente('hdr',Emergente_hdr))
        self.bill_gauss.clicked.connect(lambda:self.filtro('bilateral402'))
        self.eliminar_rostro.clicked.connect(self.del_rostro)
        self.aceptar_del_rostro.clicked.connect(self.aplicar_del_rostro)
        self.reconst.clicked.connect(lambda:self.filtro('reconst_ruido'))
        self.ruido_noct.clicked.connect(lambda:self.filtro('ruido_nocturno'))
        self.grises_bt.clicked.connect(self.modo_L)
        self.add_cl.clicked.connect(self.mapear)
        self.cancelar_gris_bt.clicked.connect(self.cancelar_gris)

    def iniciar(self):
        self.show()
    
    def desplegar(self,array):
        
        self.__actual = array
        if len(array.shape)==3:
            self.x,self.y,_ = array.shape
        else:
            self.x,self.y = array.shape
        #La misma posición anterior
        self.visor.setImage(self.__actual,autoRange = False,autoLevels = True)
        self.histograma.setLevels(rgba = [(0,255),(0,255),(0,255)])
        self.grafico.getViewBox().setLimits(xMin=-50,
                                            yMin=-50,
                                            xMax=self.x+50,
                                            yMax=self.y+50)
        
    def abrir(self):
       dialog =  QFileDialogPreview(self,'Abrir imagen',filter='Imagenes (*.png *.jpg *.jpeg *.bmp *.tiff *.immi)')
       if dialog.exec() == QDialog.Accepted:
           path = dialog.selectedFiles()
           self.__vista.abrir(path[0])
           #Set autoRange = True
           self.visor.setImage(self.__actual,autoRange = True,autoLevels = False)
           self.dock_herramientas.show()
           self.dock_hist.show()
           self.actionAbrirH.setEnabled(True)
           self.actionGuardarH.setEnabled(True)
           self.actionMetadataH.setEnabled(True)
           self.actionDeshacerH.setEnabled(True)
           self.actionRehacerH.setEnabled(True)

    def desp_metadata(self,metadata):
        dialog = Metadatos(self,metadata)
        result = dialog.exec()
    
    def guardar(self):
        dialogo = Emergente_guardar(self)
        result = dialogo.exec()
        if result == QDialog.Accepted:
            valores = dialogo.get_valores()
            try:
                self.__vista.filtro_valores('guardar',valores)
            except Exception as e:
                self.error('guardar',e)
    
    def filtro(self,clave):
        self.__vista.filtro(clave)
    
    def filtro_arg(self,clave,args):
        self.__vista.filtro_valores(clave,args)
    
    def filtro_emergente(self,clave,ventana):
        dialogo = ventana(self)
        if dialogo.exec() == QDialog.Accepted:
            values = dialogo.get_valores()
            self.__vista.filtro_valores(clave,values)
            self.visor.ui.histogram.setLevelMode('rgba')
            self.actionAdd_Color.setEnabled(False)
            self.actionModo_L.setChecked(False)        
        
    def close_el(self):
       self.__vista.eliminar()
       self.close()
    
    def cp_swt(self,clave):
        if clave == 'copiar':
            #Pendiente, multiples copias
            self.pegar_roi_bt.setEnabled(True)
            #self.actionCopiar.setEnabled(False)
            self.roi_org_0 = np.array(self.roi.state['pos'])
            self.roi_size_0 = np.array(self.roi.state['size'])

        elif clave == 'eliminar':
            roi_org_1 = np.array(self.roi.state['pos'])
            roi_size_1= np.array(self.roi.state['size'])
            valores = roi_org_1,roi_size_1
            self.__vista.filtro_valores('eliminar_roi',valores)
            
        else:
            #No requerido debido a que no es exclusivo
            #self.actionPegar.setEnabled(False)
            #self.actionCopiar.setEnabled(True)
            valores = self.roi_org_0,self.roi_size_0,np.array(self.roi.state['pos'])
            self.__vista.filtro_valores('cop',valores)
              
    def roi_swt(self,checked):
        #Se activa roi y se crea
        if checked:
            #Se activa copiar
            self.copiar_roi_bt.setEnabled(True)
            self.eliminar_roi_bt.setEnabled(True)
            #Se obtiene la posición de la imagen
            a_0 = self.visor.getView().viewRect()
            a = a_0.center()
            self.roi = pg.CircleROI([a.x()-a_0.height()/2,a.y()-a_0.height()/2], 
                                       [round(a_0.height()),
                                        round(a_0.height())], 
                                       pen='r')
            self.visor.addItem(self.roi)
        #Se desactiva roi
        elif self.roi is not None:
            self.visor.removeItem(self.roi)
            self.roi = None
            self.copiar_roi_bt.setEnabled(False)
            self.pegar_roi_bt.setEnabled(False)
            self.eliminar_roi_bt.setEnabled(False)

        #Se desactiva copiar y pegar, y eliminar
        else:
            self.copiar_roi_bt.setEnabled(False)
            self.pegar_roi_bt.setEnabled(False)
            self.eliminar_roi_bt.setEnabled(False)
    
    def del_rostro(self,checked):
        if checked:
            # Se activa aceptar
            self.aceptar_del_rostro.setEnabled(True)
            # Se obtiene la posición de la imagen
            a_0 = self.visor.getView().viewRect()
            a = a_0.center()

            # Crear un punto en lugar de un CircleROI
            self.punto = pg.ROI([a.x(), a.y()], size=[6, 6])
            self.punto.addTranslateHandle([0.5, 0.5])
            self.punto.setPen(pg.mkPen('r', width=8))
            self.visor.addItem(self.punto)
        elif self.punto is not None:
            self.visor.removeItem(self.punto)
            self.punto = None
            self.aceptar_del_rostro.setEnabled(False)

        else:
            self.aceptar_del_rostro.setEnabled(False)
    
    def aplicar_del_rostro(self):
        if self.punto is not None:
            pos = self.punto.pos()
            valores = [round(pos.x())+3,round(pos.y()+3)]
            self.__vista.filtro_valores('del_rostro',valores)

    
    def redim(self,clave):
        if self.block_ratio.isChecked():
            if clave == 'alto':
                r = round(self.sp_alto_redim.value()*self.x/self.y)
                self.sp_ancho_redim.setValue(r)
            else:
                r = round(self.sp_ancho_redim.value()*self.y/self.x)
                self.sp_alto_redim.setValue(r)
    
    def crop(self,clave):
        x,y,_ = self.__actual.shape
        self.x1_esq.setMaximum(x-1)
        self.y1_esq.setMaximum(y-1)
        self.x2_esq.setMaximum(x)
        self.y2_esq.setMaximum(y)
        if clave == 'x1':
            self.x2_esq.setMinimum(self.x1_esq.value()+1)
        if clave == 'y1':
            self.y2_esq.setMinimum(self.y1_esq.value()+1)
        if clave == 'x2':
            self.x1_esq.setMaximum(self.x2_esq.value()-1)
        if clave == 'y2':
            self.y1_esq.setMaximum(self.y2_esq.value()-1)
    
    def del_rango_hist(self,clave):
        if clave == 'max':
            self.sp_r_min.setMaximum(self.sp_r_max.value()-1)
        if clave == 'min':
            self.sp_r_max.setMinimum(self.sp_r_min.value()+1)
    
    def exp_comp_r_hist(self,clave):
        if clave == 'max':
            self.sp_ce_min.setMaximum(self.sp_ce_max.value()-1)
        if clave == 'min':
            self.sp_ce_max.setMinimum(self.sp_ce_min.value()+1)
    
    def cp_hist(self,clave):
        if clave == 'x1':
            self.sp_x2_ch.setMinimum(self.sp_x1_ch.value()+1)
        if clave == 'x2':
            self.sp_x1_ch.setMaximum(self.sp_x2_ch.value()-1)
        if clave == 'n1':
            self.sp_n2_ch.setMinimum(self.sp_n1_ch.value()+1)
        if clave == 'n2':
            self.sp_n1_ch.setMaximum(self.sp_n2_ch.value()-1)


    #Se desactivan todas las opciones de la barra de herramientas
    def modo_L(self,checked):
        if checked:
            #Desvanecer menus y barra
            self.dock_herramientas.hide()
            self.barra_herr.hide()
            self.cancelar_gris_bt.setEnabled(True)
            self.visor.ui.histogram.setLevelMode('mono')
            self.__vista.filtro_valores('modo_L','')
            self.add_cl.setEnabled(True)
            self.__mapeador = [(0,0,0),(127,127,127),(255,255,255)]
            cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, len(self.__mapeador)), color=self.__mapeador)
            self.visor.setColorMap(cmap)
            
        else:
            self.dock_herramientas.show()
            self.barra_herr.show()
            self.visor.ui.histogram.gradient.setColorMode('rgb')
            #Complicado de encontrar
            cmap = self.visor.ui.histogram.gradient.colorMap()
            # ---- ---- ----
            img = np.clip(self.__actual,0,256).astype(np.uint8)
            # Con valores de 0 a 1
            imgm = cmap.map(img/255,'float')
            # Ajustar de 0 a 255
            imgm = np.clip(imgm*255,0,255).astype(np.uint8)
            # Quitar el canal alfa
            imgm = imgm[:,:,:-1]
            #Cambiar a modo RGB
            self.__vista.filtro_valores('modo_L',imgm)
            self.visor.ui.histogram.setLevelMode('rgba')
            self.add_cl.setEnabled(False)
            self.cancelar_gris_bt.setEnabled(False)
    
    def cancelar_gris(self):
        #Desactivar modo gris
        self.actionModo_L.setChecked(False)
        self.add_cl.setEnabled(False)
        self.cancelar_gris_bt.setEnabled(False)
        img = np.clip(self.visor.getProcessedImage(),0,256).astype(np.uint8)
        imgm = np.stack([img,img,img],axis=2)
        self.__vista.filtro_valores('modo_L',imgm)
        self.visor.ui.histogram.setLevelMode('rgba')
        self.dock_herramientas.show()
        self.barra_herr.show()
        self.actionAdd_Color.setEnabled(False)
        self.grises_bt.setChecked(False)
        self.__vista.filtro('deshacer')
        self.__vista.filtro('deshacer')
            
    def mapear(self):
        color = QColorDialog.getColor() 
        if color.isValid():
        # Convertir el color a formato RGB
            r, g, b, _ = color.getRgb()
            self.__mapeador.append((r,g,b))
            cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, len(self.__mapeador)), color=self.__mapeador)
            self.visor.setColorMap(cmap)
    
    def error(self,clave,error):
        q = QMessageBox(self)
        q.setIcon(QMessageBox.Critical)
        q.setWindowTitle('Error')
        q.setText(f'{clave}\n{str(error)[0:100]}')
        q.exec()

    def transformar_custom(self):
        matriz = np.zeros((3,3))

        matriz[0,0] = self.sp_tr_00.value()
        matriz[0,1] = self.sp_tr_01.value()
        matriz[0,2] = self.sp_tr_02.value()
        matriz[1,0] = self.sp_tr_10.value()
        matriz[1,1] = self.sp_tr_11.value()
        matriz[1,2] = self.sp_tr_12.value()
        matriz[2,0] = self.sp_tr_20.value()
        matriz[2,1] = self.sp_tr_21.value()
        matriz[2,2] = self.sp_tr_22.value()

        # Enviar el estado booleano del QCheckBox llamado n_tr
        norm = self.n_tr.isChecked()
        valores = norm,matriz.astype(np.float32)

        self.__vista.filtro_valores('transf_custom',valores)
    
    def mascara_custom(self):
        matriz =  np.zeros((3,3))

        matriz[0,0] = self.sp_ms_00.value()
        matriz[0,1] = self.sp_ms_01.value()
        matriz[0,2] = self.sp_ms_02.value()
        matriz[1,0] = self.sp_ms_10.value()
        matriz[1,1] = self.sp_ms_11.value()
        matriz[1,2] = self.sp_ms_12.value()
        matriz[2,0] = self.sp_ms_20.value()
        matriz[2,1] = self.sp_ms_21.value()
        matriz[2,2] = self.sp_ms_22.value()

        norm = self.n_mask.isChecked()
        valores = norm,matriz.astype(np.float32)

        self.__vista.filtro_valores('mask_custom',valores)