#from htk import open1

import numpy as np
from os import listdir
from random import shuffle
import tensorflow as tf

from python_speech_features import mfcc
#from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

frames = 50#20
first_frame = 30
lstm_size = 128#10
mfccs = 20 #upto 26!
test_frac = 0.2


#t = open1("/home/azariaa/DNN/course/checkpoints/465000-model.ckpt.data-00000-of-00001")
#while (True):
#    print(t.readvec())

# for lang in langs:
#     for file_name in listdir(lang):
#         print(file_name)
#         a = open1("./"+lang+"/" + file_name, mode='rb')
#         curr = []
#         for i in range(first_frame + frames):
#             if i < first_frame:
#                 a.readvec()
#             else:
#                 curr.append(a.readvec()[0:mfccs])
#         all.append((curr, 1.0 * langs.index(lang)))

all = []
#langs = ['French_100','German_100']
#langs = ['Spanish_100','German_100']
#langs = ['spanish','german']
langs = ['emph','normal']

for lang in langs:
    for file_name in listdir(lang):
        print(file_name)
        (rate, sig) = wav.read("./"+lang+"/" + file_name)
        mfcc_feat = mfcc(sig,rate)
        #d_mfcc_feat = delta(mfcc_feat, 2)
        curr = logfbank(sig,rate)
        all.append((curr[first_frame:(first_frame+frames),0:mfccs]/20, 1.0 * langs.index(lang)))

#print(all)
print(all[5][0][0])
shuffle(all)
split_point = int(len(all) * (1- test_frac))
train = all[0:split_point]
test = all[split_point: len(all)]

#all = [([[0.9]],1.0), ([[0.9]],1.0), ([[0.85]],1.0), ([[0.87]],1.0), ([[0.38]],0.0), ([[0.45]],0.0), ([[0.5]],0.0), ([[0.4]],0.0)]
print(all)
x = tf.placeholder(dtype=tf.float32, shape=[None, frames, mfccs])
y_ = tf.placeholder(dtype=tf.float32, shape = [None, 1])


lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(lstm_size)
output, _ = tf.nn.dynamic_rnn(lstm_cell, x, dtype=tf.float32)
output = tf.transpose(output, [1,0,2])
last = tf.gather(output, int(output.get_shape()[0]-1))

# MFC
# x0 = tf.reshape(x, shape=[-1, frames*mfccs])
# W0 = tf.Variable(tf.truncated_normal([frames*mfccs,lstm_size], stddev=0.1))
# b0 = tf.Variable(tf.constant(0.0,shape=[lstm_size]))
# last = tf.nn.relu(tf.matmul(x0, W0) + b0)

W1 = tf.Variable(tf.truncated_normal([lstm_size,1], stddev=0.1))
b1 = tf.Variable(tf.constant(0.0,shape=[1]))

h1 = 1 / (1.0 + tf.exp(-(tf.matmul(last, W1) + b1)))

loss = tf.reduce_mean(tf.pow(y_ - h1,2))

update = tf.train.AdamOptimizer(0.01).minimize(loss)
#update = tf.train.GradientDescentOptimizer(0.01).minimize(loss)
correct_prediction = tf.logical_or(tf.abs(y_ - h1) < 0.5, (y_ - h1) == 0.5)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

frac1 = tf.reduce_mean(tf.cast(h1 >= 0.5, tf.float32))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
#Restore the session
saver.restore(sess, "/tmp/emph_400.ckpt")

#for i in range(1000):
#    [_, acc, loss_val, frac_pred] = sess.run([update, accuracy, loss, frac1], feed_dict={x: [item[0] for item in train], y_: [[item[1]] for item in train]})
#    print(i, "acc: ", acc, "loss: ", loss_val, " 1pred: ", frac_pred)
#    if acc > 0.95:
#        break

print("accuracy on test: ", sess.run(accuracy, feed_dict={x: [item[0] for item in test], y_: [[item[1]] for item in test]}))

#Save the session
#save_path = saver.save(sess, "/tmp/emph_400.ckpt")





