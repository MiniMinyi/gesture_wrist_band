import tensorflow as tf
import numpy as np
import time


class Model:
    def __init__(self):
        self._model = None
        self._model = tf.keras.models.load_model(
            "/Users/panxingyu/gesture_wrist_band/gesture_wrist_band/model/model_shallow/weights.157-92.4232.hdf5",
            compile=False)
        self._model._make_predict_function()
        print("finished init", self._model)


    def predict(self, data):
        # print("predict")
        # if not self._model:
        #     self._model = tf.keras.models.load_model(
        #         "/Users/panxingyu/gesture_wrist_band/gesture_wrist_band/demo_ms3_ht/weights.36-39.5012.hdf5",
        #         compile=False)
        #     self._model._make_predict_function()
        inputs = data[tf.newaxis, ..., tf.newaxis]
        # print(inputs)
        now = time.time()
        raw_ret = self._model.predict(inputs)
        # print(time.time()-now)
        # print(raw_ret)
        # exit()
        return raw_ret
