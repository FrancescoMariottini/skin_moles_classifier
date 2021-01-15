import cv2
from tensorflow.keras.applications import vgg16, mobilenet_v2

D = 9
SIGMACOLOR = 75
SIGMASPACE = 75

def preprocess_mobilenetV2(image):
  image = cv2.bilateralFilter(image, d=D, sigmaColor=SIGMACOLOR, sigmaSpace=SIGMASPACE)
  image = mobilenet_v2.preprocess_input(image, data_format=None)
  return image


def preprocess_vgg16(image):
  image = cv2.bilateralFilter(image, d=D, sigmaColor=SIGMACOLOR, sigmaSpace=SIGMASPACE)
  image = vgg16.preprocess_input(image, data_format=None)
  return image
