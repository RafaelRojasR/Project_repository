#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime

#Convertir a datetime y agregar columna antiguedad tienda

def calculate_segmento_tienda_antiguedad(col):
    if np.isnan(col):
        return 0
    elif col > (365*2):
        return 3
    elif col > (365):
        return 2
    else:
        return 1

def colfechas_antiguedad(df):

	df['Fecha Pedido'] = pd.to_datetime(df['Fecha Pedido'], format="%Y/%m/%d")
	df['Fecha Creación Tienda'] = pd.to_datetime(df['Fecha Creación Tienda'], format="%Y/%m/%d")
	df['HoraMovil'] = pd.to_datetime(df['HoraMovil']).dt.hour


#-------------------- NUEVA COLUMNA: Antiguedad tienda  -------------------------------------

	df['Antiguedad Tienda'] = (datetime.now() - df['Fecha Creación Tienda']).dt.days

#-------------------- NUEVA COLUMNA: Segmento antiguedad  -------------------------------------
    
	df['Segmento Antiguedad'] = df['Antiguedad Tienda'].apply(calculate_segmento_tienda_antiguedad)

	return df