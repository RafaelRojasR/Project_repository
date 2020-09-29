import pandas as pd
import numpy as np


def calculate_loyalty(promedio):
        if np.isnan(promedio):
            return "Tienda sin datos"
        elif promedio > 4:
            return "Lealtad alta"
        elif promedio > 2:
            return "Lealtad media"
        else:
            return "Lealtad baja"

def crear_col_lealtad_tienda(final_df):

        pedidos_tiendadf = final_df[['MES','Pedido', 'Tienda' ,'Nombre Tienda']].groupby(['Tienda','MES', 'Pedido'], as_index=False).agg({'Nombre Tienda':'count'})
        pedidos_tiendadf.rename({'Nombre Tienda': 'Num productos en el pedido'}, axis=1, inplace=True)

        pedidos_tiendadf2 = pedidos_tiendadf[['MES','Pedido', 'Tienda','Num productos en el pedido']].groupby(['Tienda','MES'], as_index=False).agg({'Pedido':'count', 'Num productos en el pedido':'mean'})
        pedidos_tiendadf2.rename({'Pedido': 'Num pedidos mensuales', 'Num productos en el pedido':'Num promedio productos en el pedido' }, axis=1, inplace=True)

        pedidos_tiendadf3 = pedidos_tiendadf2[['MES','Num pedidos mensuales',  'Tienda', 'Num promedio productos en el pedido']].groupby(['Tienda'], as_index=False).agg({'Num pedidos mensuales':'mean', 'Num promedio productos en el pedido':'mean'})
        pedidos_tiendadf3.rename({'Num pedidos mensuales': 'Num promedio de pedidos mensuales'}, axis=1, inplace=True)

        pedidos_tiendadf3['lealtad'] = pedidos_tiendadf3['Num promedio de pedidos mensuales'].apply(calculate_loyalty)

        return pedidos_tiendadf3['lealtad']

