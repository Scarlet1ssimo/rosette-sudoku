from common import *


def emit(Node):
    if isinstance(Node, Var):
        return Node.name
    if isinstance(Node, Num):
        return f"(int32 {Node.v})"
    if isinstance(Node, Neq):
        return f"(not (bveq {emit(Node.lhs)} {emit(Node.rhs)}))"
    if isinstance(Node, Sle):
        return f"(bvsle {emit(Node.lhs)} {emit(Node.rhs)})"
    if isinstance(Node, Assume):
        return f"(assume {emit(Node.pred)})"
    if isinstance(Node, Assert):
        return f"(assert {emit(Node.pred)})"
    assert False


def evaluate():
    ret = ""
    for i in unknown_list:
        ret += f"(define c{i} (bitvector->integer (evaluate {i} sol)))\n"
    return ret


def def_symbolics():
    return f"(define-symbolic {' '.join(unknown_list)} int32?)\n"


def emit_constraints():
    ret = ""
    for i in constraints:
        ret += emit(i)+"\n"
    return ret


if __name__ == "__main__":
    puzzle9()
    constraint_pipeline()
    rosette_code = """#lang rosette
    (define int32? (bitvector 32))
    (define (int32 i)
    (bv i int32?))
    """+def_symbolics()+"""(define sol
    (time (solve (begin"""+emit_constraints()+"))))\n"+evaluate()+printf()
    print(rosette_code)
