import pandas as pd
import geopandas as gpd
import os

df = pd.read_csv(os.path.join('practicals','data','clean','2024-06-14-listings.csv.gz'))

df2 = df.copy()

df2['last_scraped'] = pd.to_datetime(df2.last_scraped)
df2['host_since'] = pd.to_datetime(df2.host_since)
df2['first_review'] = pd.to_datetime(df2.first_review)
df2['last_review'] = pd.to_datetime(df2.last_review)

df2['property_type'] = df2.property_type.astype('category')
df2['room_type'] = df2.room_type.astype('category')

df2.to_parquet('20240614-London-listings.parquet', engine='pyarrow', compression='zstd')

gdf = gpd.GeoDataFrame(df2, geometry=gpd.points_from_xy(df2.longitude, df2.latitude, crs='EPSG:4326'))

gdf.to_parquet('20240614-London-listings.geoparquet')

exit()