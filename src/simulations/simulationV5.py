from datetime import datetime
from src.lib.Analysis import Analysis

class SimulationV5:
    def __init__(self, dataset, walletA, walletB):
        self.dataset = [[float(x) for x in d] for d in dataset]
        self.walletA = walletA
        self.walletB = walletB
        self.analysis = Analysis(self.dataset)
        self.buyPosition = False
        self.stopLoss = 0
        self.takeProfit = 0
        self.win = 0
        self.loss = 0
        self.risk = 1

    def updateDataset(self, lastCandle):
        self.dataset.pop(0)
        self.dataset.append([float(x) for x in lastCandle])
        self.analysis.setCandles(self.dataset)

    def priceAction(self):
        lastIndex = len(self.dataset) - 1
        lastVolume = self.dataset[lastIndex]
        for i in range(1, 3):
            v = self.dataset[lastIndex - i]
            if v[5] < lastVolume[5] and v[4] > lastVolume[4]:
                lastVolume = v
                
            else:
                return False
        return True

    def makeDecision(self, candle):
        self.updateDataset(candle)
        price = float(candle[1])
        if self.priceAction() and not self.buyPosition:
            self.takeProfit = price - (price * 0.01)
            self.stopLoss = price + (price * 0.01)
            self.walletA = (self.walletB * self.risk) * price
            self.walletB = self.walletB - (self.walletB * self.risk)
            self.buyPosition = True
        
        if self.buyPosition:
            if price <= self.takeProfit:
                print(datetime.fromtimestamp(int(candle[0])/1000), "\033[32m WIN\033[39m")
                self.walletB = self.walletA / price
                self.walletA = 0
                self.buyPosition = False
                self.risk = 1
                self.win += 1
            elif price >= self.stopLoss:
                print(datetime.fromtimestamp(int(candle[0])/1000), "\033[31m LOSS\033[39m")
                self.walletB = self.walletA / price
                self.walletA = 0
                self.buyPosition = False
                if self.risk < 1:
                    self.risk *= 2
                self.loss += 1