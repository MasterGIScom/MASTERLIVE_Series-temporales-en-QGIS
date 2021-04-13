import ee
from ee_plugin import Map
#Filtrar por Pais
coleccionLimites = ee.FeatureCollection("USDOS/LSIB/2017")
filtropais = coleccionLimites.filter(ee.Filter.eq('COUNTRY_NA', 'Mexico'))
Map.centerObject(filtropais,6)
#Importar Coleccion SENTINEL 5P
sentinel5P = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_NO2")
#Obtener Concentracion de NO2
NO2 = sentinel5P.filterDate("2019-08-01","2019-08-30").select("NO2_column_number_density")\
.max().clip( filtropais)
Map.addLayer(NO2,{'min':0,'max':0.0002,'palette':['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']},"NO2")


