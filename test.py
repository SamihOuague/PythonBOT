from datetime import datetime
from src.lib.Analysis import Analysis
from src.lib.Binance.BinanceAPI import BinanceAPI
from os import system
from time import sleep, time

def makeDecision(candles, pos):
    print("OK")

api = BinanceAPI()
dataset = api.getCandles("DOGEUSDT", "1m")
start = round(time() - (60 * 500)) * 1000
nbIter = 25
for i in range(0, nbIter):
    dataset = api.getCandles("DOGEUSDT", "1m", start) + dataset
    start = round(((start/1000) - (60 * 500)) * 1000)
    system("clear")
    print("download... {}%".format(round((i/nbIter) * 100)))
    sleep(1)

analysis = Analysis(dataset)
period = 14
walletA = 0
walletB = 300
stopLoss = 0
takeProfit = 0
risk = 0.125
win = 0
loss = 0
for i in range(period, len(dataset)):
    rsi = analysis.getRSI(period, i)
    ma99 = analysis.mobileAverage(99, i)
    if rsi < 30 and walletA == 0:
        price = float(dataset[i][1])
        walletA = (walletB * risk) / price
        walletB = walletB - (walletB * risk)
        stopLoss = price - (price * 0.005)
        takeProfit = price + (price * 0.006)
        print(datetime.fromtimestamp(int(dataset[i][0])/1000))

    if walletA > 0:
        if takeProfit <= float(dataset[i][2]):
            walletB = walletB + (walletA * takeProfit)
            walletA = 0
            print("\033[32mWIN\033[39m")
            risk = 0.125
            win += 1
        elif stopLoss >= float(dataset[i][3]):
            walletB = walletB + (walletA * stopLoss)
            loss += 1
            walletA = 0
            if (risk < 1):
                risk = risk * 2
            print("\033[31mLOSS\033[39m")

print("\n")
print("TAUX DE REUSSITE = " + str(round((win/(win + loss)) * 100)) + "%")
print("NOMBRE DE TRADE = " + str(win + loss))
print("WALLET USDT = " + str(round(walletB + (walletA * float(dataset[len(dataset) -1][1])), 2)))
print(datetime.fromtimestamp(int(dataset[0][0])/1000))