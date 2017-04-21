#!/usr/bin/env python

import numpy as np
import os
import sys
import glob
import time
import copy

import sys
sys.path.append('c:\\mingw\\python')
print(sys.path)

import caffe
import matplotlib.pyplot as plt
from   skimage import transform as sktr

def print_data(str_name, data):
	print ("{0} : {1}".format(str_name, data) ) 
	

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

set_gpu_mode = 0

if set_gpu_mode:
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

imagenet_labels_filename = ".\\data\\synset_words.txt"
labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

net = caffe.Net(net_file, caffe_model, caffe.TEST) 
net_full_conv = caffe.Net(net_file, caffe_model, caffe.TEST) 

# load input and configure preprocessing
str_img_fn = ".\\imgs\\cat.jpg"
img = caffe.io.load_image(str_img_fn)

img_res = sktr.resize(img, (227, 227) )

h = img_res.shape[0]
w = img_res.shape[1]

net.blobs['data'].reshape(1, 3, h, w)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', np.load(mean_npy).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)
# make classification map by forward and print prediction indices at each location
out = net.forward_all(data=np.asarray([transformer.preprocess('data', img_res)]))

print_data("blobs['conv10'].data.shape", net.blobs['conv10'].data.shape)       
print_data("blobs['pool10'].data.shape", net.blobs['pool10'].data.shape)       
print_data("blobs['prob'].data.shape", net.blobs['prob'].data.shape)     

top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
print("top_k : {0}".format(top_k) )

prob_data = net.blobs['prob'].data[0]
print ("caffe prob : ")

top_idxs = []
top_names = []
for i in np.arange(top_k.size):
    	print("idx_%d : %f, %s" %( top_k[i], prob_data[top_k[i]], labels[top_k[i]] ) )
	top_idxs.append(top_k[i])
	top_names.append(labels[top_k[i]])

print("heatmap ...... ")

img_res = sktr.resize(img, (451, 451) )

h = img_res.shape[0]
w = img_res.shape[1]

start = time.time()
net_full_conv.blobs['data'].reshape(1, 3, h, w)
transformer = caffe.io.Transformer({'data': net_full_conv.blobs['data'].data.shape})
transformer.set_mean('data', np.load(mean_npy).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)
# make classification map by forward and print prediction indices at each location
out = net_full_conv.forward_all(data=np.asarray([transformer.preprocess('data', img_res)]))
print("Caffe net forward in %.2f s." % (time.time() - start))
 
#show_data("conv1 params", net_full_conv.params['conv1'][0].data.reshape(64*3,3,3))
#print_data("blobs['fire7/concat'].data.shape", net_full_conv.blobs['fire7/concat'].data.shape)       
#print_data("blobs['fire8/concat'].data.shape", net_full_conv.blobs['fire8/concat'].data.shape)       
#print_data("blobs['fire9/concat'].data.shape", net_full_conv.blobs['fire9/concat'].data.shape)       
print_data("blobs['conv10'].data.shape", net_full_conv.blobs['conv10'].data.shape)       
print_data("blobs['pool10'].data.shape", net_full_conv.blobs['pool10'].data.shape)       
print_data("blobs['prob'].data.shape", net_full_conv.blobs['prob'].data.shape)     

fulconv_data = net_full_conv.blobs['conv10'].data
#fulconv_data = net_full_conv.blobs['pool10'].data

print ("fulconv_data ...")
#print fulconv_data[0]
#print (fulconv_data[0].argmax(axis=0) )

str_title = "net_full_conv"

# show net input and confidence map (probability of the top prediction at each location)
plt.figure(str_title),plt.title(str_title)
#plt.axis('off')

idx_fn = str_img_fn.rfind("\\")
str_title = "image: {0}".format(str_img_fn[idx_fn+1:])

plt.subplot(2, 2, 1),plt.title(str_title)
plt.imshow(transformer.deprocess('data', net_full_conv.blobs['data'].data[0]))
plt.axis('off')

plt.subplot(2, 2, 2),plt.title(top_names[0])
idx = top_idxs[0]
plt.imshow(fulconv_data[0, idx], plt.cm.hot)
plt.axis('off')

plt.subplot(2, 2, 3),plt.title(top_names[1])
idx = top_idxs[1]
plt.imshow(fulconv_data[0, idx], plt.cm.hot)
plt.axis('off')

plt.subplot(2, 2, 4),plt.title(top_names[2])
idx = top_idxs[2]
plt.imshow(fulconv_data[0, idx], plt.cm.hot)
plt.axis('off')

plt.show()


