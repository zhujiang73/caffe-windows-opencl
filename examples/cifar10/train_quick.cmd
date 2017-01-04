@echo off

set  time01=%time%
set  TOOLS=.\mingw\tools

%TOOLS%\caffe.exe  train --solver=.\examples\cifar10\cifar10_quick_solver.prototxt 

REM @ping 127.0.0.1 -n 3 -w 1000 > nul

%TOOLS%\caffe.exe  train --solver=.\examples\cifar10\cifar10_quick_solver_lr1.prototxt  --snapshot=.\examples\cifar10\cifar10_quick_iter_4000.solverstate

set  time02=%time%

echo time start: %time01%
echo time end:   %time02%

