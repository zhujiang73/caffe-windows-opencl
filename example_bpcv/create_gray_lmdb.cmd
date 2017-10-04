set  TOOLS=c:\mingw\bin

%TOOLS%\convert_imageset.exe  --gray  --resize_height=120  --resize_width=120  ..\images\scenes_train\  .\data\train.txt  .\train_lmdb

%TOOLS%\convert_imageset.exe  --gray  --resize_height=120  --resize_width=120  ..\images\scenes_test\   .\data\val.txt    .\test_lmdb


