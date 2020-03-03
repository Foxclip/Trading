import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("EURUSD_i_M1_201706131104_202002240839.csv", sep="\t")
eur_usd = list(df["<CLOSE>"])
plt.plot(eur_usd)
plt.show()
