#
# dshp: Daphne's Senior Honours Project
#
# This file runs package tests. It is also referenced in the package
# metadata in PackageInfo.g.
#
LoadPackage( "dshp" );

TestDirectory(DirectoriesPackageLibrary( "dshp", "tst" ),
  rec(exitGAP := true));

FORCE_QUIT_GAP(1); # if we ever get here, there was an error
