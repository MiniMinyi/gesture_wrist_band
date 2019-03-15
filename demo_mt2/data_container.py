from skimage import color
import cv2
import numpy as np
import skimage
from skimage.filters import sobel
from model import Model


class Data_container:
    def __init__(self, buffer_size=32, model_capacity=16):
        self._image_list = [[None for i in range(buffer_size)], [None for i in range(buffer_size)]]
        self._indexes = [0, 0]
        self._start_flag = False
        self._buffer_size = buffer_size
        self._model_capacity = model_capacity
        self._model = Model()
        self._ret_buffer = [6, 6]
        self._ret_buffer_index = 0

    def insert_image(self, image, channel):
        imageBGR = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
        img_gray = color.rgb2gray(imageRGB)
        img_resized = skimage.transform.resize(img_gray, (48, 64))
        img_sobelled = sobel(img_resized)
        self._image_list[channel][self._indexes[channel]] = img_sobelled
        self._indexes[channel] += 1
        if self._indexes[channel] >= self._buffer_size:
            self._indexes[channel] = 0
        if (not self._start_flag) and (
                self._indexes[0] >= self._model_capacity and self._indexes[1] >= self._model_capacity):
            self._start_flag = True

    def predict(self):
        if (not self._start_flag) and (
                self._indexes[0] < self._model_capacity or self._indexes[1] < self._model_capacity):
            return -2, None, None
        key_images_np = [None, None]
        for i in range(2):
            if self._indexes[i] < self._model_capacity:
                key_images_list = self._image_list[i][
                                  self._buffer_size - (self._model_capacity - self._indexes[i]):] + self._image_list[
                                                                                                        i][
                                                                                                    :self._indexes[
                                                                                                        i]]
            else:
                key_images_list = self._image_list[i][self._indexes[i] - self._model_capacity:self._indexes[i]]
            key_images_np[i] = np.stack(key_images_list, axis=2)
        input_data = np.concatenate(key_images_np, axis=2)
        if input_data.shape != (48, 64, 32):
            print("shape ERROR: ", input_data.shape)
            return -3, None, None
        # print(input_data.shape)
        rets = self._model.predict(input_data)
        current_ret = np.argmax(rets)
        self._ret_buffer[self._ret_buffer_index] = current_ret
        self._ret_buffer_index += 1
        if self._ret_buffer_index == len(self._ret_buffer):
            self._ret_buffer_index = 0
        counts = np.bincount(self._ret_buffer)
        best_ret = np.argmax(counts)

        return 0, rets.tolist(), int(best_ret)
