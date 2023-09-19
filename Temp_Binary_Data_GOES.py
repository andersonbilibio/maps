# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 08:57:00 2023

@author: Anderson Bilibio
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
# import xarray as xr
# from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
# import matplotlib.ticker as mticker
# from matplotlib import ticker, cm
# import time 
# import cartopy.io.img_tiles as cimgt
# import matplotlib.colors as mcolors
# from mpl_toolkits.basemap import Basemap 


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
threshold = -40
dados_temperatura, longitude, latitude, date_obj = read_gzbin(f_name, threshold)
###============================================================================

# Etapa 2: Identifique as regiões de convecção (substitua com seus próprios critérios)
temperatura_negativa = np.where(dados_temperatura > -40, np.nan, dados_temperatura)
limite_temperatura = -80  # Limite de temperatura para identificar a convecção
regioes_conveccao = np.where(temperatura_negativa < limite_temperatura, np.nan, temperatura_negativa)

# Etapa 4: Plote o mapa da América Latina com destaque nas regiões de convecção
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())


# Plote um mapa da América Latina (substitua com seus próprios dados geoespaciais)
# Use 'latitude' e 'longitude' para definir os limites geográficos do mapa.
ax.set_extent([-90, -20, -40, 20], ccrs.PlateCarree())

#? Adiciona os cortornos#===========================================
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

states = cfeature.NaturalEarthFeature(category='cultural', 
                                      name='admin_1_states_provinces_lines', 
                                      scale='50m', 
                                      facecolor='none')

ax.add_feature(states, edgecolor='black', linestyle=':', linewidth=1)

#? construindo a grade do mapa#===========================================
g1 = ax.gridlines(crs=ccrs.PlateCarree(), 
                  draw_labels=True, 
                  linestyle='--', 
                  linewidth=1, 
                  color='black',
                  )

#? Utilizar como base mapa quando nao for usar do google
ax.stock_img() 


# Mostre o mapa
plt.imshow(temperatura_negativa/100.-273.13, cmap='magma',  
           origin='lower', 
           extent=[longitude.min(), longitude.max(), 
                   latitude.min(), latitude.max()], 
           transform = ccrs.PlateCarree()
           )

    
plt.colorbar(label='Temperatura (°C) -' +' '+ str(date_obj), shrink=0.80)

# Ajusta o espaçamento entre os subplots
plt.tight_layout()

# Personalize o mapa (adicionando contornos de países, títulos, etc.)
# Add a label to the plot
plt.title('Regiões de Convecção')

plt.text(-55, -44, 'Longitude ($^{\circ}$)', transform=ccrs.PlateCarree(), 
         fontsize=12, color='black')

plt.text(-97, -15, 'Latitude ($^{\circ}$)', transform=ccrs.PlateCarree(), 
         fontsize=12, color='black', rotation=90 )

plt.subplots_adjust(wspace=0.15, hspace=0.02, left=0.12, right=0.98, top=0.95, bottom=0.005)

plt.text(-87, 17, '${\lambda_{H}}=$', transform=ccrs.PlateCarree(), 
         fontsize=15, color='black')

plt.text(-35, 17, '${c_{H}}=$', transform=ccrs.PlateCarree(), 
         fontsize=15, color='black')

plt.text(-35, -37, '${\phi}=$', transform=ccrs.PlateCarree(), 
         fontsize=15, color='black')

plt.text(-87, -37, '${per}=$', transform=ccrs.PlateCarree(), 
         fontsize=15, color='black')

plt.show()


