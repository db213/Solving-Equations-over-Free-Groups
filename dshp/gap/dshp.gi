InstallGlobalFunction( CheckLinearEquationSolution,
function( constants, solution )
	local productSum, i;
	productSum := constants[1] * Inverse( constants[1] );
	for i in [1..Length( constants ) - 1] do
		productSum := productSum * constants[i] * solution[i];
	od;
	productSum := productSum * constants[Length( constants )];
	return productSum = constants[1] * Inverse( constants[1] );
end);

InstallGlobalFunction( LinearEquationSolutions,
function( constants )
	local i, GetOffsetPermutations, GetLeftSubval, GetRightSubval,
		GenerateVarVal, GenerateNewConstants, InsertIntoSolutions, Solve,
		seenSolutions, variables, VarValAlreadyFound, solutions,
		in_list_form, solution, one_solution;
	
	GetOffsetPermutations := function( word1, word2 )
		local offsets, k, j, permutation;
		offsets := [];
		for k in [0..Length( word1 )] do
			permutation := [k];
			for j in [0..Length( word2 )] do
				Add( permutation, j );
				Add( offsets, StructuralCopy( permutation ) );
				permutation := [k];
			od;
		od;
		return offsets;
	end;

	GetLeftSubval := function( constants, permutation, i )
		if permutation[1] = 0 then
			return constants[i] * Inverse( constants[i] );
		fi;
		return Subword( constants[i], Length(constants[i] ) - 
			permutation[1] + 1, Length( constants[i] )); 
	end;

	GetRightSubval := function( constants, permutation, i )
		if permutation[2] = 0 then
			return constants[i] * Inverse( constants[i] );
		fi;
		return Subword( constants[i + 1], 1, permutation[2] );
	end;

	GenerateVarVal := function( constants, permutation, i )
		return Inverse( GetLeftSubval( constants, permutation, i ) ) *
			Inverse( GetRightSubval( constants, permutation, i ) );
	end;

	GenerateNewConstants := function( constants, varValue, i )
		local newConstant, newConstants;
		newConstant := constants[i] * varValue * constants[i + 1];
		newConstants := StructuralCopy( constants );
		newConstants[i] := newConstant;
		Remove( newConstants, i + 1 );
		return newConstants;
	end;

	InsertIntoSolutions := function( subSolutions, varValue, i, noVars )
		local solution, subSolution, biggerSolution;
		solution := [];
		for subSolution in subSolutions do
			biggerSolution := StructuralCopy( subSolution );
			AddDictionary( biggerSolution, i, varValue );
			Add( solution, biggerSolution );
		od;
		return solution;
	end;

	VarValAlreadyFound := function( solutions, var, varValue )
		local solution;
		for solution in solutions do
			if LookupDictionary( solution, var ) = varValue then
				return true;
			fi;
		od;
		return false;
	end;

	Solve := function( constants, variables, seenSolutions )
		local allSolutions, solution, i, offsetPermutations,
			  variablesCopy, varValue, newConstants, subSolutions,
			  permutation, wrapper, position;
		if Length( constants ) <> ( Length( variables ) + 1 ) then
			Error( "Error: number of variables and constants do not " +
                    "match." );
		fi;
		if Length( constants ) = 2 then
			wrapper := [];
			solution := NewDictionary( variables[1], true );
			AddDictionary( solution, variables[1], Inverse( constants[1] ) * 
						   Inverse( constants[2] ) );
			Add( wrapper, solution );
			return wrapper;	
		fi;

		allSolutions := [];
		for i in variables do
			position := Position(variables, i);
			offsetPermutations := GetOffsetPermutations( 
                                    constants[position],
									constants[position + 1] );
			variablesCopy := StructuralCopy( variables );
			Remove( variablesCopy, position);
			for permutation in offsetPermutations do
				varValue := GenerateVarVal( constants, permutation, 
                                            position );
				if not VarValAlreadyFound( seenSolutions, i, varValue ) then
                    newConstants := GenerateNewConstants( constants, 
                                                          varValue, 
                                                          position );
                    subSolutions := Solve( newConstants, variablesCopy, 
                                            seenSolutions );
                    solution := InsertIntoSolutions( subSolutions, 
                                                     varValue, i, 
                                                     Length( variables ) - 1 );
                    Append( seenSolutions, StructuralCopy( solution  ) );
                    Append( allSolutions, StructuralCopy( solution ) );
				fi;
			od;	
		od;
		return allSolutions;
	end;

	seenSolutions := [];
	variables := [];
	for i in [1..Length(constants) - 1] do
		Add( variables, i );
	od;
	solutions := Solve( constants, variables, seenSolutions );
	in_list_form := [];
	for solution in solutions do
		one_solution := [];
		for i in [1..Length(constants) - 1] do
			Add(one_solution, LookupDictionary(solution, i));
		od;
		Add(in_list_form, one_solution);
	od;
	return in_list_form;
end);