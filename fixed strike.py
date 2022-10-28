import requests
import pandas as pd
import matplotlib.pyplot as plt

ticker = "SPY"
strike = 370
strike1 = 350
strike2 = 400
exp = '2022-10-21'
datecutoff = '2022-09-01'

url = "https://api.orats.io/datav2/hist/strikes/options?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker="+str(ticker)+"&expirDate="+str(exp)+"&strike="+str(strike)
payload={}
headers={}
response = requests.request("GET", url, headers=headers, data=payload)
df = pd.read_json(response.text, orient='split')
print(df.head)
df.to_csv("fixed.csv")


url = "https://api.orats.io/datav2/hist/strikes/options?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker="+str(ticker)+"&expirDate="+str(exp)+"&strike="+str(strike1)
payload={}
headers={}
response = requests.request("GET", url, headers=headers, data=payload)
df1 = pd.read_json(response.text, orient='split')
print(df.head)
df1.to_csv("fixed.csv")

url = "https://api.orats.io/datav2/hist/strikes/options?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker="+str(ticker)+"&expirDate="+str(exp)+"&strike="+str(strike2)
payload={}
headers={}
response = requests.request("GET", url, headers=headers, data=payload)
df2 = pd.read_json(response.text, orient='split')
print(df.head)
df1.to_csv("fixed.csv")

df = df[df.tradeDate>=datecutoff]
df1 = df1[df1.tradeDate>=datecutoff]
df2 = df2[df2.tradeDate>=datecutoff]

fig, (ax1) = plt.subplots(nrows=1, ncols=1)
ax2 = ax1.twinx()
ax1.set_title("smoothed Vol for: " +str(strike) + " " + str(exp))
#ax1.plot(df['tradeDate'], df['smvVol'], label=str(strike))
ax1.plot(df['tradeDate'], df['callMidIv'], label=(str(strike)+ " calls"), color='black', linestyle='dotted')
ax1.plot(df['tradeDate'], df['putMidIv'], label=(str(strike)+ " puts"), color='grey', linestyle='dotted')
ax1.plot(df1['tradeDate'], df1['callMidIv'], color = 'orange', label=(str(strike1) + " calls"))
ax1.plot(df1['tradeDate'], df1['putMidIv'], color = 'pink', label=(str(strike1) + " puts"))
ax1.plot(df2['tradeDate'], df2['callMidIv'], color = 'purple', label=(str(strike2) + " calls"))
ax1.plot(df2['tradeDate'], df2['putMidIv'], color = 'blue', label=(str(strike2)+" puts"))

ax2.plot(df['tradeDate'], df['spotPrice'], color='red', label = 'Stock')
plt.xticks(rotation=90)

ax1.legend()
ax2.legend()
plt.show()