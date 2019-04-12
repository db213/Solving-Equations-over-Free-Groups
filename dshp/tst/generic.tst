# Two variable test, non trivial constants
# i*x1*j*x2*i = 1
gap> f := FreeGroup( "i", "j" );; constants := [f.1, f.2, f.1];;
gap> LinearEquationSolutions( constants );
[ [ <identity ...>, j^-1*i^-2 ], [ j^-1, i^-2 ], [ i^-1, j^-1*i^-1 ], 
  [ i^-1*j^-1, i^-1 ], [ i^-2*j^-1, <identity ...> ], [ i^-2, j^-1 ] ]

# One variable test, exactly one solution
# i*x*j = 1
gap> f := FreeGroup( "i", "j" );; constants := [f.1, f.2];;
gap> LinearEquationSolutions( constants );
[ [ i^-1*j^-1 ] ]

# One variable test, one trivial constant
# i*x = 1
gap> f := FreeGroup( "i", "j" );; constants := [f.1, f.2 * f.2^-1];;
gap> LinearEquationSolutions( constants );
[ [ i^-1 ] ]

# Two variable test, middle constant trivial
# i*x1*x2*j = 1
gap> f := FreeGroup( "i", "j" );; constants := [f.1, f.2 * f.2^-1, f.2];;
gap> LinearEquationSolutions( constants );
[ [ <identity ...>, i^-1*j^-1 ], [ i^-1, j^-1 ], 
  [ i^-1*j^-1, <identity ...> ] ]

# Three constants, three variables
# i*x1*j*x2*k*x3 = 1
gap> f := FreeGroup( "i", "j", "k" );; constants := [f.1, f.2, f.3, f.1*f.1^-1];;
gap> solutions := LinearEquationSolutions( constants );;
gap> for solution in solutions do
>        if not CheckLinearEquationSolution( constants, solution ) then
>            Error( "error" );
>        fi;
>    od;

# Long equation, check all of the results are valid solutions
# iji^-1*x1*j^3*x2*i*x4*x5*i^-3 = 1
gap> f := FreeGroup( "i", "j" );;
gap> constants := [f.1*f.2*f.1^-1, f.2^3, f.1, f.1*f.1^-1, f.1^-3];;
gap> solutions := LinearEquationSolutions( constants );;
gap> for solution in solutions do
>        if not CheckLinearEquationSolution( constants, solution ) then
>            Error( "error" );
>        fi;
>    od;

# Long equation with trivial outer values, check all results are valid solutions
# x1*j^3i^2*x2*i*x3*ij^4*x4*i^-3*x5 = 1
gap> f := FreeGroup( "i", "j" );;
gap> constants := [f.1*f.1^-1, f.2^3*f.1^2, f.1, f.1*f.2^4, f.1^-3, f.2*f.2^-1];;
gap> solutions := LinearEquationSolutions( constants );;
gap> for solution in solutions do
>        if not CheckLinearEquationSolution( constants, solution ) then
>            Error( "error" );
>        fi;
>    od;
