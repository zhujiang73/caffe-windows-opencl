#!/usr/bin/env python

import numpy as np
import os
import sys
import argparse
import glob
import time

import sys
sys.path.append('c:\\mingw\\python')
print(sys.path)

import caffe
import matplotlib.pyplot as plt

def convert_mean(binMean,npyMean):
	blob = caffe.proto.caffe_pb2.BlobProto()
	bin_mean = open(binMean, 'rb' ).read()
	blob.ParseFromString(bin_mean)
	arr = np.array( caffe.io.blobproto_to_array(blob) )
	npy_mean = arr[0]
	np.save(npyMean, npy_mean )

def show_data(data, padsize=1, padval=0):
	data -= data.min()
	data /= data.max()
	# force the number of filters to be square
	n = int(np.ceil(np.sqrt(data.shape[0])))
	padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
	data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
	# tile the filters into an image
	data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
	data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
	plt.figure()
	plt.imshow(data,cmap='gray')
	plt.axis('off')

	plt.rcParams['figure.figsize'] = (8, 8)
	plt.rcParams['image.interpolation'] = 'nearest'
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

net_file=".\\data\\squeezenet_v1.1.prototxt"
caffe_model=".\\data\\squeezenet_v1.1.caffemodel"

mean_bin=".\\data\\imagenet_mean.binaryproto"
mean_npy=".\\data\\imagenet_mean.npy"

convert_mean(mean_bin, mean_npy)

net = caffe.Net(net_file,caffe_model,caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(mean_npy).mean(1).mean(1))
transformer.set_raw_scale('data', 255) 
transformer.set_channel_swap('data', (2,1,0))
input_data=net.blobs['data'].data

#im=caffe.io.load_image(".\\images\\cat.jpg")
#im=caffe.io.load_image(".\\images\\cat_gray.jpg")
#im=caffe.io.load_image(".\\images\\fish_bike.jpg")
#im=caffe.io.load_image(".\\images\\2007_001704.jpg")
im=caffe.io.load_image(".\\images\\blender_820.jpg")

# Classify.
net.blobs['data'].data[...] = transformer.preprocess('data',im)
start = time.time()
out = net.forward()
print("Caffe Done in %.2f s." % (time.time() - start))

data = [(k, v.data.shape) for k, v in net.blobs.items()]
#print("data")
#print(data)

params = [(k, v[0].data.shape) for k, v in net.params.items()]
#print("params")
#print(params)
plt.figure()
plt.subplot(1,2,1),plt.title("origin")
plt.imshow(im)
plt.axis('off')
plt.subplot(1,2,2),plt.title("subtract mean")
plt.imshow(transformer.deprocess('data', input_data[0]))
plt.axis('off')

show_data(net.blobs['conv1'].data[0])
print net.blobs['conv1'].data.shape
show_data(net.params['conv1'][0].data.reshape(64*3,3,3))
print net.params['conv1'][0].data.shape

feat = net.blobs['prob'].data[0]
#print feat
plt.figure(4)
plt.plot(feat.flat)

imagenet_labels_filename = ".\\data\\synset_words.txt"
labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
for i in np.arange(top_k.size):
    print top_k[i], labels[top_k[i]]

plt.show()

