import json
from src.simulations.simulationV5 import SimulationV5

candlesM1 = json.loads(open("dataset1M.json", "r").read())
simulation = SimulationV5(candlesM1[0:500], 0, 100)
for i in range(500, len(candlesM1)):
    simulation.makeDecision(candlesM1[i])

print("TAUX DE REUSSITE {}%".format(int(round(simulation.win / (simulation.win + simulation.loss), 2) * 100)))
print("NOMBRE DE TRADE = {}".format(simulation.win + simulation.loss))
print(round(simulation.walletA, 2), round(simulation.walletB, 2))