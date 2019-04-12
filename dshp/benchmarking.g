#
# dshp: Daphne's Senior Honours Project
#
# Declarations
#
#! @Chapter Linear Equations over Free Groups
#! @Section Solving Linear Equations
#! @Arguments the variable to vary, the minimum value, maximum value,
#! the increment, the fixed values of the other two variables
#! @Returns nothing - outputs to .csv file
#! @Description
#! Variable must be one of "constSize", "alphabetSize", or "noVars"
#! otherwise nothing will happen. For alphabetSize and constSize, the
#! increment is used multiplicitively. For noVars, it's used additively.
#! For each step between min and max of the increment, a random equation
#! is generated and then solved. The time it takes to find all the
#! is written to a CSV file named {variable}_{min}_{max}_{fixed1}_{fixed2}.
#! @BeginExample
#! BenchmarkLinearEquationSolution( "constSize", 1, 4, 2, 2, 2 );
#! @EndExample
#!
BenchmarkLinearEquationSolution := function( variable, min, max, increment, fixed1, fixed2 )
# Order for fixed1 and 2: constant size, alphabet size, number of variables
local GenerateConstant, GenerateFreeGroup, GenerateEquation, j, 
    out, constSize, alphabetSize, noVars, Run, name;

    GenerateFreeGroup := function( alphabetSize )
        local generators, i;
        generators := [];
        for i in [1..alphabetSize] do
            Add(generators, String( i ) );
        od;
        return FreeGroup( generators ); 
    end;

    GenerateConstant := function( size, f )
        local i, const, generators, source, genCopy;
        source := RandomSource( IsMersenneTwister );
        const := f.1 * Inverse( f.1 );
        generators := GeneratorsOfGroup( f );
        genCopy := [];
        for i in [1..Length( generators )] do
            Add( genCopy, generators[i] );
            Add( genCopy, Inverse( generators[i] ) );
        od;
        while Length( const ) < size do
            const := const * Random( source, generators );
        od;
        return const;
    end;

    GenerateEquation := function( constSize, alphabetSize, noVars )
        local i, constants, const, f;
        constants := [];
        f := GenerateFreeGroup( alphabetSize );
        for i in [0..noVars] do
            const := GenerateConstant( constSize, f );
            Add(constants, const);
        od;
        return constants;
    end;

    Run := function( constSize, alphabetSize, noVars, out )
        local equation, start, stop, solutions;
        equation := GenerateEquation( constSize, alphabetSize, noVars );
        start := NanosecondsSinceEpoch() / 1000;
        solutions := LinearEquationSolutions( equation );
        stop := NanosecondsSinceEpoch() / 1000;
        PrintTo( out, String( stop - start ) );
        PrintTo( out, "," );
        PrintTo( out, String( Length( solutions ) ) );
        PrintTo( out, "\n" );
    end;

    j := min;
    name := Concatenation( Concatenation( Concatenation( Concatenation( Concatenation( Concatenation( 
        Concatenation( Concatenation( Concatenation( variable, "_" ), String( min ) ), "_" ), 
        String( max ) ), "_" ), String( fixed1 ) ), "_" ), String( fixed2 ) ), ".csv" );
    out := OutputTextFile( name, true );
    if variable = "constSize" then
        PrintTo( out, "constSize,time,numSolutions\n" );
        while j <= max do
            constSize := j;
            alphabetSize := fixed1;
            noVars := fixed2;
            PrintTo( out, String( j ) );
            PrintTo( out, "," );
            Run( constSize, alphabetSize, noVars, out );
            j := j * increment;
        od;
    elif variable = "alphabetSize" then
        PrintTo( out, "alphabetSize,time,numSolutions\n" );
        while j <= max do
            constSize := fixed1;
            alphabetSize := j;
            noVars := fixed2;
            PrintTo( out, String( j ) );
            PrintTo( out, "," );
            Run( constSize, alphabetSize, noVars, out );
            j := j * increment;
        od;
    elif variable = "noVars" then
        PrintTo( out, "noVars,time,numSolutions\n" );
        while j <= max do
            constSize := fixed1;
            alphabetSize := fixed2;
            noVars := j;
            PrintTo( out, String( j ) );
            PrintTo( out, "," );
            Run( constSize, alphabetSize, noVars, out );
            j := j + increment;
        od;
    fi;
end;