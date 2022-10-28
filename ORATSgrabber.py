import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

#define strike range

def getData(stock):

    url = "https://api.orats.io/datav2/one-minute/strikes/chain?token=d63fc184-fa10-4b3e-9a15-ce756595897b&ticker=" + str(stock)
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    df = pd.read_csv(StringIO(response.text), sep=',')
    return(df)