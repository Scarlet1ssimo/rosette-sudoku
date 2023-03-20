from collections import namedtuple
Var = namedtuple("Var", 'name')
Num = namedtuple("Num", 'v')
Neq = namedtuple("Neq", 'lhs rhs')
Sle = namedtuple("Sle", 'lhs rhs')
Assume = namedtuple("Assume", "pred")
Assert = namedtuple("Assert", "pred")

unknown_list = []
constraints = []
symtable = {}


def parse(p: str):
    global dim
    symtable.clear()
    l = p.split("\n")
    dim = len(l)
    for i, s in enumerate(l):
        assert len(s) == dim
        for j, c in enumerate(s):
            if c == ' ':
                std_name = f"x_{i}{j}"
                unknown_list.append(std_name)
                symtable[(i, j)] = Var(std_name)
            else:
                symtable[(i, j)] = Num(c)


def input_bound():
    for i in range(dim):
        for j in range(dim):
            obj = symtable[(i, j)]
            if isinstance(obj, Var):
                constraints.append(Assume(Sle(Num(1), obj)))
                constraints.append(Assume(Sle(obj, Num(dim))))


def row_col_constraint():
    for row in range(dim):
        for i in range(dim):
            for j in range(i+1, dim):
                obj1 = symtable[(row, i)]
                obj2 = symtable[(row, j)]
                if isinstance(obj1, Var) or isinstance(obj2, Var):
                    constraints.append(Assert(Neq(obj1, obj2)))
    for col in range(dim):
        for i in range(dim):
            for j in range(i+1, dim):
                obj1 = symtable[(i, col)]
                obj2 = symtable[(j, col)]
                if isinstance(obj1, Var) or isinstance(obj2, Var):
                    constraints.append(Assert(Neq(obj1, obj2)))


def region_constraint():
    region = {6: [
        "000111",
        "000111",
        "222333",
        "222333",
        "444555",
        "444555",
    ], 9: [
        "000111222",
        "000111222",
        "000111222",
        "333444555",
        "333444555",
        "333444555",
        "666777888",
        "666777888",
        "666777888",
    ]}[dim]
    # can be improved but fast enough
    for i1 in range(dim):
        for i2 in range(i1, dim):
            for j1 in range(dim):
                for j2 in range(j1+1, dim) if i1 == i2 else range(dim):
                    if region[i1][j1] == region[i2][j2]:
                        obj1 = symtable[(i1, j1)]
                        obj2 = symtable[(i2, j2)]
                        if isinstance(obj1, Var) or isinstance(obj2, Var):
                            constraints.append(Assert(Neq(obj1, obj2)))


def constraint_pipeline():
    constraints.clear()
    input_bound()
    row_col_constraint()
    region_constraint()


def printf():
    format_str = ""
    arg_list = []
    for i in range(dim):
        for j in range(dim):
            obj = symtable[(i, j)]
            if isinstance(obj, Num):
                format_str += obj.v
            elif isinstance(obj, Var):
                format_str += "~a"
                arg_list.append("c"+obj.name)
            else:
                assert False
        format_str += "~n"
    return f'(printf "{format_str}" {" ".join(arg_list)})'


def puzzle6():
    puzzle = """\
263 1 
4  623
5 4 61
 31 4 
 4  5 
     2"""
    parse(puzzle)


def puzzle9():
    puzzle = """\
 4  6 3 9
 3  7  2 
  29 4   
  1  54 2
3 97    8
8  6  7  
7   26 4 
 6 4  51 
 93  7   """
    parse(puzzle)
