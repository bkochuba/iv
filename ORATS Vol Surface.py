
import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

#define strike range
stock = 'SPX'
lows = 3750
highs = 3950

theexp = '2022-10-27'
theexp1 = '2022-10-27'
histdate = '202210261200'

#types: hist, comp, single
charttype = 'hist'

url = "https://api.orats.io/datav2/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker=" + str(stock)
payload={}
headers={}
response = requests.request("GET", url, headers=headers, data=payload)
df = pd.read_csv(StringIO(response.text), sep=',')
print(df.head)
df.to_csv("QQQoutput.csv")

#get past data
if charttype=='hist':
    hist_url = "https://api.orats.io/datav2/hist/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker="+ str(stock)+ "&tradeDate="+str(histdate)
else:
    hist_url = "https://api.orats.io/datav2/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker=" + str(stock)
payload={}
headers={}
response = requests.request("GET", hist_url, headers=headers, data=payload)
df_hist = pd.read_csv(StringIO(response.text), sep=',')
print(df_hist.head)


#various filtering
df['sym'] = df.ticker.astype(str)+df.expirDate.astype(str)+df.strike.astype(str)
putVolumeAll = df.putVolume.sum()
callVolumeAll = df.callVolume.sum()
print(putVolumeAll+callVolumeAll)

df = df[df.expirDate == theexp]
callVolumeNext = df.callVolume.sum()
putVolumeNext = df.putVolume.sum()
callOINext = df.callOpenInterest.sum()
putOINext = df.putOpenInterest.sum()
print(callOINext+putOINext)
print(callVolumeNext+putVolumeNext)
callPct = round(callVolumeNext/callVolumeAll,0)*100
putPct = round(putVolumeNext/putVolumeAll,0)*100

df = df[(df.strike>=lows) &  (df.strike<=highs)]
df['putOpenInterest'] = df.putOpenInterest * -1
df['putVolume'] = df.putVolume * -1
df.to_csv('merged1.csv')

df_hist['sym'] = (df_hist.ticker.astype(str))+(df_hist.expirDate.astype(str))+df_hist.strike.astype(str)

df_hist = df_hist[df_hist.expirDate == theexp1]

df_hist = df_hist[(df_hist.strike>=lows) & (df_hist.strike<=highs)]
df_hist.to_csv('merged2.csv')
df_hist['putOpenInterest'] = df_hist.putOpenInterest * -1
df_hist['putVolume'] = df_hist.putVolume * -1



df2 = df.merge(df_hist, left_on='sym', right_on='sym')
df2['callOIchg'] = df2.callOpenInterest_x - df2.callOpenInterest_y
df2['putOIchg'] = df2.putOpenInterest_x - df2.putOpenInterest_y
df2.to_csv("merged_comb.csv")


#plot it

fig, (ax1,  ax5, ax2) = plt.subplots(nrows=3, ncols=1)
ax3 = ax1.twinx()
ax4 = ax2.twinx()
if charttype=='hist':
    ax1.set_title(str(stock) + "  Skew for Exp: " + str(theexp) + " vs Exp on Date:" + str(histdate))
    ax1.plot(df['strike'], df['smvVol'], label=str(theexp))
    ax1.plot(df_hist['strike'], df_hist['smvVol'], color='blue', linestyle='dotted', label="hist" + str(theexp))
elif charttype=='single':
    ax1.set_title(str(stock) + "  Skew for Exp: " + str(theexp) + " vs Exp on Date:" + str(histdate))
    ax1.plot(df_hist['strike'], df_hist['smvVol'], label=str(theexp))
else:
    ax1.set_title(str(stock) + "  Skew for Exp: " + str(theexp) + " vs Exp:" + str(theexp1))
    ax1.plot(df['strike'], df['smvVol'], label=str(theexp))
    ax1.plot(df_hist['strike'], df_hist['smvVol'], color='blue', linestyle='dotted', label=str(theexp1))

#ax1.plot(df['strike'], df['smvVol'], label='current IV')
#ax1.plot(df_hist['strike'], df_hist['smvVol'], color = 'blue', linestyle='dotted', label = "hist iv")
ax3.bar(df.strike, df.callOpenInterest, color = 'green', label='COI')
ax3.bar(df.strike, df.putOpenInterest, color = 'red',label='POI')

ax5.bar(df.strike, df.callVolume, color = 'green', label='cVol')
ax5.bar(df.strike, df.putVolume, color = 'red',label='pVol')
ax5.set_title("Call Vol: " + str(callVolumeNext) +" = " + str(callPct) + "% of total | Put Vol: " +str(putVolumeNext) +" = " + str(putPct) + "% of total ")


ax3.bar(df2.strike_x, df2.callOIchg, color = 'green')
ax3.bar(df2.strike_x, df2.putOIchg, color = 'red')
ax2.plot(df['strike'], df['callMidIv'], color = 'blue')
ax2.plot(df_hist['strike'], df_hist['callMidIv'], color = 'blue', linestyle='dotted')
ax2.plot(df['strike'], df['putMidIv'], color = 'red')
ax2.plot(df_hist['strike'], df_hist['putMidIv'], color = 'red', linestyle='dotted')
ax4.bar(df2.strike_x, df2.callOIchg, color = 'green', label='COI Daily Chg')
ax4.bar(df2.strike_x, df2.putOIchg, color = 'red', label='POI Daily Chg')
ax1.legend()
#ax3.legend()
ax4.legend()
ax5.legend()
fig.tight_layout()
plt.show()




