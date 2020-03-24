import pandas as pd
import time

time1 = time.time()
df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
time2 = time.time()
elapsed = time2 - time1
print(f"Opening: {elapsed}s")

time1 = time.time()
tm = pd.to_datetime(df["<TIME>"].iloc[-1])
print(tm)
time_column = pd.to_datetime(df["<TIME>"])
print(time_column)
print(time_column.dt.dayofweek)
print(time_column.iloc[-1].dayofweek)
print(time_column.iloc[-1].hour)
print(time_column.iloc[-1].minute)
time2 = time.time()
elapsed = time2 - time1
print(f"Converting: {elapsed}s")
