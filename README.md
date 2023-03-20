# Rosette Sudoku Solver

Mini project to get familiar with Rosette (and Python code-generation). wwwww

## Experiments

```shell
❯ python3 sudoku.py > sudoku.rkt && racket sudoku.rkt
cpu time: 76 real time: 148 gc time: 11
147268359
936571824
582934671
671385492
359742168
824619735
715826943
268493517
493157286
❯ python3 sudoku_bv.py > sudoku_bv.rkt && racket sudoku_bv.rkt
cpu time: 54 real time: 144 gc time: 12
147268359
936571824
582934671
671385492
359742168
824619735
715826943
268493517
493157286
```

## Notes

Though I split the code into two versions, one uses builtin integer and the other uses bitvector, **there is no notable time difference between them**.