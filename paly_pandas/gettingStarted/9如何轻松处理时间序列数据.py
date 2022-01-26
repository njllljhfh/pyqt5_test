# -*- coding:utf-8 -*-
import pandas as pd

air_quality = pd.read_csv("data/air_quality_no2_long.csv")
air_quality = air_quality.rename(columns={"date.utc": "datetime"})
print(air_quality)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(air_quality.city.unique())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(air_quality["datetime"])
air_quality["datetime"] = pd.to_datetime(air_quality["datetime"])
print(air_quality["datetime"])
