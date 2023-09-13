# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:45:42 2023

@author: Anderson Bilibio
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import numpy as np
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import ticker, cm
import time 
import cartopy.io.img_tiles as cimgt



# Carregue seus dados binários aqui (depende do formato)
def read_gzbin(f_name, threshold):
    # import necessary libraries
    import numpy as np
    import gzip
    from datetime import datetime
    
    # extract date and time from file name
    date_str = f_name[-15:-3]
    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M')#%S
    
    # read binary data from gzip-compressed file
    with gzip.open(f_name, 'rb') as f:
        uncompressed_data = f.read()
        dados_binarios = np.frombuffer(uncompressed_data, dtype=np.int16)

        
        # reshape binary data into a 2D numpy array
        imageSize = [1800,1800]
        dados_binarios = dados_binarios.reshape(imageSize)
        
        # Define x and y positions
        dlon=np.arange(dados_binarios.shape[1]) * 0.04 - 100
        dlat=np.arange(dados_binarios.shape[0]) * 0.04 - 50
        
        
        # return the 2D numpy array, dlon, dlat, and date_obj
        return dados_binarios, dlon, dlat, date_obj


caminho = 'C:/2023/Beckup_note/ANDERSON/PCI_D_inpe_2023\
/mapas_temp_nuvem_python/03-06-2005-goes12_ch4/'                              

# f_name='gcr.050602.0200_0200g.ch4'
nome = 'S10216956_200506020330.gz'

f_name = caminho+nome

saida = caminho 

#Deletes values higher than -65 celcius degress
threshold = 0. 
data, dlon, dlat, date_obj = read_gzbin(f_name, threshold)
###============================================================================


###============================================================================
# Matriz de temperatura 
temperatura = data

# Defina um limite de temperatura negativa para filtragem
limite_negativo = 0  # Ajuste conforme necessário

# Crie uma máscara para valores de temperatura abaixo do limite negativo
mascara_negativa = temperatura < limite_negativo

# Aplique a máscara para manter apenas os valores mais negativos
temperatura_negativa = np.where(mascara_negativa, temperatura, np.nan)

###============================================================================
# Cria uma figura e os eixos do mapa usando a projeção de Mercator
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection=ccrs.Mercator()))

# Adiciona os limites do Brasil
ax.set_extent([-75, -30, -35, 7], ccrs.PlateCarree())

# Adiciona um fundo com mapa de satélite usando a biblioteca contextily (opcional)
# ax.stock_img()


# Adiciona características do mapa, como a costa do Brasil e os países
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

states = cfeature.NaturalEarthFeature(category='cultural', 
                                      name='admin_1_states_provinces_lines', 
                                      scale='50m', 
                                      facecolor='none')

ax.add_feature(states, edgecolor='black', linestyle='--', linewidth=1)

#? construindo a grade do mapa#===========================================
g1 = ax.gridlines(crs=ccrs.PlateCarree(), 
                  draw_labels=True, 
                  linestyle='--', 
                  linewidth=1, 
                  color='black')


###============================================================================
# Plote a temperatura negativa no mapa
# plt.imshow(temperatura_negativa,  cmap='BuPu_r', origin='lower', 
#            transform = ccrs.PlateCarree(), vmin=limite_negativo, vmax= 0)

X, Y = np.meshgrid(dlon, dlat)
Z = temperatura_negativa
plt.pcolormesh(X, Y, Z, vmin = 0, vmax = -100, cmap = 'rainbow') 

# Adicione uma barra de cores
plt.colorbar(shrink=0.7, label='Temperatura (°C)')

# Configurações adicionais do mapa, como contornos de países e título
ax.set_title(str(date_obj))
plt.tight_layout()

# Mostra o mapa
plt.show()