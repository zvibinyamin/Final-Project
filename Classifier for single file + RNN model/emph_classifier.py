import tensorflow as tf

from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav

frames = 50#20
first_frame = 30
lstm_size = 128#10
mfccs = 20 #upto 26!
test_frac = 0.2

file_name = './emphasised/%Can I borrow this Look for a day%.wav'
file_name = './all_normal/kevin -Are they coming here tomorrow.wav'
emph = 0

print(file_name)
(rate, sig) = wav.read(file_name)
mfcc_feat = mfcc(sig,rate)
curr = logfbank(sig,rate)
data = (curr[first_frame:(first_frame+frames),0:mfccs]/20, 1.0 * (1-emph))
#print(data[0])
#print(data[1])
x = tf.placeholder(dtype=tf.float32, shape=[None, frames, mfccs])
y_ = tf.placeholder(dtype=tf.float32, shape = [None, 1])


lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(lstm_size)
output, _ = tf.nn.dynamic_rnn(lstm_cell, x, dtype=tf.float32)
output = tf.transpose(output, [1,0,2])
last = tf.gather(output, int(output.get_shape()[0]-1))

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
saver.restore(sess, "/tmp/emph_573.ckpt")

print("accuracy on test: ", sess.run(accuracy, feed_dict={x: [data[0]], y_: [[data[1]]]}))