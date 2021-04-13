import ee
from ee_plugin import Map
countries = ee.FeatureCollection('USDOS/LSIB/2017');
country = countries.filter(ee.Filter.eq('COUNTRY_NA', 'Peru'))
#region = country.geometry()
trmm = ee.ImageCollection("TRMM/3B42")
rainfall =trmm.select("precipitation").filterDate("2017-11-01","2017-11-30")
maximum = rainfall.max()
aoi = country.geometry()

Map.addLayer(maximum.clip(aoi),{'min':0, 'max':20, 'palette':['white','blue','darkblue','red','purple']},"pp")