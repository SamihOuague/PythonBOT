from time import sleep, time
from src.lib.Binance.BinanceAPI import BinanceAPI
from src.lib.Analysis import Analysis

class Bot:
    def __init__(self):
        self.api = BinanceAPI()
        self.walletB = float(self.api.getAccount("USDT")["free"])
        self.walletA = float(self.api.getAccount("ADA")["free"])
        price = float(self.api.ticker()["price"])
        sleep(1)
        self.stopLoss = round(price - (price * 0.005), 4)
        self.takeProfit = round(price + (price * 0.01), 4)
        self.risk = 0.50
        self.lastFund = round(self.walletB, 2)
        
    def run(self):
        candles = self.api.getCandles("ADAUSDT", "1m")
        analysis = Analysis(candles)
        while True:
            price = float(self.api.ticker()["price"])
            if round(time() * 1000) > (int(candles[499][0]) + 60000):
                candles = self.api.getCandles("ADAUSDT", "1m")
                analysis.setCandles(candles)
                print(price, (analysis.getRSI(period=14, pos=len(candles) - 15)))
            self.makeDecision(price, (analysis.getRSI(period=14, pos=len(candles) - 15)))
            sleep(3)

    def makeDecision(self, price, rsi):
        if (rsi < 30 and self.walletA < 10):
            print("BUY => " + str(price))
            self.buy()
        
        if (price >= self.takeProfit and self.walletA > 10):
            self.risk = 0.50
            print("SELL => " + str(price))
            self.sell()
        elif (price <= self.stopLoss and self.walletA > 10):
            if (self.risk < 1):
                self.risk = self.risk * 2
            print("SELL => " + str(price))
            self.sell()

    def refreshWallets(self):
        self.walletB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        self.walletA = float(self.api.getAccount("ADA")["free"])

    def buy(self):
        order = self.api.createOrder("buy", self.walletB * self.risk)
        self.refreshWallets()
        return order
    
    def sell(self):
        order = self.api.createOrder("sell", self.walletA)
        self.refreshWallets()
        return order

bot = Bot()
bot.run()