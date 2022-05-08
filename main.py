import cv2
import tensorflow as tf
import tf.keras as keras
import numpy as np
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from keras.models import Sequential
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Reshape
from keras.layers import Conv2D
from keras.layers import UpSampling2D
from keras.layers import AveragePooling2D
from keras.layers import LeakyReLU
from keras.layers import Layer
from keras.layers import Add
from keras.constraints import max_norm
from keras.initializers import RandomNormal
from keras.layers import BatchNormalization
from keras import backend
"""there are three custom functions involved in making a progressive GAN - 
Weighted Average layer of two tensors of same dimensions
Minibatch Standard Deviation to summarize statistics for a batch of images in the discriminator
"""
class WeightedSum(tf.keras.layers.Layer):
    def __init__(self, alpha = 0.1, **kwags):
        super(WeightedSum, self).__init__()
        self.alpha = tf.keras.backend.variable(alpha, name = "ws_alpha")

    def _merge_function(self, inputs):
        # only supports a weighted sum of two inputs
        assert (len(inputs) == 2)
        # ((1-a) * input1) + (a * input2)
        output = ((1.0 - self.alpha) * inputs[0]) + (self.alpha * inputs[1])
        return output

""" Minibatch Std. Deviation algo- 

"""
import tf.keras.backend as backend
class MinibatchDev(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(MinibatchDev, self).__init__()
    def call(self, inputs):
        mean = backend.mean(inputs, axis=0, keepdims=True)
        squ_diffs = backend.square(inputs - mean)
        mean_sq_diff = backend.mean(squ_diffs, axis=0, keepdims=True)
        mean_sq_diff += 1e-8
        stdev = backend.sqrt(mean_sq_diff)
        mean_pix = backend.mean(stdev, keepdims=True)
        shape = backend.shape(inputs)
        output = backend.tile(mean_pix, (shape[0], shape[1], shape[2], 1))
        # concatenate with the output
        combined = backend.concatenate([inputs, output], axis=-1)
        return combined

    def compute_output_shape(self, input_shape):
        # create a copy of the input shape as a list
        input_shape = list(input_shape)
        # add one to the channel dimension (assume channels-last)
        input_shape[-1] += 1
        # convert list to a tuple
        return tuple(input_shape)
#define losss function
def wgan_loss(y_true, y_pred):
    return backend.mean(y_true*y_pred)
def disbase(input, dim):
    for i in range(2):
        model = Conv2D(128, (3,3), strides = 1, padding = 'same')(input)
        model = LeakyReLU(alpha=0.1)(model)
    model = AveragePooling2D()(model)
    return Model(input, model)
def add_disblock(old_model, n_input_layers = 3):
     in_shape = list(old_model.input.shape)
     try :
         #input processing layer
         input = Input(shape = in_shape)
         model1  = Conv2D(128, (1,1), padding='same', kernel_initializer=init, kernel_constraint=const)(input)
         model1 = LeakyReLU()(model1)
         model1 = disbase(model1, (in_shape[0],in_shape[1],in_shape[2]))
         """for the first step, this input processing layer will compile with the old_model. Once that's in motion, 
         we'll use the weighted average to slowly introduce the downscaling layer. As soon as we're done with this, our 
         new_model will be finished and the discriminator will be able to work with higher-res images """
         d = model1 #create a clone instance of model1
         for i in range(n_input_layers, len(old_model.layers)):
             d = old_model.layers[i](d)
         model_one = Model(input, d)
         model_one.compile(loss=wgan_loss, optimizer= Adam())
         #now we'll connect a downsampling model
         downsample = AveragePooling2D()(input)
         model2 = old_model.layers[1](downsample)
         model2 = old_model.layers[2](model2)
         d = WeightedSum()([model1, model2])
         for i in range(n_input_layers, len(old_model.layers)):
             d = old_model.layers[i](d)
         model_two = Model(input, d)
         model_two.compile(loss = wgan_loss, optimizer= Adam)
         return [model_one, model_two]
     except RecursionError as e:
         print("damn the discriminator block didn't work - add_disblock")


def define_discriminator(n_blocks, input_shape=(4,4,3)):
	init = RandomNormal(stddev=0.02)
	const = max_norm(1.0)
	model_list = list()
	in_image = Input(shape=input_shape)
	d = Conv2D(128, (1,1), padding='same', kernel_initializer=init, kernel_constraint=const)(in_image)
	d = LeakyReLU(alpha=0.2)(d)
	d = MinibatchStdev()(d)
	d = Conv2D(128, (3,3), padding='same', kernel_initializer=init, kernel_constraint=const)(d)
	d = LeakyReLU(alpha=0.2)(d)
	d = Conv2D(128, (4,4), padding='same', kernel_initializer=init, kernel_constraint=const)(d)
	d = LeakyReLU(alpha=0.2)(d)
	d = Flatten()(d)
	out_class = Dense(1)(d)
	model = Model(in_image, out_class)
	model.compile(loss=wgan_loss, optimizer=Adam(lr=0.001, beta_1=0, beta_2=0.99, epsilon=10e-8))
	model_list.append([model, model])
	for i in range(1, n_blocks):
		old_model = model_list[i - 1][0]
		models = add_disblock(old_model)
		model_list.append(models)
	return model_list

# add a generator block
def add_generator_block(old_model):
	# weight initialization
	init = RandomNormal(stddev=0.02)
	# weight constraint
	const = max_norm(1.0)
	# get the end of the last block
	block_end = old_model.layers[-2].output
	# upsample, and define new block
	upsampling = UpSampling2D()(block_end)
	g = Conv2D(128, (3,3), padding='same', kernel_initializer=init, kernel_constraint=const)(upsampling)
	g = PixelNormalization()(g)
	g = LeakyReLU(alpha=0.2)(g)
	g = Conv2D(128, (3,3), padding='same', kernel_initializer=init, kernel_constraint=const)(g)
	g = PixelNormalization()(g)
	g = LeakyReLU(alpha=0.2)(g)
	# add new output layer
	out_image = Conv2D(3, (1,1), padding='same', kernel_initializer=init, kernel_constraint=const)(g)
	# define model
	model1 = Model(old_model.input, out_image)
	# get the output layer from old model
	out_old = old_model.layers[-1]
	# connect the upsampling to the old output layer
	out_image2 = out_old(upsampling)
	# define new output image as the weighted sum of the old and new models
	merged = WeightedSum()([out_image2, out_image])
	# define model
	model2 = Model(old_model.input, merged)
	return [model1, model2]

# define generator models
def define_generator(latent_dim, n_blocks, in_dim=4):
	# weight initialization
	init = RandomNormal(stddev=0.02)
	# weight constraint
	const = max_norm(1.0)
	model_list = list()
	in_latent = Input(shape=(latent_dim,))
	g  = Dense(128 * in_dim * in_dim, kernel_initializer=init, kernel_constraint=const)(in_latent)
	g = Reshape((in_dim, in_dim, 128))(g)
	g = Conv2D(128, (3,3), padding='same', kernel_initializer=init, kernel_constraint=const)(g)
	g = PixelNormalization()(g)
	g = LeakyReLU(alpha=0.2)(g)
	g = Conv2D(128, (3,3), padding='same', kernel_initializer=init, kernel_constraint=const)(g)
	g = PixelNormalization()(g)
	g = LeakyReLU(alpha=0.2)(g)
	out_image = Conv2D(3, (1,1), padding='same', kernel_initializer=init, kernel_constraint=const)(g)
	model = Model(in_latent, out_image)
	model_list.append([model, model])
	for i in range(1, n_blocks):
		old_model = model_list[i - 1][0]
		models = add_generator_block(old_model)
		model_list.append(models)
	return model_list
def define_composite(discriminators, generators):
	model_list = list()
	# create composite models
	for i in range(len(discriminators)):
		g_models, d_models = generators[i], discriminators[i]
		# straight-through model
		d_models[0].trainable = False
		model1 = Sequential()
		model1.add(g_models[0])
		model1.add(d_models[0])
		model1.compile(loss=wasserstein_loss, optimizer=Adam(lr=0.001, beta_1=0, beta_2=0.99, epsilon=10e-8))
		# fade-in model
		d_models[1].trainable = False
		model2 = Sequential()
		model2.add(g_models[1])
		model2.add(d_models[1])
		model2.compile(loss=wasserstein_loss, optimizer=Adam(lr=0.001, beta_1=0, beta_2=0.99, epsilon=10e-8))
		# store
		model_list.append([model1, model2])
	return model_list