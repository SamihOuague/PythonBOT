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
        bottom = float(dataset1M[0][3])
        top = float(dataset1M[0][2])
        for i in range(0, len(dataset1M)):
            if (float(dataset1M[i][3]) < bottom):
                bottom = float(dataset1M[i][3])
            elif (float(dataset1M[i][2]) > top):
                top = float(dataset1M[i][2])
        if bottom < top:
            index = range(round(bottom * 10000), round(top * 10000))
        else:
            index = range(round(top * 10000), round(bottom * 10000))
        support = []
        for i in index:
            price = i/10000
            nbr = 0
            for c in dataset1M:
                if price <= float(c[2]) and price >= float(c[3]):
                    nbr += 1
            support.append((price, nbr))
        zone = []
        for i in range(0, len(support)):
            if (support[i][1] > 10 and support[i][1] < 50):
                current = round(support[i][0]*10000)   
                zone.append(current/10000)
        arrTmp = []
        nZone = []
        for i in range(0, len(zone)):
            if not round(zone[i], 3) in arrTmp:
                arrTmp.append(round(zone[i], 3))
                nZone.append(zone[i])
        return nZone

    def getRSI(self, period = 14, pos = 0):
        candles = self.candles[(pos - period):pos]
        avgH = []
        avgL = []
        for i in range(1, len(candles)):
            current = candles[i]
            prev = candles[i - 1]
            diff = float(prev[4]) - float(current[4])
            if diff < 0:
                avgH.append(-1 * float(diff))
                avgL.append(0)
            else:
                avgL.append(float(diff))
                avgH.append(0)
        if (sum(avgH) > 0):
            avgH = sum(avgH)/len(avgH)
        else:
            avgH = 0
        if (sum(avgL) > 0):
            avgL = sum(avgL)/len(avgL)
        else:
            avgL = 0
        if avgH == 0 and avgL == 0:
            return 0
        return round((avgH/(avgL + avgH)) * 100)
    