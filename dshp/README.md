# The GAP package dshp

DSHP: Stands for Daphne's Senior Honours Project. A GAP package for finding solutions to linear equations over freely presented groups.


## Contact
My GitHub username is db213.

## Usage
Copy the package into the `pkg` directory of your GAP installation. Then load it during your GAP session. Example usage:

```
gap> f := FreeGroup( "i", "j" );;
gap> consts := [ f.1, f.2, f.1 ];;
gap> GetSolutions(consts);
     [ [ <identity ...>, j^-1*i^-2 ], [ j^-1, i^-2 ], [ i^-1, j^-1*i^-1 ],
       [ i^-1*j^-1, i^-1 ], [ i^-2*j^-1, <identity ...> ], [ i^-2, j^-1 ] ]
```

## License
GNU General Public License v2
