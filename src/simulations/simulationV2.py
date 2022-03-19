from datetime import datetime
from src.lib.Analysis import Analysis

def simulation(dataset, walletA, walletB):
    analysis1M = Analysis(dataset)
    walletA = walletA
    walletB = walletB
    stopLoss = 0
    takeProfit = 0
    risk = 1
    win = 0
    loss = 0
    msg = ""
    lossRate = 0
    winRate = 0
    support = analysis1M.getSupport()
    for i in range(25, len(dataset)):
        price = float(dataset[i][1])
        if i > 50 and walletA == 0:
            for s in range(1, len(support) - 1):
                if (float(dataset[i][4]) > support[s] and float(dataset[i - 1][1]) < support[s]):
                    walletA = (walletB * risk) / price
                    walletB = walletB - (walletB * risk)
                    stopLoss = price - (price * 0.01)
                    takeProfit = price + (price * 0.01)
                    break

        if walletA > 0:
            if takeProfit <= float(dataset[i][2]):
                walletB = walletB + (walletA * takeProfit)
                walletA = 0
                win += 1
                #system("clear")
                print(datetime.fromtimestamp(int(dataset[i][0])/1000))
                print(msg, "\033[32mWIN\033[39m")
                #sleep(1)
                winRate += 1
                risk = 1
            elif stopLoss >= float(dataset[i][3]):
                walletB = walletB + (walletA * stopLoss)
                loss += 1
                walletA = 0
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
    return [walletA, walletB, winRate, lossRate]