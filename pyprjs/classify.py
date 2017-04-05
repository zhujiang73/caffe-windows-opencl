#!/usr/bin/env python

import numpy as np
import os
import sys
import argparse
import glob
import time
import copy

import StringIO

import sys
sys.path.append('c:\\mingw\\python')
print(sys.path)

import caffe
import matplotlib.pyplot as plt

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

def show_data(str_title, data_p, padsize=1, padval=0):
	data = copy.deepcopy(data_p)
	
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

net_file=".\\data\\bvlc_reference_caffenet.prototxt"
caffe_model=".\\data\\bvlc_reference_caffenet.caffemodel"

mean_bin=".\\data\\imagenet_mean.binaryproto"
mean_npy=".\\data\\imagenet_mean.npy"

imagenet_labels_filename = ".\\data\\synset_words.txt"
labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

convert_mean(mean_bin, mean_npy)

net = caffe.Net(net_file,caffe_model,caffe.TEST)

show_data("conv1 params", net.params['conv1'][0].data.reshape(96*3,11,11))
print_data("net.params['conv1'][0].data.shape", net.params['conv1'][0].data.shape)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(mean_npy).mean(1).mean(1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))
input_data=net.blobs['data'].data

str_img_fn = ".\\imgs\\cat.jpg"
img=caffe.io.load_image(str_img_fn)

# Classify.
net.blobs['data'].data[...] = transformer.preprocess('data',img)

start = time.time()
#out = net.forward()
out = net.forward(start="conv1", end="prob")
print("Caffe net forward in %.2f s." % (time.time() - start))

show_data("conv1", net.blobs['conv1'].data[0])
print_data("net.blobs['conv1'].data.shape", net.blobs['conv1'].data.shape)   

params = [(k, v[0].data.shape) for k, v in net.params.items()]
plt.figure("img")
plt.subplot(1,2,1),plt.title("origin")
plt.imshow(img)
plt.axis('off')
plt.subplot(1,2,2),plt.title("subtract mean")
plt.imshow(transformer.deprocess('data', input_data[0]))
plt.axis('off')
  
data = [(k, v.data.shape) for k, v in net.blobs.items()]
feat = net.blobs['prob'].data[0]
#print feat
plt.figure('prob')
plt.plot(feat.flat)

top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
print("top_k : ", top_k)

prob_data = net.blobs['prob'].data[0]
print ("caffe prob : ")

for i in np.arange(top_k.size):
    	print("idx_%d : %f, %s" %( top_k[i], prob_data[top_k[i]], labels[top_k[i]] ) )

plt.show()


