from ORATSgrabber import getData
import matplotlib.pyplot as plt
# Importing library
from scipy.stats import skew
import numpy as np


df = getData('QQQ')
df["OTM"] = df.strike/df.spotPrice
df = df[(df.OTM<=1.099) & (df.OTM>=.91)]
explist = df.expirDate.unique()

slopeList = []

for exp in explist:
    df_new = df[df.expirDate==exp]
    epxSkew = skew(df_new.smvVol.to_list(), axis=0, bias=True)
    print(str(exp)+ " " + str(epxSkew))

    #I was calculating slope, but "diff" picks up curve changes better
    #slope, intercept = np.polyfit(np.log(df_new.strike.to_list()), np.log(df_new.smvVol.to_list()), 1)
    #abline_values = [slope * i + intercept for i in df_new.strike.unique()]

    dx = np.diff(df_new.strike.unique())
    dy = np.diff(df_new.smvVol.to_list())
    slopeList.append((exp,df_new.strike.unique(), dx, dy))
    print(slopeList)

    df_new.plot('strike','smvVol')
    #plt.plot(df_new.strike.unique(),abline_values)
    plt.title(str(exp))
    plt.show()
