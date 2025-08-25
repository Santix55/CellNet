from typing import TypeAlias
Word: TypeAlias = list[str]

class CellOperation:
    population: list[str]

    def __init__(self, population=None):
        self.population = population if population!=None else []

    def apply()->str: 
        raise "Abstract method not implemented for this class" 
        return "! NO CELL OPERATION"

    def __repr__(self) ->str : 
        raise "Abstract method not implemented for this class" 
        return " ! NO CELL OPERATION"