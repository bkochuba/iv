
import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

def dteData_app():

    #define strike range
    stock = 'SPY'
    lows = 377
    highs = 392

    theexp = '2022-10-28'
    theexp1 = '2022-10-28'
    histdate = '202210271600'

    #types: hist, comp, single
    charttype = 'hist'

    url = "https://api.orats.io/datav2/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker=" + str(stock)
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    df = pd.read_csv(StringIO(response.text), sep=',')


    #get past data
    if charttype=='hist':
        hist_url = "https://api.orats.io/datav2/hist/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker="+ str(stock)+ "&tradeDate="+str(histdate)
    else:
        hist_url = "https://api.orats.io/datav2/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker=" + str(stock)
    payload={}
    headers={}
    response = requests.request("GET", hist_url, headers=headers, data=payload)
    df_hist = pd.read_csv(StringIO(response.text), sep=',')

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

    df.columns = 'current_' + df.columns
    df_hist.columns = 'hist_' + df_hist.columns
    df2 = df.merge(df_hist, left_on='current_sym', right_on='hist_sym')
    df2['callOIchg'] = df2.hist_callOpenInterest - df2.current_callOpenInterest
    df2['putOIchg'] = df2.hist_putOpenInterest - df2.current_putOpenInterest
    return(df2)






