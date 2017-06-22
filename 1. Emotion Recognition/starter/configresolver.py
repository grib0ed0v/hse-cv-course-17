import configparser
import logging

from preprocessor.facedetector import FaceDetector
from preprocessor.processor.impl.color import ColorProcessor
from preprocessor.processor.impl.noise import NoiseProcessor
from preprocessor.processor.impl.tonal import TonalProcessor
from preprocessor.processor.impl.contrast import ContrastProcessor


class ConfigResolver:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./resources/config.ini')

    def get_face_detector(self):
        if not self.config.has_section('FaceDetector'):
            raise ValueError('No FaceDetector configuration!')
        else:
            cascade_classifier_path = self.config.get('FaceDetector', 'cascadeClassifier', fallback='./resources/haarcascade_frontalface_default.xml')
            scaleFactor = self.config.getfloat('FaceDetector', 'scaleFactor', fallback=1.3)
            minNeighbors = self.config.getint('FaceDetector', 'minNeighbors', fallback=4)
            minSize_x = self.config.getint('FaceDetector', 'minSize_x', fallback=40)
            minSize_y = self.config.getint('FaceDetector', 'minSize_y', fallback=40)
            return FaceDetector(cascade_classifier_path, scaleFactor, minNeighbors, (minSize_x, minSize_y))

    def get_processor_chain(self):
        chain_description = self.config.get('ProcessorChain', 'chain', fallback=None)

        if chain_description is None:
            logging.warning('No processor chain configured! Image will be sent to CNN without preprocessing.')
        else:
            return self.__build_processor_chain(chain_description)

    def __build_processor_chain(self, chain_description):
        chain = list()
        for processor_name in chain_description.split():
            if processor_name == 'NoiseProcessor':
                chain.append(self.__build_noise_processor())
            elif processor_name == 'TonalProcessor':
                chain.append(self.__build_tonal_processor())
            elif processor_name == 'ContrastProcessor':
                chain.append(self.__build_contrast_processor())
            elif processor_name == 'ColorProcessor':
                chain.append(self.__build_color_processor())
            else:
                logging.error('No such processor with name: ' + processor_name)

        if len(chain) == 0:
            logging.warning('No processor chain configured! Image will be sent to CNN without preprocessing.')
        return chain

    def __build_noise_processor(self):
        h = self.config.getint('NoiseProcessor', 'h', fallback=10)
        hColor = self.config.getint('NoiseProcessor', 'hColor', fallback=10)
        templateWindowSize = self.config.getint('NoiseProcessor', 'templateWindowSize', fallback=7)
        searchWindowSize = self.config.getint('NoiseProcessor', 'searchWindowSize', fallback=21)
        return NoiseProcessor(h, hColor, templateWindowSize, searchWindowSize)

    def __build_tonal_processor(self):
        gamma = self.config.getfloat('TonalProcessor', 'gamma', fallback=1.0)
        return TonalProcessor(gamma)

    def __build_contrast_processor(self):
        clipLimit = self.config.getfloat('ContrastProcessor', 'clipLimit', fallback=2.0)
        tileGridSize_h = self.config.getint('ContrastProcessor', 'tileGridSize_h', fallback=8)
        tileGridSize_w = self.config.getint('ContrastProcessor', 'tileGridSize_w', fallback=8)
        return ContrastProcessor(clipLimit, (tileGridSize_h,tileGridSize_w))

    def __build_color_processor(self):
            return ColorProcessor()
