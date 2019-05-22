from UgolGame import UgolGame
from ConstellationGraph import CSVtoConstellationGraph

game = UgolGame(CSVtoConstellationGraph('map.csv'))
game.start()
