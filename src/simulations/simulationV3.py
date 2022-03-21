from datetime import datetime
from src.lib.Analysis import Analysis

def simulation(dataset, walletA, walletB):
    analysis1M = Analysis(dataset)
    walletUSDT = walletA
    walletCHZ = walletB
    stopLoss = 0
    takeProfit = 0
    risk = 1
    win = 0
    loss = 0
    msg = ""
    lossRate = 0
    winRate = 0
    support = analysis1M.getSupport()[::-1][0:3]
    for i in range(25, len(dataset)):
        price = float(dataset[i][1])
        if i > 50 and walletUSDT == 0:
            for s in range(1, len(support) - 1):
                if (float(dataset[i][4]) < support[s] and float(dataset[i - 1][1]) > support[s]):
                    walletUSDT = walletCHZ * price
                    walletCHZ = 0
                    stopLoss = price + (price * 0.01)
                    takeProfit = price - (price * 0.02)
                    break

        if walletUSDT > 0:
            if takeProfit >= float(dataset[i][2]):
                
                walletCHZ = walletUSDT / takeProfit
                walletUSDT = 0
                win += 1
                #system("clear")
                print(datetime.fromtimestamp(int(dataset[i][0])/1000))
                print(msg, "\033[32mWIN\033[39m")
                #sleep(1)
                winRate += 1
                risk = 1
            elif stopLoss <= float(dataset[i][3]):
                walletCHZ = walletUSDT / stopLoss
                walletUSDT = 0
                loss += 1
                #print(msg)
                #system("clear")
                print(datetime.fromtimestamp(int(dataset[i][0])/1000))
                print(msg, "\033[31mLOSS\033[39m")
                #sleep(1)
                lossRate += 1
                if (risk < 1):
                    risk = risk * 2

    #print("TAUX DE REUSSITE = " + str(round(win / (win + loss) * 100)) + "%")
    #print("NOMBRE DE TRADE = " + str(win + loss))
    #print(str(round(walletB + (walletA * float(dataset[len(dataset) - 1][1])), 2)) + " USDT")
    #print("END")
    return [round(walletUSDT, 2), round(walletCHZ, 2), winRate, lossRate]