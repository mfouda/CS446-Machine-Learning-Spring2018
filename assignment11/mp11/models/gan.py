"""Generative adversarial network."""

import numpy as np
import tensorflow as tf

from tensorflow import contrib
from tensorflow.contrib import layers

class Gan(object):
    """Adversary based generator network.
    """
    def __init__(self, ndims=784, nlatent=2):
        """Initializes a GAN

        Args:
            ndims(int): Number of dimensions in the feature.
            nlatent(int): Number of dimensions in the latent space.
        """

        self._ndims = ndims
        self._nlatent = nlatent

        # Input images
        self.x_placeholder = tf.placeholder(tf.float32, [None, ndims])

        # Input noise
        self.z_placeholder = tf.placeholder(tf.float32, [None, nlatent])

        # Build graph.
        self.x_hat = self._generator(self.z_placeholder)        
        y_hat = self._discriminator(self.x_hat)
        y = self._discriminator(self.x_placeholder, reuse=True)

        # Discriminator loss
        self.d_loss = self._discriminator_loss(y, y_hat)

        # Generator loss
        self.g_loss = self._generator_loss(y_hat)

        # Optimizers
        self.learning_rate = tf.placeholder(tf.float32, shape=[])

        self.generator_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='generator')
        self.discriminator_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='discriminator')

        self.discriminator_optimizer = tf.train.GradientDescentOptimizer(learning_rate = self.learning_rate)
        self.discriminator_train_op = self.discriminator_optimizer.minimize(self.d_loss, var_list=self.discriminator_variables)

        self.generator_optimizer = tf.train.AdamOptimizer(learning_rate = self.learning_rate)
        self.generator_train_op = self.generator_optimizer.minimize(self.g_loss, var_list=self.generator_variables)

        # Create session
        self.session = tf.InteractiveSession()
        self.session.run(tf.global_variables_initializer())

    def _discriminator(self, x, reuse=False):
        """Discriminator block of the network.

        Args:
            x (tf.Tensor): The input tensor of dimension (None, 784).
            reuse (Boolean): re use variables with same name in scope instead of creating
              new ones, check Tensorflow documentation
        Returns:
            y (tf.Tensor): Scalar output prediction D(x) for true vs fake image(None, 1). 
              DO NOT USE AN ACTIVATION FUNCTION AT THE OUTPUT LAYER HERE.

        """
        with tf.variable_scope("discriminator", reuse=reuse) as scope:
            if reuse:
                tf.get_variable_scope().reuse_variables()
            h1 = tf.layers.dense(x, 128 , activation = tf.nn.relu)
            y = tf.layers.dense(h1, 1)
            return y


    def _discriminator_loss(self, y, y_hat):
        """Loss for the discriminator.

        Args:
            y (tf.Tensor): The output tensor of the discriminator for true images of dimension (None, 1).
            y_hat (tf.Tensor): The output tensor of the discriminator for fake images of dimension (None, 1).
        Returns:
            l (tf.Scalar): average batch loss for the discriminator.

        """
        # Loss corresponding to true samples
        true_samples_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels = tf.ones(tf.shape(y)), logits = y)
        
        # Loss corresponding to fake samples
        fake_samples_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels = tf.zeros(tf.shape(y_hat)), logits = y_hat)
        
        # Discriminator tries to classify true samples with 1 and fake samples with 0
        l = tf.reduce_mean(true_samples_loss) + tf.reduce_mean(fake_samples_loss)
        return l


    def _generator(self, z, reuse=False):
        """From a sampled z, generate an image.

        Args:
            z(tf.Tensor): z from _sample_z of dimension (None, 2).
            reuse (Boolean): re use variables with same name in scope instead of creating
              new ones, check Tensorflow documentation 
        Returns:
            x_hat(tf.Tensor): Fake image G(z) (None, 784).
        """
        with tf.variable_scope("generator", reuse=reuse) as scope:
            if reuse:
                tf.get_variable_scope().reuse_variables()
            h1 = tf.layers.dense(z, 128 , activation = tf.nn.relu)
            x_hat = tf.layers.dense(h1, self._ndims, activation = tf.nn.sigmoid)
            return x_hat


    def _generator_loss(self, y_hat):
        """Loss for the discriminator.

        Args:
            y_hat (tf.Tensor): The output tensor of the discriminator for fake images of dimension (None, 1).
        Returns:
            l (tf.Scalar): average batch loss for the discriminator.

        """
        # Generator tries to make discriminator classify fake samples with 1
        l = tf.nn.sigmoid_cross_entropy_with_logits(labels = tf.ones(tf.shape(y_hat)), logits = y_hat)
        return tf.reduce_mean(l)
