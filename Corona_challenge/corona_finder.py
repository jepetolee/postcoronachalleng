import tensorflow as tf
import numpy as np
import pandas as pd
import datetime


def normalization(x):
    array = np.array(x)
    return (array - array.min()) / (array.max() - array.min() + 3e-7) #오류방지

def denormalization(orginal_confirm, confirm):
    orginal_confirm_array = np.array(orginal_confirm)
    array = np.array(confirm)
    return (array * (orginal_confirm_array.max() - orginal_confirm_array.min() + 3e-7)) + orginal_confirm_array.min()

def lstm_cell():
    cell = tf.contrib.rnn.BasicLSTMCell(num_units=20,forget_bias=0.001, state_is_tuple=True, activation=tf.nn.softsign)
    #망각편향은 1.0,히든레이어 20개
    if 0.57 < 1.0:
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=0.47)
    return cell

def train(xtrain,ytrain,x,confirms,z,newz,ztrain,trial):
    Xinput = tf.placeholder(tf.float32, [None,None, 4])  # 이거 3으로 바꾸어야함,# 30은 데이터를 분류하는 만큼의 숫자
    xinput = tf.placeholder(tf.float32, [None,None,1])

    Yinput= tf.placeholder(tf.float32, [None, 1])
    yinput = tf.placeholder(tf.float32, [None, 1])

    stackRNN = [lstm_cell() for _ in range(4)]  # 레이어를 쌓은 수
    multi_RNNlayers = tf.contrib.rnn.MultiRNNCell(stackRNN, state_is_tuple=True) if 2 > 1 else lstm_cell()


    hypothesis, _states = tf.nn.dynamic_rnn(multi_RNNlayers, Xinput, dtype=tf.float32)
    hypothesis = tf.contrib.layers.fully_connected(hypothesis[:, -1], 1, activation_fn=tf.identity)

    hyp,_states=tf.nn.dynamic_rnn(lstm_cell(), xinput, dtype=tf.float32)
    hyp = tf.contrib.layers.fully_connected(hyp[:, -1], 1, activation_fn=tf.identity)

    loss = tf.reduce_sum(tf.square(hypothesis - Yinput))#단일 데이터의 평균제곱오차 연산
    optimizer = tf.train.AdamOptimizer(0.001)  # 학습률

    lost=tf.reduce_sum(tf.square(hyp - yinput))
    optim= tf.train.AdamOptimizer(0.001)

    learn = optimizer.minimize(loss)
    study=optim.minimize(lost)

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    for epoch in range(trial):

        _, loster = sess.run([learn, loss], feed_dict={Xinput: xtrain, Yinput: ytrain})
        _, losted = sess.run([study, lost], feed_dict={xinput: newz, yinput: ztrain})
        if (epoch+1)%100==0:
            recent = np.array([x[len(x) - 2:]])
            prediction = sess.run(hypothesis, feed_dict={Xinput: recent})
            prediction = denormalization(confirms, prediction)  # 금액데이터 역정규화한다
            print("epoch: {},prediction: {}, Tomorrow's confirmer: {}".format(epoch + 1, prediction[0][0], prediction[
                0]))  # 예측한 주가를 출력한다 RNN Cell(여기서는 LSTM셀임)들을 연결
            recent = np.array([x[len(x) - 2:]])
            predictions = []
            prediction = [sess.run(hypothesis, feed_dict={Xinput: recent})]
            recent_z = np.array([z[len(z) - 2:]])
            recent_z = np.concatenate((recent_z, prediction), axis=1)
            for i in range(10):
                pred = sess.run(hyp, feed_dict={xinput: recent_z})
                predictions.append(pred)
                recent_z = np.concatenate((recent_z, [pred]), axis=1)
            predictions = denormalization(confirms, predictions)
            for i in range(len(predictions)):
                if predictions[i] < 0:
                    predictions[i] = 0
                predictions[i] = int(predictions[i])

            print(" Tomorrow's confirmer:\n [[[2.]]\n\n [[4.]]\n\n [[12.]]\n\n [[18.]]]\n\n 여기까지가 5월 9일까지의 값\n\n {}".format(predictions))
