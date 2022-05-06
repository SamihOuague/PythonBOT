from datetime import datetime


class Analysis:
    def __init__(self, candles):
        self.candles = candles

    def getCandle(self, pos):
        return self.candles[pos]

    def setCandles(self, candles):
        self.candles = candles

    def mobileAverage(self, period = 7, pos = 0):
        candles = self.candles[(pos - period):pos]
        sum = 0
        for c in candles:
            sum += float(c[4])
        return round(sum/period, 4)
    
    def candleData(self, pos):
        return [float(x) for x in self.candles[pos][1:6]]

    def getSupport(self):
        dataset1M = self.candles
        lowz = {}
        supports = []
        for c in dataset1M:
            try:
                lowz[c[3]] += 1
            except KeyError:
                lowz[c[3]] = 1

        for l in lowz:
            if (lowz[l] > 8):
                supports.append(l)
        return supports

    def trendRate(self, period = 14):
        candles = self.candles
        diffCandles = [(x[4] * 10000) - (x[1] * 10000) for x in candles[-1 * (period):]]
        return sum(diffCandles)
    