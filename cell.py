from cell_operation import CellOperation
from typing import TypeAlias
import random

from filters import Filter, empty

Word:TypeAlias = list[str]
Filter:TypeAlias = list[str] 

class Cell:
    name: str
    operation: CellOperation
    population: list[Word]

    # FILTROS:
    # None -> Doesn't filter anything
    # dict[int, set[str]] -> key: length of the rules, subword or symbol of the filter
    inFilter :  Filter
    outFilter:  Filter

    connections: list["Cell"]

    def __init__(self, name, population=None, operation=None, inFilter=empty, outFilter=empty,  connections=None):
        self.name = name
        self.population = population if population!= None else []
        self.operation = operation; operation.population = self.population

        self.inFilter = inFilter
        self.outFilter = outFilter

        self.connections = connections if connections!=None else []

    def simulation_tick(self)->str:
        if len(self.population) <= 0: return f"{self.name}: no operation: no population in this cell"
        trace = random.choice([self.exit, self.operation.apply])()
        return f"{self.name}: {trace}"
    
    def enter(self, word):
        if self.inFilter(word):
            self.population.append(word)
            return f"entered in cell {self.name}"
        else:
            return f"deleted in cell {self.name}"

    def exit(self):
        # Get the indexes of the words that can exit the cell
        out_idxs = []
        for idx, word in enumerate(self.population):
            if self.outFilter(word):
                out_idxs.append(idx)

        # Select the word that will go out
        if len(out_idxs) <= 0: return f"no move: no word can pass the output filter"
        idx = random.choice(out_idxs)
        word = self.population.pop(idx)
        trace = random.choice(self.connections).enter(word)

        return f"move: {word} {trace}"

    def __repr__(self):
        rep = f"== {self.name} ==\n\n"

        rep += repr(self.operation)

        rep += "POPULATION:\n"
        for word in self.population:
            rep += "".join(word) + "\n"
        rep += "\n"

        rep += f"[>>] INPUT FILTER:\n{self.inFilter}\n\n"

        rep += f"[<<] OUTPUT FILTER:\n{self.outFilter}\n\n"

        rep += "CONNECTIONS:\n"
        for cell in self.connections:
            rep += cell.name + "\n"

        return rep




### TEST #################################################################################
def _test():
    from cell import Cell
    from filters import permited, excluded
    from cell_operation import CellOperation

    # Mock operation for testing
    class MockOperation(CellOperation):
        def apply(self):
            return "mock operation applied"
        
        def __repr__(self):
            return "MockOperation"

    # Create two cells connected to each other
    cell1 = Cell(
        name="Cell1",
        operation=MockOperation(),
        inFilter=permited({'a', 'b'}),
        outFilter=excluded({'x', 'y'})
    )

    cell2 = Cell(
        name="Cell2",
        operation=MockOperation(),
        inFilter=permited({'a', 'b'}),
        outFilter=excluded({'x', 'y'})
    )

    # Connect the cells
    cell1.connections = [cell2]
    cell2.connections = [cell1]

    # Test 1: Verify word entry with valid input
    print("Test 1 - Valid entry:")
    result = cell1.enter(['a', 'b'])
    print(result)
    print("Cell1 population:", cell1.population)
    print("Cell2 population:", cell2.population)

    # Test 2: Verify word exit and transfer
    print("\nTest 2 - Valid exit:")
    exit_result = cell1.exit()
    print(exit_result)
    print("Cell1 population after exit:", cell1.population)
    print("Cell2 population after exit:", cell2.population)

    # Test 3: Simulation tick
    print("\nTest 3 - Simulation tick:")
    tick_result = cell1.simulation_tick()
    print(tick_result)


def _test2():
    from cell import Cell
    from filters import permited, excluded
    from cell_operation import CellOperation

    # Mock operation for testing
    class MockOperation(CellOperation):
        def apply(self):
            return "mock operation applied"
        
        def __repr__(self):
            return "MockOperation"

    # Create two cells connected to each other
    cell1 = Cell(
        name="Cell1",
        operation=MockOperation(),
        inFilter=permited({'a', 'b'}),
        outFilter=excluded({'x', 'y'}),
        population=[["c","d"]]
    )

    cell2 = Cell(
        name="Cell2",
        operation=MockOperation(),
        inFilter=permited({'a', 'b'}),
        outFilter=excluded({'x', 'y'})
    )

    # Connect the cells
    cell1.connections = [cell2]
    cell2.connections = [cell1]

    print(cell1.exit())

if __name__ == "__main__": _test2()