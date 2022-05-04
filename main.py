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
class MibatchDev(tf.keras.layers.Layer):
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
def disbase(input, dim):
    for i in range(2):
        model = Conv2D(128, (3,3), strides = 1, padding = 'same')(input)
        model = LeakyReLU(alpha=0.1)(model)
    model = AveragePooling2D()(model)
    return Model([input, model])
def disblock(input, old_model):
     in_shape = list(old_model.input.shape)
     try :
         #input processing layer
         model1  = Conv2D(128, (1,1), padding='same', kernel_initializer=init, kernel_constraint=const)(input)
         model1 = LeakyReLU()(model1)
         model1 = disbase(model1, (in_shape[0],in_shape[1],in_shape[2]))
         #input downscaling layer
         model2 = AveragePooling2D()(input)
        model2 = Conv2D(128, (1, 1), padding='same', kernel_initializer=init, kernel_constraint=const)(model2)
        model2 = LeakyReLU()(model2)

