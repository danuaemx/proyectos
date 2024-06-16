#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:14:02 2024

@author: daniel
"""
#ES, CS, IP No se consideran

reg_gral_16 = 'AX,BX,CX,DX'.split(',')
reg_gral_8 = 'AH,AL,BH,BL,CH,CL,DH,DL'.split(',')
reg_segmento = 'DS,SS'.split(',')
reg_base = 'BP,SP'.split(',')
reg_index = 'SI,DI'.split(',')
reg_dir = []
reg_dir = reg_base + reg_dir

#Pseudoinstrucciones

ps_seg = '.stack segment,.data segment,.code segment'.split(',')
ps_data = 'db,dw'.split(',')
ps_dir = 'byte,word,ptr'.split(',')

#Instrucciones

inst_0 = 'AAD,AAM,CMPSB,NOP,CMC,POPA'.split(',')
inst_1 =  'JA,JC,JNAE,JNE,JNLE,LOOPE,INC,INT,IDIV,MUL'.split(',')
inst_2 = 'XOR,OR,AND,LEA'.split(',')


