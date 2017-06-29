import cv2
import numpy as np
from preprocessor.processor.abstractprocessor import AbstractProcessor


class TonalProcessor(AbstractProcessor):
    def __init__(self, gamma=1):
        self.gamma = gamma

    # Method receives image, modifies it in order to fix tones and propagates it to the next processor.
    def process(self, image):
        new_gamma = 1.0 / self.gamma
        adj_gamma = np.array([((i / 255.0) ** new_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")  # build  table with their adjusted gamma values
        cv2.LUT(image, adj_gamma, image)  # function LUT fills the output array with values from the adjusted gamma
