from datetime import datetime
from src.lib.Analysis import Analysis
from src.lib.Binance.BinanceAPI import BinanceAPI
from os import system
from time import sleep, time

def makeDecision(candles, pos):
    print("OK")

api = BinanceAPI()
start = round(time() - (60 * 500)) * 1000
dataset = api.getCandles("ADAUSDT", "1m", start)
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
start = round(((start/1000) - (60 * 500)) * 1000)
sleep(1)
dataset = api.getCandles("ADAUSDT", "1m", start) + dataset
analysis = Analysis(dataset)
nbr = len(dataset) - 15
walletADA = 0
walletUSDT = 2000
price = float(dataset[0][4])
stopLoss = round(price - (price * 0.01), 4)
takeProfit = round(price + (price * 0.01), 4)
lastFund = walletUSDT
win = 0
loss = 0
risk = 1
for i in range(0, nbr):
    price = float(dataset[i][4])
    priceLow = float(dataset[i][3])
    priceHigh = float(dataset[i][2])
    if analysis.getRSI(14, i) < 30 and walletADA == 0:
        walletADA = (walletUSDT * risk)/float(dataset[i][4])
        stopLoss = round(price - (price * 0.005), 4)
        takeProfit = round(price + (price * 0.01), 4)
        lastFund = walletUSDT
        walletUSDT = walletUSDT - (walletUSDT * risk)
    elif walletADA > 0 and priceHigh >= takeProfit:
        walletUSDT = walletUSDT + (walletADA * takeProfit)
        walletADA = 0
        risk = 1
        win += 1
        system("clear")
        print("{} \033[32m {} USDT\033[39m".format(datetime.fromtimestamp(dataset[i][0]/1000), round(walletUSDT - lastFund, 2)))
        print("\nWIN RATE => {}%".format(round(win/(loss+win) * 100)))
        print("NB TRADE => {}".format(win+loss))
        print("USDT => {}".format(round(walletUSDT, 2)))
        sleep(1)
    elif walletADA > 0 and priceLow <= stopLoss:
        walletUSDT = walletUSDT + (walletADA * stopLoss)
        walletADA = 0
        loss += 1
        if risk < 1:
            risk = risk * 2
        system("clear")
        print("{} \033[31m {} USDT\033[39m".format(datetime.fromtimestamp(dataset[i][0]/1000), round(walletUSDT - lastFund, 2)))
        print("\nWIN RATE => {}%".format(round(win/(loss+win) * 100)))
        print("NB TRADE => {}".format(win+loss))
        print("USDT => {}".format(round(walletUSDT, 2)))
        sleep(1)