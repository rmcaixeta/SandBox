
import pandas as pd
from pyproj import Transformer

df = pd.read_csv('file.csv',low_memory=False)

#converter = Transformer.from_crs("EPSG:3060", "EPSG:3163", always_xy=True) # IGN to RGNC
converter = Transformer.from_crs("EPSG:3163", "EPSG:3060", always_xy=True) # RGNC to IGN

df['XT'], df['YT'] = converter.transform(df.X, df.Y)
print(df[['X','Y','XT','YT']])

