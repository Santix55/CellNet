from cell_net import CellNet
from cell import Cell
from crossover import Crossover; from mutation import Mutation
from filters import excluded, permited, Filter
from itertools import chain

from parser import Grammar, parse, parseFile

def compile(grammar: Grammar) -> CellNet:
    N = set(grammar.rules.keys())  # non-terminals
    T = grammar.symbols - N        # terminals

    H  = set([f"[^{n}]" for n in N])               # *hatted* non-terminals (auxiliar symbols)
    TN = set([f"[{t}{n}]" for n in N for t in T])  # [terminals non-terminals]

    V = N|T|H|TN    # vocabulary

    VV = Filter(lambda word: len(word) >= 2, "VV")  # VV filter: the word at least have to be 2 symbols long

    def permited_input_3(word):
        permited_subowords = set([(f"[{a}{A}]",f"[^{A}]") for A in N for a in T])
        for i in range(len(word)-1):
            if (word[i], word[i+1]) in permited_subowords: return True
        return False

    PI3 = Filter(permited_input_3, "{[aA]Â : a ∈ T ∧ A ∈ N}")

    P = {}  # productions A->[Bc] or A->a
    for inSym, outWords in grammar.rules.items():
        for word in outWords:
            word_str = "".join(word)
            if len(word)>=2: word_str = "["+word_str+"]"
            if inSym not in P: P[inSym] = []
            P[inSym].append(word_str)
    
    #            {[aA] → a ∶ A ∈ N ∧ a ∈ T}      ∪     {Â → A ∶ A ∈ N}
    M3 = {f"[{a}{A}]":[a] for A in N for a in T} | {f"[^{A}]":[A] for A in N}

    N1 = Cell(
        name = "N1",
        operation = Mutation(P),
        population = [[grammar.startSym]],
        inFilter = excluded(TN|H),
        outFilter = permited(TN)
    )

    N2 = Cell(
        name = "N2",
        operation = Crossover(),
        population = [[h] for h in H],
        inFilter = permited(TN),
        outFilter = VV|permited(V-H)
    )

    N3 = Cell(
        name = "N3",
        operation = Mutation(M3),
        population = [],
        inFilter = PI3,
        outFilter = excluded(TN|N) 
    )

    N1.connections = [N2, N3]
    N2.connections = [N1, N3]
    N3.connections = [N1, N2]

    return CellNet([N1, N2, N3])

def compileFile(name_file):
    return compile(parseFile(name_file))

def compileCode(code):
    return compile(parse(code))

### TEST #########################################################

def _test():
    cellnet = compileFile("test.grammar")
    print(cellnet)

    print("============================================")
    print("After 100 ticks..."); open("output.txt", "w").write(cellnet.run(ticks=100)) 
    print("============================================")
    print(cellnet)
if __name__ == "__main__":
    _test()
