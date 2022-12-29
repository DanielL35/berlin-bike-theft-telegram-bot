import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
from pyproj import Transformer

def assess_location(x,y,final):

    transformer = Transformer.from_proj(
        "epsg:4326",
        "epsg:25833",
        always_xy=True)

    lon_tr, lat_tr = transformer.transform(x, y)

    point = gpd.points_from_xy([lon_tr], [lat_tr], crs="EPSG:25833")

    final['where_am_I'] = final['geometry'].contains(point[0])
    
    if final[final['where_am_I'] == True]['thefts'].empty:
        print('Oops! This location does not seem to be in Berlin. Try again!')
        return None, None
    
    thefts_lor = final[final['where_am_I'] == True]['thefts'][0]
    
    
    
    your_loc = final[final['where_am_I'] == True]['PLR_NAME'][0]
    
    return your_loc, thefts_lor