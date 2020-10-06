def similarity_matrix(data):
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from scipy import sparse

    #Substract orders and products
    Ped_mat=data[['Pedido','Material','Nombre Material']]
    Ped_mat.insert(2,'valor',1)
    
    #Get the contingency table (transactions)
    Transactions=pd.crosstab(Ped_mat['Pedido'],Ped_mat['Material'],values=Ped_mat['valor'],aggfunc='count')

    #Reset dataframe format
    Transactions=Transactions.notnull()
    Transactions.index.name=None
    Transactions.columns.name=None
    Trans=Transactions.loc[:,:].replace(False, np.nan)
    
    #Replace values with 0 in null values and 1 when the item appears in row
    Trans=Transactions.loc[:,:].replace(False, '0')
    Trans=Trans.loc[:,:].replace(True, '1')
    
    #Get similarity matrix (cosine)
    Trans_prueba=Trans.transpose()
    similar=cosine_similarity(Trans_prueba)
    similar_items_matrix=pd.DataFrame(similar)
    
    #Replace columns and index names with material codes
    names=list(Trans.columns)
    similar_items_matrix.columns=[x for x in names]
    similar_items_matrix.index=[x for x in names]
    
    return Trans,similar_items_matrix;  
