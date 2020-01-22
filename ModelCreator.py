import tensorflow as tf
from common.constants import *
import os

inputs = tf.keras.Input(shape = (AUTO_vector_size,))
x = tf.keras.layers.Dense(6)(inputs)
x = tf.keras.activations.relu(x, max_value = 6)
x = tf.keras.layers.Dense(3)(x)
x = tf.keras.activations.relu(x, max_value = 6)
outputs = tf.keras.layers.Dense(2, activation = 'softmax')(x)
model = tf.keras.Model(inputs = inputs, outputs = outputs)
model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)
model.summary()
model.save(os.path.join(AUTO_PATH, AUTO_default_filename))