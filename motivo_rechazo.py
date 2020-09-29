def clean_motivo_rechazo(df):
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace(['Pédido Incompleto', 'Pédido incompleto'], 
                                                                              'Pedido incompleto')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace(['No hizo pédido', 
                                                                               'No Hizo Pedido'], 'No hizo pedido')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace('Pédido Duplicado', 'Pedido duplicado')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace(['Pédido sin descuento', 
                                                                               'Pédido sin Descuento'], 'Pedido sin descuento')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace('Pédido Atrasado',
                                                                              'Pedido atrasado')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].replace(['Averías de Transporte',
                                                                               'Daño Mecánico Transporte'], 
                                                                              'Problema en transporte')
    df['Denominación Motivo Rechazo'] = df['Denominación Motivo Rechazo'].str.capitalize()

    return df