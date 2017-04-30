set  TOOLS=c:\mingw\bin
set  IMGSDIR=d:\caffe_net\images

%TOOLS%\convert_imageset.exe  --gray  --resize_height=115  --resize_width=115  %IMGSDIR%\places_train\  .\data\train.txt  .\train_lmdb

%TOOLS%\convert_imageset.exe  --gray  --resize_height=115  --resize_width=115  %IMGSDIR%\places_test\   .\data\val.txt    .\test_lmdb


