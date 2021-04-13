#Algorithms.Landsat.simpleComposite
#método para seleccionar un subconjunto de escenas en cada ubicación,
#convierte a reflectancia TOA, aplica la
#puntuación de nube simple y toma la mediana de los píxeles menos nublados

import ee
from ee_plugin import Map
geometry=ee.Geometry.Point(-78.48077,-8.48461)

landsatraw = ee.ImageCollection("LANDSAT/LC08/C01/T1")\
.filterDate('2018-01-01','2018-12-31')\
.filterBounds(geometry)

composicionsimple = ee.Algorithms.Landsat.simpleComposite(**
{'collection': landsatraw,
'percentile':75,
'cloudScoreRange':5,
'asFloat': True
})

trueVis432 = { 'bands':['B4','B3', 'B2'],'min' : 0 ,'max': 0.3}
falsocolor={ 'bands':['B5','B4', 'B3'],'min' : 0 ,'max': [0.5,0.3,0.3]}
Map.addLayer(composicionsimple,trueVis432,'LC08432')
Map.addLayer(composicionsimple,falsocolor,'FalsoColor')
