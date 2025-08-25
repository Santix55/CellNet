from dataclasses import dataclass
from typing import TypeAlias

Word:TypeAlias = list[str]

@dataclass
class Grammar:
    rules: dict[str,Word]
    startSym: str
    symbols: dict[str]

def parse(code: str):
    code.replace(" ",""); code.replace("\t","")

    rules = dict(); symbols = set()
    for i, line in enumerate(code.splitlines()):
        if line == "": continue

        try: non_terminal, productions_code = line.split("->", 1)
        except: raise f"Error in line {i+1}: Every not empty line have to contain the symbol '->' "

        if len(rules.keys()) == 0: startSym = line[0]
        symbols.add(non_terminal) 

        # Add non-terminals as dict key
        if len(non_terminal) != 1: raise f"Error in line {i+1}: Every symbol must be one character long"
        if not non_terminal in rules: rules[non_terminal] = []

        # Add production rules as dict value
        productions = productions_code.split('|')
        for production in productions:
            word = list(production)
            rules[non_terminal].append(word)
            for sym in word:
                symbols.add(sym)

    return Grammar(rules, startSym, symbols)

def parseFile(nameFile) -> Grammar:
    with open(nameFile, "r", encoding="utf-8") as file:
       return parse(file.read())

### TEST ########################################################################################################
def _test():
    g: Grammar = parseFile("test.grammar")
    print("rules: ", g.rules)
    print("symbols:", g.symbols)


if __name__ == "__main__":
    _test()