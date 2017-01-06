@echo off

set  time01=%time%
set  TOOLS=.\mingw\tools

%TOOLS%\caffe.exe  train --solver=.\examples\cifar10\cifar10_quick_solver.prototxt 

set  time02=%time%

%TOOLS%\caffe.exe  train --solver=.\examples\cifar10\cifar10_quick_solver_lr1.prototxt  --snapshot=.\examples\cifar10\cifar10_quick_iter_4000.solverstate

set  time03=%time%

echo time 01:  %time01%
echo time 02:  %time02%
echo time 03:  %time03%

