from skimage import color
import cv2
import numpy as np
import skimage
from skimage.filters import sobel
from model import Model

IMAGE_SIZE = (96, 128)

class Data_container:
    def __init__(self):
        self._image_buffer = [None, None]
        self._empty_flags = [True, True]
        self._model = Model()

    def insert_image(self, image, channel):
        # print("start inserting", channel)
        imageBGR = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

        imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
        img_gray = color.rgb2gray(imageRGB)
        # print("inserting", channel, img_resized.shape)
        # img_resized = img_gray
        self._image_buffer[channel] = img_gray
        self._empty_flags[channel] = False
        # print(channel, img_gray.shape)

    def predict(self):
        if self._empty_flags[0] or self._empty_flags[1]:
            return -2, None
        img_1 = skimage.transform.resize(self._image_buffer[0], IMAGE_SIZE)
        img_2 = skimage.transform.resize(self._image_buffer[1], IMAGE_SIZE)
        img = np.concatenate([img_1, img_2])
        ret = self._model.predict(img)
        return 0, ret
