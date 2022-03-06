class Analysis:
    def __init__(self, candles):
        self.candles = candles

    def getCandle(self, pos):
        return self.candles[pos]

    def setCandles(self, candles):
        self.candles = candles

    def mobileAverage(self, period = 7, pos = 0):
        candles = self.candles[pos:(pos + period)]
        sum = 0
        for c in candles:
            sum += float(c[4])
        return round(sum/period, 4)

    def getRSI(self, period = 14, pos = 0):
        candles = self.candles[pos:(pos + period)]
        avgH = []
        avgL = []

        for i in range(1, len(candles)):
            current = candles[i]
            prev = candles[i - 1]
            diff = float(prev[4]) - float(current[4])
            if diff < 0:
                avgL.append(-1 * float(diff))
                avgH.append(0)
            else:
                avgH.append(float(diff))
                avgL.append(0)

        avgH = sum(avgH)/len(avgH)
        avgL = sum(avgL)/len(avgL)

        return round((avgH/(avgL + avgH)) * 100)