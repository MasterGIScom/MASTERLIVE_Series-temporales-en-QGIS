import ee
coleccionLimites = ee.FeatureCollection("USDOS/LSIB/2017")
filtropais = coleccionLimites.filter(ee.Filter.eq('COUNTRY_NA', 'Peru'))
Map.centerObject(filtropais,6)
    # Factor R -------------
clim_rainmap = ee.Image("OpenLandMap/CLM/CLM_PRECIPITATION_SM2RAIN_M/v01")
year = clim_rainmap.reduce(ee.Reducer.sum())
R_monthly = ee.Image(10).pow(ee.Image(1.5).multiply(clim_rainmap.pow(2).divide(year).log10().subtract(-0.08188))).multiply(1.735)
factorR = R_monthly.reduce(ee.Reducer.sum())
    
    # Factor K --------------
sand = ee.Image("OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02").select('b0')
silt = ee.Image('users/aschwantes/SLTPPT_I').divide(100)
clay = ee.Image("OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02").select('b0')
morg = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02").select('b0').multiply(0.58)
sn1 = sand.expression('1 - b0 / 100', {'b0': sand})
orgcar = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02").select('b0')
        
soil = ee.Image([sand, silt, clay, morg, sn1, orgcar]).rename(['sand', 'silt', 'clay', 'morg', 'sn1', 'orgcar'] )
factorK = soil.expression(
  '(0.2 + 0.3 * exp(-0.0256 * SAND * (1 - (SILT / 100)))) * (1 - (0.25 * CLAY / (CLAY + exp(3.72 - 2.95 * CLAY)))) * (1 - (0.7 * SN1 / (SN1 + exp(-5.51 + 22.9 * SN1))))',
  {
    'SAND': soil.select('sand'),
    'SILT': soil.select('silt'),
    'CLAY': soil.select('clay'),
    'MORG': soil.select('morg'),
    'SN1':  soil.select('sn1'),
    'CORG': soil.select('orgcar')
  });
    
    # Factor LS --------------
facc = ee.Image("WWF/HydroSHEDS/15ACC")
dem = ee.Image("WWF/HydroSHEDS/03CONDEM")
slope = ee.Terrain.slope(dem)
    
ls_factors = ee.Image([facc, slope]).rename(['facc','slope'])
factorLS = ls_factors.expression(
  '(FACC*270/22.13)**0.4*(SLOPE/0.0896)**1.3',
  {
    'FACC': ls_factors.select('facc'),
    'SLOPE': ls_factors.select('slope')     
  });
    
    # Factor C --------------
ndvi_median = ee.ImageCollection("MODIS/006/MOD13A2").median().multiply(0.0001).select('NDVI')
factorC = ee.Image(0.805).multiply(ndvi_median).multiply(-1).add(0.431)
        
    # EROSION
erosion = factorC.multiply(factorR).multiply(factorLS).multiply(factorK)
    
    # MAPA
paleta_erosion = ["#00BFBF", "#00FF00", "#FFFF00", "#FF7F00", "#BF7F3F", "#141414"]
erosion_vis = {'palette':paleta_erosion,'min':0,'max': 6000}

Map.addLayer(erosion.clip(filtropais), erosion_vis, 'Erosion')
Map.centerObject(roi)
    