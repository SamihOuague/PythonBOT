from datetime import datetime
from src.lib.Analysis import Analysis

class SimulationV4:
    def __init__(self, dataset, walletA, walletB):
        self.dataset = [[float(x) for x in d] for d in dataset]
        self.walletA = walletA
        self.walletB = walletB
        self.analysis = Analysis(self.dataset)
        self.buyPosition = False
        self.sellPosition = False
        self.stopLoss = dataset[-1][3]
        self.takeProfit = dataset[-1][2]
        self.win = 0
        self.loss = 0
        self.iter = 0
        self.supports = self.analysis.getSupport()
        self.msg = ""

    def updateDataset(self, lastCandle):
        self.dataset.pop(0)
        self.dataset.append([float(x) for x in lastCandle])
        self.analysis.setCandles(self.dataset)

    def priceAction(self, support):
        currentCandle = self.dataset[-1]
        prevCandle = self.dataset[-2]
        for s in support:
            if prevCandle[3] <= s and currentCandle[1] > s:
                return True
        return False

    def getSupports(self):
        self.analysis.setCandles(self.dataset)
        self.supports = self.analysis.getSupport()
        return self.supports
        
    def makeDecision(self, candle):
        self.updateDataset(candle)
        candles = self.dataset
        price = candles[-1][1]
        if (self.iter % 10 == 0):
            self.supports = self.analysis.getSupport()
        if self.buyPosition == False and self.priceAction(self.supports):
            self.msg = str(self.analysis.trendRate())
            self.takeProfit = price + (price * 0.01)
            self.stopLoss = price - (price * 0.01)
            self.buyPosition = True
        elif self.buyPosition == True:
            if price > self.takeProfit:
                self.win += 1
                #print(self.msg)
                print(datetime.fromtimestamp(int(candle[0])/1000), "\033[32m WIN\033[39m")
                self.buyPosition = False
            elif price < self.stopLoss:
                self.loss += 1
                #print(self.msg)
                print(datetime.fromtimestamp(int(candle[0])/1000), "\033[31m LOSS\033[39m")
                self.buyPosition = False
        #drawChart(self.dataset[-15:])
        #sleep(1)
        self.iter += 1
