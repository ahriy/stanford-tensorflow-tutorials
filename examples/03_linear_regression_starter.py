""" Simple linear regression example in TensorFlow
This program tries to predict the number of thefts from 
the number of fire in the city of Chicago
Author: Chip Huyen
Prepared for the class CS 20SI: "TensorFlow for Deep Learning Research"
cs20si.stanford.edu
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd

import utils

DATA_FILE = 'data/fire_theft.xls'
def huber_loss(labels, predictions, delta=1.0):
    residual = tf.abs(predictions - labels)
    condition = tf.less(residual, delta)
    small_res = 0.5 * tf.square(residual)
    large_res = delta * residual - 0.5 * tf.square(delta)
    return tf.where(condition, small_res, large_res)

# Phase 1: Assemble the graph
# Step 1: read in data from the .xls file
book = xlrd.open_workbook(DATA_FILE, encoding_override='utf-8')
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])
n_samples = sheet.nrows - 1

# Step 2: create placeholders for input X (number of fire) and label Y (number of theft)
# Both have the type float32
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# Step 3: create weight and bias, initialized to 0
# name your variables w and b
w = tf.Variable(0, dtype=tf.float32, name="w")
b = tf.Variable(0, dtype=tf.float32, name="b")
w1 = tf.Variable(0, dtype=tf.float32, name="w1")
b1 = tf.Variable(0, dtype=tf.float32, name="b1")
# Step 4: predict Y (number of theft) from the number of fire
# name your variable Y_predicted
Y_predicted = X * w + b
Y_predicted1 = X * w1 + b1

# Step 5: use the square error as the loss function
# name your variable loss
loss = tf.square(Y - Y_predicted, name="loss")
loss1 = huber_loss(Y, Y_predicted1)
# Step 6: using gradient descent with learning rate of 0.01 to minimize loss
opti = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)
opti1 = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss1)
init_wb = tf.variables_initializer([w, b, w1, b1], name="init_wb")
# Phase 2: Train our model
with tf.Session() as sess:
    writer = tf.summary.FileWriter('./my_graph/03/linear_reg',
								   sess.graph)
    # Step 7: initialize the necessary variables, in this case, w and b
	# TO - DO
    sess.run(init_wb)
    # Step 8: train the model
    for i in range(100): # run 100 epochs
        total_loss = 0
        total_loss1 = 0
        for x, y in data:
            # Session runs optimizer to minimize loss and fetch the value of loss. Name the received value as l
			# TO DO: write sess.run()
            _, l = sess.run([opti, loss], feed_dict={X: x, Y: y})
            _, l1 = sess.run([opti1, loss1], feed_dict={X: x, Y: y})
            total_loss += l
            total_loss1 += l1
        print("Epoch {0}: {1}".format(i, total_loss/n_samples))
        print("Epoch1 {0}: {1}".format(i, total_loss1 / n_samples))
    w, b = sess.run([w, b])
    w1, b1 = sess.run([w1, b1])
# plot the results
X, Y = np.array(data.T[0]), np.array(data.T[1])
plt.plot(X, Y, 'bo', label='Real data')
plt.plot(X, X * w + b, 'r', label='Predicted data')
plt.plot(X, X * w1 + b1, 'g', label='Predicted data huber')
plt.legend()
plt.show()