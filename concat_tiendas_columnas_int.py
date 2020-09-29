import numpy as np
import pandas as pd

def load_dataframes():
	# It is necessary to put all raw files on a direcory called /new_data
	file_names = ['Enero 2019','Febrero 2019', 'Marzo 2019', 'Abril 2019', 'Mayo 2019', 'Junio 2019', 'Julio 2019',
	'Agosto 2019', 'Septiembre 2019', 'Octubre 2019', 'Noviembre 2019', 'Diciembre 2019', 'Enero 2020',
	'Febrero 2020', 'Marzo 2020', 'Abril 2020', 'Mayo 2020', 'Junio 2020', 'Julio 2020', 'Agosto 2020']

	listOfDFs = []
	for m in file_names:
		listOfDFs.append(pd.read_excel('new_data/Tx 51 '+m+'.xlsx'))

	stores = pd.read_excel('new_data/BDD Tx 89 2016-2020.xlsx')
	return listOfDFs, stores
    

def joining_pedidos_tiendas(listOfDFs, stores):

	file_names = ['Enero 2019','Febrero 2019', 'Marzo 2019', 'Abril 2019', 'Mayo 2019', 'Junio 2019', 'Julio 2019',
	'Agosto 2019', 'Septiembre 2019', 'Octubre 2019', 'Noviembre 2019', 'Diciembre 2019', 'Enero 2020',
	'Febrero 2020', 'Marzo 2020', 'Abril 2020', 'Mayo 2020', 'Junio 2020', 'Julio 2020', 'Agosto 2020']

	for i in range(len(file_names)):
		listOfDFs[i]['MES'] = file_names[i]

	df = pd.concat(listOfDFs)
	df2 = pd.merge(df, stores, left_on='Tienda', right_on='Codigo', how='inner')
	return df2

def formatingText(text):
	# This function was used by Ana in the bootcamp this allows us to give a standard an simple format to our text
	# Here it will be applied in the shops
    text = text.lower()
    text = re.sub('<.*?>', '', text)
    text = re.sub(':.*?:', '', text)
    text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", text), 0, re.I)
    text = normalize( 'NFC', text)
    text = re.sub('[^a-z ]', '', text)
    return text

def extracting_columns(df2):
	df_ = df2[['Pedido','Fecha Pedido','Tienda','Nombre','Población_y', 'Calle', 'Fabricante',
	'Nombre Fabricante','Material','Nombre Material','Cantidad de pedido','UM','Valor Unitario Pedido','Valor Total Pedido',
	'Ctd.facturada','Valor Unitario Factura','Valor TotalFactura','Descuento Teaté','Denominación Motivo Rechazo',
	'Cupón Dscto','Valor Cupón Teaté', 'FechaCreación','Nombre ZonaComercial','Comuna','Barrio','MES','Ce.','HoraMovil','Nombre Ruta']].copy()

	df_['Region'] = df_['Ce.'].apply(lambda x:np.where(x == 2000, 'region cali', 'region medellin'))

	df_.rename(columns={'Población_y':'Población','Nombre':'Nombre Tienda',
		'Calle':'Dirección Tienda','FechaCreación':'Fecha Creación Tienda'},inplace=True)

	df_['Pedido'] = df_['Pedido'].astype('int')
	df_['Tienda'] = df_['Tienda'].astype('int')
	df_['Fabricante'] = df_['Fabricante'].astype('int')

	df3 = df_[['Tienda','Nombre Tienda','Población','Dirección Tienda','Fecha Creación Tienda',
	'Nombre ZonaComercial','Comuna','Barrio','Region','Pedido','Fecha Pedido','Fabricante',
	'Nombre Fabricante','Material','Nombre Material','Cantidad de pedido','UM',
	'Valor Unitario Pedido','Valor Total Pedido','Ctd.facturada','Valor Unitario Factura',
	'Valor TotalFactura','Descuento Teaté','Denominación Motivo Rechazo','Cupón Dscto',
	'Valor Cupón Teaté','HoraMovil','Nombre Ruta','MES']].copy()

	df3['Nombre Tienda'] = df3['Nombre Tienda'].apply(formatingText)

	return df3