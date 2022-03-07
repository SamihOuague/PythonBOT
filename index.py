
from datetime import datetime
from os import system
from time import sleep, time
from src.lib.Binance.BinanceAPI import BinanceAPI
from src.lib.Analysis import Analysis

class Bot:
    def __init__(self, currency = "CHZ"):
        self.api = BinanceAPI()
        self.walletB = float(self.api.getAccount("USDT")["free"])
        self.walletA = float(self.api.getAccount(currency)["free"])
        self.symbol = currency + "USDT"
        self.currency = currency
        price = float(self.api.ticker(self.symbol)["price"])
        sleep(1)
        self.stopLoss = round(price - (price * 0.005), 4)
        self.takeProfit = round(price + (price * 0.005), 4)
        self.risk = 0.125
        self.lastFund = round(self.walletB, 2)
        self.logs = []
        
    def run(self):
        candles = self.api.getCandles(self.symbol, "1m")
        analysis = Analysis(candles)
        rsi = analysis.getRSI(period=14, pos=len(candles) - 1)
        while True:
            price = float(self.api.ticker(self.symbol)["price"])
            if round(time() * 1000) > (int(candles[499][0]) + 60000):
                candles = self.api.getCandles(self.symbol, "1m")
                analysis.setCandles(candles)
                rsi = analysis.getRSI(period=14, pos=len(candles) - 1)
            self.makeDecision(price, rsi)
            system("clear")
            print("UDST = {}\nPRICE = {}\nRSI = {}".format(round(self.walletB + (self.walletA * price), 2), price, rsi))
            if (self.walletA > 10):
                print("TAKE PROFIT = {}\nSTOP LOSS = {}".format(self.takeProfit, self.stopLoss))
            for log in self.logs:
                print(log)
            sleep(3)

    def makeDecision(self, price, rsi):
        if (rsi < 30 and self.walletA < 10):
            self.stopLoss = round(price - (price * 0.005), 4)
            self.takeProfit = round(price + (price * 0.006), 4)
            self.buy()
            self.logs.append("{} \033[33m BUY => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletB, 2))))
        
        if (price >= self.takeProfit and self.walletA > 10):
            self.risk = 0.125
            self.sell()
            self.logs.append("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletB, 2))))
        elif (price <= self.stopLoss and self.walletA > 10):
            if (self.risk < 1):
                self.risk = self.risk * 2
            self.sell()
            self.logs.append("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(round(time())), str(round(self.walletB, 2))))

    def refreshWallets(self):
        self.walletB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        self.walletA = float(self.api.getAccount(self.currency)["free"])

    def buy(self):
        order = self.api.createOrder("buy", self.walletB * self.risk, self.symbol)
        self.refreshWallets()
        return order
    
    def sell(self):
        order = self.api.createOrder("sell", self.walletA, self.symbol)
        self.refreshWallets()
        return order

bot = Bot("DOGE")
bot.run()