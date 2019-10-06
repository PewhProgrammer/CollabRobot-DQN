import os
import tensorflow as tf

if __name__ == '__main__':
    print("hallo")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
