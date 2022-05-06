#from datetime import datetime
#from time import sleep, time
#from src.lib.Binance.BinanceAPI import BinanceAPI
#from src.lib.Analysis import Analysis
#
#api = BinanceAPI()
#
#start = round(time() - (60 * 514)) * 1000
#candlesM15 = [[float(x) for x in d] for d in api.getCandles("CHZUSDT", "15m", start)]
#candlesM1 = [[float(x) for x in d] for d in api.getCandles("CHZUSDT", "1m")]
#analysis = Analysis(candlesM1)
#print(analysis.getSupport())
#j = 0
#for i in range(0, len(candlesM1)):
#    if candlesM1[i][0] == (candlesM15[j][0] + 900 * 1000):
#        j += 1





#lowz = {}
#
#for c in candles:
#    try:
#        lowz[c[3]] += 1
#    except KeyError:
#        lowz[c[3]] = 1

#for l in lowz:
#    if (lowz[l] > 8):
#        print(l, lowz[l])
n = 0.01
for i in range(0, 30):
    n = n * 2

print(n)
