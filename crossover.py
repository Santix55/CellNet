from cell_operation import CellOperation
import random

from typing import TypeAlias

Word: TypeAlias = list[str]

class Crossover(CellOperation):
    def apply(self):
        
        if len(self.population) <= 0: return "no crossover: empty population in this cell"

        wordA = random.choice(self.population)
        wordB = random.choice(self.population)

        ''' # SINGLE CHILD CROSSOVER (+memory efficent, -combinations)
        idxA = random.randint(0, len(wordA)-1)
        idxB = random.randint(0, len(wordB)-1)

        #print("prefix", wordA[:idxA])
        #print("sufix", wordB[idxB:])

        child = wordA[:idxA]+wordB[idxB:]
        self.population.append(wordA[:idxA]+wordB[idxB:])

        return f"crossover: {wordA} + {wordB} -> {child}"
        '''

        # MULTIPLE CHILD CROSSOVER
        prefixesA, sufixesA = _get_prefixes_and_sufixes(wordA)
        prefixesB, sufixesB = _get_prefixes_and_sufixes(wordB)

        self.population.extend(_merge(prefixesA, sufixesB))
        self.population.extend(_merge(prefixesB, sufixesA))

        return f"crossover: {wordA} + {wordB}"

    def __repr__(self):
        return "CROSSOVER\n\n"


def _get_prefixes_and_sufixes(word):
    prefixes = []; sufixes = []
    for i in range(len(word)+1):
        prefixes.append(word[:i]); sufixes.append(word[i:])
    sufixes.pop() # remove the last []
    return (prefixes, sufixes)
    
def _merge(prefixes, sufixes):
    childs = []
    for prefix in prefixes:
        for sufix in sufixes:
            childs.append(prefix+sufix)
    return childs
    
### TEST #################################################################################
    
def _test():
    crossover = Crossover(population=[["a","b","c"],["A","B","C"]])
    print(crossover)
    print(crossover.apply())
    print(crossover.population)
    crossover.population[2][0] = "X" # prove if exist reference copy problem
    print(crossover.population)
    
if __name__ == "__main__":
    _test()