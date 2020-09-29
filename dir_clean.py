import pandas as pd
import numpy as np
import re

def replacing_val(dictionary, column, df):
    for key in dictionary.keys():
        df[column]=df[column].str.replace(key,dictionary[key])
        df[column]=df[column].str.strip()
        
def assign_data(df,key,value):
    dictionary=df[[key,value]][df[value]!='SIN DATOS'].groupby([key,value]).last().reset_index(level=1).to_dict()
    for i,val in enumerate(df[value]):
        #print(i,val)
        if val=='SIN DATOS' and df.loc[i,key] in dictionary[value].keys():
            df.loc[i,value]=dictionary[value][df.loc[i,key]]
            #print(i, val, df.loc[i,key], df.loc[i,value])
        
def clean(df):
    df_copy=df.copy()
    for i in ['Barrio','Población','Comuna']:
        df_copy[i].fillna('Sin Datos', inplace=True)
    
    df_neigh = df_copy[['Dirección Tienda', 'Barrio', 'Población', 'Comuna', 'Region', 'Tienda']].groupby(['Dirección Tienda', 'Barrio', 'Población', 'Comuna', 'Region', 'Tienda']).last().reset_index()
    
    for i in ['Dirección Tienda','Barrio','Población','Comuna']:
        df_neigh[i]=df_neigh[i].str.upper()
    replace_dict_dir={' ':'', 'KIL.*METRO':'Kilometro', 'OESTE':'O', 'OE':'O', 'ESTE':'E', 'NORTE':'N','SUR':'S', 'AC':'Calle', 'AK':'Carrera', 'TV':'Transversal', 'AV':'Avenida', 'CR':'Carrera', 'CL':'Calle', 'KR':'Carrera', 'CRA':'Carrera', 'CLL':'Calle', 'DG':'Diagonal'}
    replace_dict_other={'Á':'A','É':'E','Í':'I','Ã':'I','Ó':'O','Ú':'U','Ñ':'N','BARRIO':'','.':'','\xad':'', '  ':' ','ª':'','AA':'A'}
    replace_dict_barrios={'^ALFONZO':'ALFONSO', ' II':' 2', ' LLL':' 3','ETAPA':'',' ET ':' ','JARDI$':'JARDIN','AGACATAL':'AGUACATAL', 'VALLE DE LILI':'VALLE DEL LILI','HELENA':'ELENA','GIRARDO$':'GIRARDOT','CONFENALCO':'COMFENALCO', 'BRISA ':'BRISAS ','DESEPAZ':'DECEPAZ','- ':' ','IMVICALI':'INVICALI', 'INDICALI':'INVICALI','COMUNEROS I' : 'COMUNEROS 1','COMUNEROS L':'COMUNEROS 1', 'LENGUA':'LEGUA', 'DOCE ':'12 ', 'KENEDY':'KENNEDY', 'FLORALIA IA':'FLORALIA', 'LAURIANO':'LAUREANO','XV2I':'X2I', 'MIRA FLORES':'MIRAFLORES','NARANJO ':'NARANJOS ','NARANJOS I':'NARANJOS 1', 'CONFANDI':'COMFANDI', 'TORRIJO$':'TORRIJOS', ' LL$':' 2', 'PRIMERO':'1', 'SOL I':'SON 1', 'REMANSOS$':'REMANSO', 'CLAVEL':'CLAVER', 'SANTAMONICA':'SANTA MONICA','COLORADO I':'COLORADO 1',' N ':' ',' Nº ':' ', 'ARAJUEZ':'ARANJUEZ','PICHACHITO':'PICACHITO','VICTOIRIA':'VICTORIA','BELALACAZAR':'BELALCAZAR', 'VELAZCO':' VELASCO', 'PORTAL DE JORDAN':'PORTAL DEL JORDAN', 'TERRANOZA':'TERRANOVA','PARQUES DE CASTILLA':'PARQUE DE CASTILLA','ISAC':'ISAAC','ISAS':'ISAAC','SANJORGE':'SAN JORGE','#':'', 'SAN ANTONIO PRADOS':'SAN ANTONIO DE PRADO', '  ':' '}
    replace_dict_poblacion={'SAN ANTONIO PRADOS':'SAN ANTONIO DE PRADO','^ESTRELLA':'LA ESTRELLA','^CALI':'SANTIAGO DE CALI'}
    replacing_val(replace_dict_dir, 'Dirección Tienda', df_neigh)
    replacing_val(replace_dict_other, 'Barrio', df_neigh)
    replacing_val(replace_dict_barrios, 'Barrio', df_neigh)
    replacing_val(replace_dict_other, 'Población', df_neigh)
    replacing_val(replace_dict_poblacion, 'Población', df_neigh)
    replacing_val(replace_dict_other, 'Comuna', df_neigh)
    df_neigh['Dirección Tienda']=df_neigh['Dirección Tienda'].apply(lambda x:re.sub("VIA|[A-Za-z]+|[0-9]+|[#]+|[-]+", lambda ele:ele[0] + " ", x))
    df_neigh['Comuna'] = df_neigh['Comuna'].str.replace('COMUNA', '').str.strip().str.lstrip('0')
    df_neigh_cali=df_neigh[df_neigh['Region']=='region cali']
    df_neigh_cali=df_neigh_cali.reset_index(drop=True)
    for i in ['Barrio','Población','Comuna']:
        assign_data(df_neigh_cali,'Dirección Tienda',i)
    df_neigh_med=df_neigh[df_neigh['Region']=='region medellin']
    df_neigh_med=df_neigh_med.reset_index(drop=True)
    for i in ['Barrio','Población','Comuna']:
        assign_data(df_neigh_med,'Dirección Tienda',i)
    df_neigh_concat=pd.concat([df_neigh_cali,df_neigh_med],axis=0)
    df_neigh_concat.reset_index(inplace=True, drop=True)
    df_neigh_concat.drop_duplicates(subset='Tienda', inplace=True)
    df_neigh_concat.reset_index(drop=True, inplace= True)
    df_final=df_copy.merge(df_neigh_concat,left_on=['Tienda'],right_on=['Tienda'], how="left")
    return df_final
    
