heatmaps.py  screenshot:

![](heatmaps_2008_001042.jpg)


DataSet Images:

dir d:\caffe_net\images\places_train 
2017/04/29  21:21    <DIR>          .
2017/04/29  21:21    <DIR>          ..
2017/04/30  01:25    <DIR>          cars
2017/04/30  01:32    <DIR>          fashions
2017/04/29  21:31    <DIR>          places

dir d:\caffe_net\images\places_test
2017/04/29  21:20    <DIR>          .
2017/04/29  21:20    <DIR>          ..
2017/04/30  01:25    <DIR>          cars
2017/04/30  01:32    <DIR>          fashions
2017/04/29  21:31    <DIR>          places



train caffemodel:

...\caffe-windows-opencl\hmprjs> python  lists_train.py
...\caffe-windows-opencl\hmprjs> python  lists_test.py
...\caffe-windows-opencl\hmprjs> create_gray_lmdb.cmd
...\caffe-windows-opencl\hmprjs> make_mean.cmd
...\caffe-windows-opencl\hmprjs> train_quick.cmd



heatmaps:
...\caffe-windows-opencl\hmprjs> python  heatmaps.py





