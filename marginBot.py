from datetime import datetime
from os import system
from time import sleep, time
from src.lib.Binance.BinanceAPI import BinanceAPI
from src.lib.Analysis import Analysis

class Bot:
    def __init__(self, api, currency = "CHZ"):
        self.api = api
        self.walletB = float(self.api.getAccount("USDT", "margin")["free"])
        self.walletA = float(self.api.getAccount(currency, "margin")["free"])
        self.symbol = currency + "USDT"
        self.currency = currency
        price = float(self.api.ticker(self.symbol)["price"])
        sleep(1)
        self.stopLoss = round(price + (price * 0.01), 4)
        self.takeProfit = round(price - (price * 0.02), 4)
        self.risk = 1
        self.lastFund = round(self.walletB, 2)
        self.logs = []
        
    def run(self):
        candlesM1 = self.api.getCandles(self.symbol, "1m")
        analysisM1 = Analysis(candlesM1)
        support = analysisM1.getSupport()[0:3]
        while True:
            try:
                price = float(self.api.ticker(self.symbol)["price"])
                if round(time() * 1000) > (int(candlesM1[499][0]) + 60000):
                    candlesM1 = self.api.getCandles(self.symbol, "1m")
                    analysisM1.setCandles(candlesM1)
                    support = analysisM1.getSupport()[::-1][0:3]
                    self.makeDecision(price, self.priceAction(support, candlesM1))
            except:
                print("Connexion Lost")
                sleep(1)
                continue
            self.makeDecision(price, False)
            system("clear")
            print("CHZ = {}\nPRICE = {}\nRISK RATIO = {}".format(round(self.walletA + (self.walletB / price), 2), price, self.risk))
            print(support)
            print(datetime.fromtimestamp(int(candlesM1[len(candlesM1) - 1][0])/1000))
            if (self.walletB > 10):
                print("TAKE PROFIT = {}\nSTOP LOSS = {}".format(self.takeProfit, self.stopLoss))
            for log in self.logs:
                print(log)
            sleep(3)

    def priceAction(self, support, candles):
        currentPos = len(candles) - 1
        for s in range(1, len(support) - 1):
            if (float(candles[currentPos][4]) < support[s] and float(candles[currentPos - 1][1]) > support[s]):
                return True
        return False

    def makeDecision(self, price, letsGo):
        if (letsGo and self.walletA > 10):
            self.stopLoss = round(price + (price * 0.01), 4)
            self.takeProfit = round(price - (price * 0.02), 4)
            self.sell()
            self.logs.append("{} \033[33m BUY => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletA, 2))))
        
        if (price <= self.takeProfit and self.walletB > 10):
            self.risk = 1
            self.buy()
            self.logs.append("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletA, 2))))
        elif (price >= self.stopLoss and self.walletB > 10):
            if (self.risk < 1):
                self.risk = self.risk * 2
            self.buy()
            self.logs.append("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletA, 2))))

    def refreshWallets(self):
        self.walletB = float(self.api.getAccount("USDT", "margin")["free"])
        sleep(1)
        self.walletA = float(self.api.getAccount(self.currency, "margin")["free"])

    def buy(self):
        order = self.api.createMarginOrder("BUY", self.walletB * self.risk, self.symbol)
        self.refreshWallets()
        return order
    
    def sell(self):
        order = self.api.createMarginOrder("SELL", self.walletA, self.symbol)
        self.refreshWallets()
        return order

try:
    api = BinanceAPI()
    bot = Bot(api, "CHZ")
    bot.run()
except:
    print("No Connexion")