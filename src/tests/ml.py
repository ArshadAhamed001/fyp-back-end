import os
import matplotlib.pyplot as plt

import cv2
from random import randint
import numpy as np

import tensorflow as tf
from tensorflow import keras


CLASSES = ['Aventurine Green', 'Aquamarine', 'Amazonite', 'Andalusite', 'Andradite', 'Almandine', 'Alexandrite', 'Ametrine', 'Amethyst', 'Amber', 'Blue Lace Agate', 'Chalcedony Blue', 'Cats Eye', 'Beryl Golden', 'Bixbite', 'Bloodstone', 'Aventurine Yellow', 'Benitoite', 'Chalcedony', 'Carnelian', 'Chrome Diopside', 'Diamond', 'Coral', 'Chrysoberyl', 'Dumortierite', 'Danburite', 'Chrysocolla', 'Citrine', 'Chrysoprase', 'Diaspore', 'Emerald', 'Fluorite', 'Jasper', 'Iolite', 'Goshenite', 'Garnet Red', 'Jade', 'Hiddenite', 'Hessonite', 'Grossular', 'Onyx Black', 'Kyanite', 'Morganite',
           'Moonstone', 'Larimar', 'Onyx Green', 'Labradorite', 'Kunzite', 'Malachite', 'Lapis Lazuli', 'Prehnite', 'Pyrope', 'Quartz Rose', 'Opal', 'Pearl', 'Peridot', 'Onyx Red', 'Pyrite', 'Quartz Lemon', 'Quartz Beer', 'Rhodonite', 'Rhodolite', 'Sapphire Pink', 'Sapphire Blue', 'Sapphire Yellow', 'Quartz Rutilated', 'Rhodochrosite', 'Ruby', 'Sapphire Purple', 'Quartz Smoky', 'Sodalite', 'Scapolite', 'Tigers Eye', 'Serpentine', 'Sphene', 'Sunstone', 'Spinel', 'Spodumene', 'Tanzanite', 'Spessartite', 'Topaz', 'Tourmaline', 'Zoisite', 'Variscite', 'Zircon', 'Turquoise', 'Tsavorite']

gems = []  # names of classes, count of images for each class

model = keras.models.load_model('./content/predicted_model.h5')

newimage = "./images/amethyst.png"
new_image = cv2.imread(newimage)

image = cv2.resize(new_image, (128, 128))
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image = tf.image.resize(image, size=[128, 128])
image = tf.reshape(image, [1, 128, 128, 3])
predict_x = model.predict(image)
classes_x = np.argmax(predict_x, axis=1)

print(classes_x)


print(CLASSES[classes_x[0]])
# print(classes_x)
# print(CLASSES)
