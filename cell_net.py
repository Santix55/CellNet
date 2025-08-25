from cell import Cell
from math import inf
from time import time
import random
from datetime import datetime, timedelta

class CellNet:
    cells: list[Cell]

    def __init__(self, cells): self.cells = cells

    def run(self, ticks=inf, seconds=inf):
        if ticks==inf and seconds==inf: raise "You have to at least specify a number of ticks or seconds"

        current_tick = 0; start_time = time(); trace = ""; diff_time = -1
        while current_tick < ticks and diff_time < seconds:
            cell = random.choice(self.cells)
            trace += cell.simulation_tick() + "\n"
            current_tick += 1; diff_time = time() - start_time
            
        return trace
        
    def __repr__(self):
        rep = ""
        for i ,cell in enumerate(self.cells):
            rep += f"{cell}\n"
        return rep
    
    def getCell(self, name):
        for cell in self.cells:
            if cell.name == name: return cell