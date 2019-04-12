#
# dshp: Daphne's Senior Honours Project
#
# Declarations
#
#! @Chapter Linear Equations over Free Groups
#! @Section Solving Linear Equations
#! @Arguments constants
#! @Returns list of solutions
#! @Description
#! Finds all solutions to a linear equation. Linear equation is given
#! as a list of the constants, when the equation is in the form
#! a1(x1)a2(x2)...an(xn) = 1
#! where a1...an are the <A>constants</A> and x1...xn are variables.
#! @BeginExample
#! f := FreeGroup( "i", "j" );
#! consts := [ f.1, f.2, f.1 ];
#! GetSolutions(consts);
#! [ [ <identity ...>, j^-1*i^-2 ], [ j^-1, i^-2 ], [ i^-1, j^-1*i^-1 ],
#!   [ i^-1*j^-1, i^-1 ], [ i^-2*j^-1, <identity ...> ], [ i^-2, j^-1 ] ]
#! @EndExample
#!
DeclareGlobalFunction( "LinearEquationSolutions" );

#! @Arguments constants, solution
#! @Returns boolean of whether or not the solution solves the equation given
#! @Description
#! Checks whether a <A>solution<\A> (a list of values for each variable, as they
#! occur in the equation) is valid in an equation (given by a list of constants
#! with a variable assumed to be in between each pair of sequential elements in
#! the list).
#! @BeginExample
#! f := FreeGroup( "i", "j" );
#! consts := [ f.1, f.2, f.1 ];
#! solutions := LinearEquationSolutions( consts );
#! CheckLinearEquationSolution( consts, solutions[1] );
#! true
#! @EndExample
#!
DeclareGlobalFunction( "CheckLinearEquationSolution" );