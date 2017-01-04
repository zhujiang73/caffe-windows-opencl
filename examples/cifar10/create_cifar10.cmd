@echo off

set  TOOLS=.\mingw\tools

set  EXAMPLE=.\examples\cifar10
set  DATA=.\data\cifar10
set  DBTYPE=lmdb

echo "Creating $DBTYPE..."

.\mingw\examples\cifar10\convert_cifar_data.exe  %DATA%  %EXAMPLE%  %DBTYPE%

echo "Computing image mean..."

%TOOLS%\compute_image_mean.exe  -backend=%DBTYPE%  %EXAMPLE%\cifar10_train_%DBTYPE%  %EXAMPLE%\mean.binaryproto

echo "Done."


