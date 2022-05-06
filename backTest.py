from datetime import datetime
import json
#from src.lib.Analysis import Analysis
#from os import system
#from time import sleep
from src.simulations.simulationV2 import simulation
#from src.simulations.simulationV3 import simulation
#from src.lib.Chart import drawChart
#for i in range(50, len(candles)):
#    system("clear")
#    drawChart(candles[(i-50):i])
#    sleep(1)
#simulation()

#api = BinanceAPI()
candles = json.loads(open("dataset1M.json", "r").read())
walletA = 0
walletB = 3000
i = 0
win = 0
loss = 0
while (i < len(candles)):
    c = candles[i: i+500]
    i += 500
    wallets = simulation(c, walletA, walletB)
    walletB = wallets[0:2][1] + (wallets[0:2][0] * float(c[0][1]))
    win += wallets[2]
    loss += wallets[3]

print("TAUX DE REUSSITE = ", str(round((win / (win+loss)) * 100)) + "%")
print(datetime.fromtimestamp(int(candles[0][0])/1000))
print(win + loss)
#print(str(round(walletB, 2)) + " CHZ")
print(str(round(walletB, 2)) + " USDT")
#
#for i in range(1, len(candles)):
#    if (float(candles[i][1]) > support[1] and float(candles[i - 1][1]) < support[1]):
#        print(candles[i][1])