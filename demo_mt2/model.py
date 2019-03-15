import tensorflow as tf
import numpy as np


class Model:
    def __init__(self):
        self._model = tf.keras.models.load_model(
            "/Users/panxingyu/gesture_wrist_band/gesture_wrist_band/model/weights.60-loss=0.0849-acc=0.99.hdf5",
            compile=False)
        self._model._make_predict_function()

    def predict(self, data):
        inputs = data[tf.newaxis, ..., tf.newaxis]
        raw_ret = self._model.predict(inputs)
        ret = np.exp(raw_ret)
        return ret[0]
