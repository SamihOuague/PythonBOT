from datetime import datetime
from lib.Analysis import Analysis
import json

def makeDecision(candles, pos):
    print("OK")

dataset = json.loads(open("dataset.json", "r").read())
analysis = Analysis(dataset)
nbr = len(dataset) - 15
walletADA = 0
walletUSDT = 100
price = float(dataset[0][4])
stopLoss = round(price - (price * 0.01), 4)
takeProfit = round(price + (price * 0.02), 4)
for i in range(0, nbr):
    if analysis.getRSI(14, i) == 0 and walletUSDT > 0:
        walletADA = walletUSDT/float(dataset[i][4])
        walletUSDT = 0

print(stopLoss, takeProfit)
if (walletUSDT == 0):
    walletUSDT = walletADA * float(dataset[i][4])
    walletADA = 0