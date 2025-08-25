#-------------------------------------------------------
# FILTER OBJECT-FUNCTION

class Filter:
    def __init__(self, func, repr_str=None):
        self._func = func
        self._repr = repr_str if repr_str is not None else func.__name__
        
    def __call__(self, symbols):  # symbols es una lista de símbolos
        return self._func(symbols)
        
    def __repr__(self):
        return self._repr
        
    def __and__(self, other):
        return logical_and(self, other)
        
    def __or__(self, other):
        return logical_or(self, other)

#-------------------------------------------------------
# FUNCTION FACTORIES

def logical_and(filter0, filter1):
    def _and(symbols): 
        return filter0(symbols) and filter1(symbols)
    return Filter(_and, f"({filter0!r} & {filter1!r})")

def logical_or(filter0, filter1):
    def _or(symbols): 
        return filter0(symbols) or filter1(symbols)
    return Filter(_or, f"({filter0!r} | {filter1!r})")

def permited(allowed_set):
    sorted_set = sorted(allowed_set)
    def _permited(symbols):
        for sym in symbols:
            if sym in allowed_set: 
                return True
        return False
    return Filter(_permited, f"permited({sorted_set})")

def excluded(forbidden_set):
    sorted_set = sorted(forbidden_set)
    def _excluded(symbols):
        for sym in symbols:
            if sym in forbidden_set: 
                return False
        return True
    return Filter(_excluded, f"excluded({sorted_set})")

def empty():
    def _empty(symbols):
        return True
    return Filter(_empty, "empty()")

### TEST ######
def _test():
    always_true = empty()
    
    print(always_true(['a', 'b', 'c']))  # True
    print(always_true(['1', '2', '3']))  # True
    print(always_true([]))               # True
    print(always_true(['x', 'y']))       # True

    allowed = ['a', 'b', 'c']
    filter1 = permited(allowed)
    combined = filter1 & empty()
    print(combined)

    print(combined(['a', 'b']))  # True (filter1 is True y empty is True)
    print(combined(['x', 'y']))  # False (porque filter1 is False)

def _test1():
    """Test básico de filtros con listas de símbolos"""
    print("\n=== TEST BÁSICO DE FILTROS CON LISTAS DE SÍMBOLOS ===")
    
    simbolos_permitidos = {'a', 'b', 'c'}
    simbolos_prohibidos = {'x', 'y', 'z'}
    
    permited_filter = permited(simbolos_permitidos)
    excluded_filter = excluded(simbolos_prohibidos)
    empty_filter = empty()
    
    combined_filter = permited_filter & excluded_filter
    combined_with_empty = combined_filter | empty_filter
    
    print("Created filters:")
    print(f"permited_filter: {permited_filter}")
    print(f"excluded_filter: {excluded_filter}")
    print(f"empty_filter: {empty_filter}")
    print(f"combined_filter: {combined_filter}")
    print(f"combined_with_empty: {combined_with_empty}")
    
    test_cases = [
        (['a', 'b', 'c'], "Only  permited symbols"),
        (['a', 'x', 'c'], "Contains a excluded symbol"),
        (['x', 'y', 'z'], "Only contains excluded symbols"),
        ([], "Empty list"),
    ]
    
    print("\nResultados:")
    for symbols, description in test_cases:
        print(f"\n{description} {symbols}:")
        print(f"  permited: {permited_filter(symbols)}")
        print(f"  excluded: {excluded_filter(symbols)}")
        print(f"  empty: {empty_filter(symbols)}")
        print(f"  combined: {combined_filter(symbols)}")
        print(f"  combined_with_empty: {combined_with_empty(symbols)}")

if __name__ == "__main__":
    _test1()