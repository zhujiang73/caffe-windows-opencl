#!/usr/bin/env python

import numpy as np
import os
import sys
import argparse
import glob
import time
import copy

import StringIO
from   collections import OrderedDict

import sys
sys.path.append('c:\\mingw\\python')
print(sys.path)

import caffe
import matplotlib.pyplot as plt
from   skimage import transform as sktr

def print_data(str_name, data):
	s = StringIO.StringIO()
	s.write(str_name) 
	s.write(" : ")
	s.write(data) 
	s.seek(0)
	print (s.read()) 
	#s.truncate(0)

def convert_mean(binMean, npyMean):
	blob = caffe.proto.caffe_pb2.BlobProto()
	bin_mean = open(binMean, 'rb' ).read()
	blob.ParseFromString(bin_mean)
	arr = np.array( caffe.io.blobproto_to_array(blob) )
	npy_mean = arr[0]
	np.save(npyMean, npy_mean )

def show_data(str_title, data_fp, padsize=1, padval=0):
	data = copy.deepcopy(data_fp)
	
	data -= data.min()
	data /= data.max()
	# force the number of filters to be square
	n = int(np.ceil(np.sqrt(data.shape[0])))
	padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
	data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
	# tile the filters into an image
	data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
	data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
	plt.figure(str_title),plt.title(str_title)
	plt.imshow(data,cmap='gray')
	plt.axis('off')

	plt.rcParams['figure.figsize'] = (8, 8)
	# plt.rcParams['image.interpolation'] = 'nearest'
	plt.rcParams['image.cmap'] = 'gray'

def convert_full_conv(model_define,model_weight,model_define_fc,model_weight_fc):
	net = caffe.Net(model_define, model_weight, caffe.TEST)

	params = ['fc6', 'fc7', 'fc8']
	# fc_params = {name: (weights, biases)}
	fc_params = {pr: (net.params[pr][0].data, net.params[pr][1].data) for pr in params}

	net_full_conv = caffe.Net(model_define_fc, model_weight, caffe.TEST)

	params_full_conv = ['fc6-conv', 'fc7-conv', 'fc8-conv']
	# conv_params = {name: (weights, biases)}
	conv_params = {pr: (net_full_conv.params[pr][0].data, net_full_conv.params[pr][1].data) for pr in params_full_conv}

	for pr, pr_conv in zip(params, params_full_conv):
		conv_params[pr_conv][0].flat = fc_params[pr][0].flat # flat unrolls the arrays
		conv_params[pr_conv][1][...] = fc_params[pr][1]

    	net_full_conv.save(model_weight_fc)
    	print 'convert done!'
    	return net_full_conv

set_gpu = 1

if set_gpu:
	caffe.set_mode_gpu()
   	caffe.set_device(0)
   	#caffe.set_device(1)
   	caffe.select_device(0, True)
   	print("GPU mode")
else:
   	caffe.set_mode_cpu()
   	print("CPU mode")

net_file_fc=".\\data\\bvlc_caffenet_full_conv.prototxt"
caffe_model_fc=".\\data\\bvlc_caffenet_full_conv.caffemodel"

net_file=".\\data\\bvlc_reference_caffenet.prototxt"
caffe_model=".\\data\\bvlc_reference_caffenet.caffemodel"

mean_bin=".\\data\\imagenet_mean.binaryproto"
mean_npy=".\\data\\imagenet_mean.npy"

convert_mean(mean_bin, mean_npy)

imagenet_labels_filename = ".\\data\\synset_words.txt"
labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

if not os.path.isfile(caffe_model_fc):
	net_full_conv = convert_full_conv(net_file, caffe_model, net_file_fc, caffe_model_fc)
else:
	net_full_conv = caffe.Net(net_file_fc, caffe_model_fc, caffe.TEST) 

# load input and configure preprocessing
str_img_fn = ".\\imgs\\cat.jpg"
img = caffe.io.load_image(str_img_fn)

img_res = sktr.resize(img, (451, 451) )

h = img_res.shape[0]
w = img_res.shape[1]

net_full_conv.blobs['data'].reshape(1, 3, h, w)
transformer = caffe.io.Transformer({'data': net_full_conv.blobs['data'].data.shape})
transformer.set_mean('data', np.load(mean_npy).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)
# make classification map by forward and print prediction indices at each location
out = net_full_conv.forward_all(data=np.asarray([transformer.preprocess('data', img_res)]))

show_data("conv1 params", net_full_conv.params['conv1'][0].data.reshape(96*3,11,11))
      
print_data("blobs['pool5'].data.shape", net_full_conv.blobs['pool5'].data.shape)       

print ("out prob ...")
#print out['prob'][0]
print ( out['prob'][0].argmax(axis=0) )

vals = out['prob'][0].argmax(axis=0)

va_lists = []

for vas in vals:
	for va in vas:
		va_lists.append(va)

va_sets = set(va_lists)

va_name_idx_maps = {}
va_name_num_maps = {}

for va in va_sets:
	str_name = labels[va]
	va_name_idx_maps[str_name] = va

	num = 0
	for ve_tmp in va_lists:
		if (va == ve_tmp):
			num = num+1

	va_name_num_maps[str_name] = num	

va_sort_maps = OrderedDict( sorted(va_name_num_maps.iteritems(), key=lambda d:d[1], reverse = True) )	

str_names = []
for  name in va_sort_maps.keys():	
	str_names.append(name)

str_title = "net_full_conv"

# show net input and confidence map (probability of the top prediction at each location)
plt.figure(str_title),plt.title(str_title)

str_title = "img_src : %s"%(str_img_fn)
plt.subplot(2, 2, 1),plt.title(str_title)
plt.imshow(transformer.deprocess('data', net_full_conv.blobs['data'].data[0]))

plt.subplot(2, 2, 2),plt.title(str_names[0])
idx = va_name_idx_maps[ str_names[0] ]
plt.imshow(out['prob'][0, idx], plt.cm.hot)

plt.subplot(2, 2, 3),plt.title(str_names[1])
idx = va_name_idx_maps[ str_names[1] ]
plt.imshow(out['prob'][0, idx], plt.cm.hot)

plt.subplot(2, 2, 4),plt.title(str_names[2])
idx = va_name_idx_maps[ str_names[2] ]
plt.imshow(out['prob'][0, idx], plt.cm.hot)

plt.show()


