from ORATSgrabber import getData
import matplotlib.pyplot as plt
# Importing library
from scipy.stats import skew
import numpy as np
import py_vollib.black_scholes


df = getData('QQQ')

exp = '2022-09-21'

df = df[df.expirDate == exp]
df['ivShiftUp'] = df.smvVol.shift(4)
df['ivShiftDown'] = df.smvVol.shift(-4)
