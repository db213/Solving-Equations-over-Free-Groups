DSHP: a Python package for solving equations over freely presented groups.

## About
Uses Google OR-Tools constraint solver to find solutions to equations over groups.

## Usage
There are three runnable files: `benchmarking.py`, `solver`, and `tests.py`. Run using a virtual environment in which `requirements.txt` has been installed.

```
$ python -m solver -h
usage: __main__.py [-h] --equation EQUATION [--solvability] [--bound BOUND]
                   [--verbose] [--incrementbounds]

Solve equations over free groups.

optional arguments:
  -h, --help           show this help message and exit
  --equation EQUATION  The equation: constants must be in lower case and
                       variables in upper case. No numbers. Letters followed
                       by asterisks are inverted.
  --solvability        Check only if the equation is solvable.
  --bound BOUND        What bound to place on the variable size. Options are:
                       linear, orientable, nonorientable.
  --verbose            Whether the solver should print solutions.
  --incrementbounds    Whether to incrementally increase bound on variable
                       value size. Can only be true for solvability problems.
```

Benchmarking is for running timing experiments on randomly generated equations.

```
$ python benchmarking.py -h
usage: Profile constraint solver. [-h] --equation EQUATION --variable VARIABLE
                                  --min MIN --max MAX --intervaltype
                                  INTERVALTYPE --interval INTERVAL --invariant
                                  INVARIANT [--solvability] [--solvable]
                                  --bound BOUND [--savefile SAVEFILE]
                                  [--verbose] [--repetitions REPETITIONS]
                                  [--incrementbounds]

optional arguments:
  -h, --help            show this help message and exit
  --equation EQUATION   What type of equation generate. The options are:
                        linear, quadratic.
  --variable VARIABLE   The variable to vary: noVars, constSize.
  --min MIN             The minimum variable value
  --max MAX             The maximum variable value
  --intervaltype INTERVALTYPE
                        Logarithmically or linearly scale from min to max:
                        linear, logarithmic.
  --interval INTERVAL   Interval size.
  --invariant INVARIANT
                        Invariant value.
  --solvability         Run until only one solution is found.
  --solvable            Whether the equation must be solvable.
  --bound BOUND         What bound to put on variable size.
  --savefile SAVEFILE   Where to save output.
  --verbose             Whether the solver should print output.
  --repetitions REPETITIONS
                        Number of times to run same experiment.
  --incrementbounds     Whether to incrementally increase bound on variable
                        value size. Can only be true for solvability problems.
```

## License
GNU General Public License v2