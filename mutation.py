from cell_operation import CellOperation
from typing import TypeAlias
import random

Word:TypeAlias = list[str]

class Mutation(CellOperation):
    population: list[Word]
    rules: dict[str, list[str]]

    def __init__(self, rules:dict[str, list[str]], population:list[Word]=None):
        self.rules = rules
        super().__init__(population)

    def apply(self) -> str:
        if len(self.population) <= 0: return "no mutation: empty population in this cell"

        idxW = random.randint(0, len(self.population) - 1)
        word = self.population[idxW]
        repr_prev = repr(word)

        posible_replacements = []
        for idxS, symbol in enumerate(word):
            if symbol in self.rules:
                posible_replacements.extend([(idxS, newSymbol) for newSymbol in self.rules[symbol]])
        
        if len(posible_replacements) <= 0: return f'no mutation: no posible replacement for the word {word}'

        idxS, newSymbol = random.choice(posible_replacements)
        self.population[idxW][idxS] = newSymbol

        return f'mutation: {repr_prev} -> {self.population[idxW]}'

    def __repr__(self):
        rep = "MUTATION\n"
        for inSym, outSyms in self.rules.items():
            for outSym in outSyms:
                rep += inSym+ "->" + outSym+ "\n"
        rep += "\n"
        return rep
    
### TEST #################################################################################

def _test():
    print("\nTEST")
    population = [["a","b","a","b","a"], ["b", "a", "b", "a", "b", "a"]]
    rules = {
        "a": ["A","á"],
        "b": ["B"]
    }
    mutation = Mutation(rules, population)
    print(mutation)

    print(population)
    print(mutation.apply())
    print("after mutation")
    print(population)


if __name__ == "__main__":
    _test()