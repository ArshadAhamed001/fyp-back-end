import os
import cv2
import wikipediaapi
import json
import requests
import numpy as np
import tensorflow as tf
import time
from flask import Flask, request, jsonify
from random import randint
from bs4 import BeautifulSoup
from tensorflow import keras
import random
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import random
import PIL

basedir = os.path.abspath(os.path.dirname(__file__))
# assume you have created a uploads folder
uploads_path = os.path.join(basedir, '../uploads')

content_path = os.path.join(basedir, '../content')


def json_list(list):
    lst = []
    for pn in list:
        d = {}
        d['mpn'] = pn
        lst.append(d)
    return json.dumps(lst)


def init_auth_routes(app):
    @app.route('/upload-image', methods=['POST'])
    def upload_image():
        file = request.files['file']

        file_name = file.filename
        file_name = file_name.replace(' ', '')
        split_filename = file_name.split(".")
        file_type = split_filename[1]

        print(f"File Name :  {file_name}")
        print(f"File Type :  {file_type}")

        file_save_path = os.path.join(
            uploads_path+"/Ruby", 'uploaded_image.' + file_type)

        # save the file into the uploads folder
        file.save(file_save_path)

        CLASSES = ['Alexandrite', 'Amazonite', 'Amber', 'Amethyst', 'Ametrine', 'Andalusite', 'Aquamarine',
                   'Aventurine Green', 'Aventurine Yellow', 'Benitoite', 'Bixbite', 'Bloodstone', 'Blue Lace Agate',
                   'Carnelian', 'Cats Eye', 'Chalcedony', 'Chalcedony Blue', 'Chrome Diopside', 'Chrysocolla',
                   'Chrysoprase', 'Citrine', 'Coral', 'Danburite', 'Diamond', 'Emerald', 'Fluorite', 'Garnet Red',
                   'Goshenite', 'Hessonite', 'Hiddenite', 'Iolite', 'Jade', 'Jasper', 'Kunzite', 'Kyanite',
                   'Labradorite', 'Lapis Lazuli', 'Larimar', 'Malachite', 'Moonstone', 'Morganite', 'Onyx Black',
                   'Onyx Green', 'Onyx Red', 'Opal', 'Pearl', 'Peridot', 'Prehnite', 'Pyrite', 'Quartz Beer',
                   'Quartz Lemon', 'Quartz Rose', 'Quartz Rutilated', 'Quartz Smoky', 'Rhodochrosite', 'Rhodolite',
                   'Rhodonite', 'Ruby', 'Sapphire Blue', 'Sapphire Pink', 'Sapphire Purple', 'Scapolite', 'Serpentine',
                   'Sodalite', 'Sphene', 'Spinel', 'Spodumene', 'Sunstone', 'Tanzanite', 'Tigers Eye', 'Topaz',
                   'Tourmaline', 'Tsavorite', 'Turquoise', 'Variscite', 'Zircon', 'Zoisite']

        model_path = os.path.join(basedir, 'gemstone_model_250')
        print(model_path)

        model = keras.models.load_model(model_path)

        image_path = r'C:\Users\Acer\Downloads\fyp-back-end\src\uploads'
        print(image_path)
        time.sleep(5)

        datagen_kwargs_augment = dict(
            rotation_range=2,
            width_shift_range=0.05,
            height_shift_range=0.05,
            shear_range=1,
            # fill_mode = "nearest",
            horizontal_flip=True,
            vertical_flip=True,
            rescale=1 / 255,
            validation_split=0.10,
        )


        datagen_kwargs_default = dict(rescale=1 / 255)

        target_resolution = (256, 256)
        random_seed = random.randrange(0, 10000, 1)
        # random_seed = 1369
        gemstones_folder = uploads_path

        training_datagen = ImageDataGenerator(**datagen_kwargs_augment)
        training_generator = training_datagen.flow_from_directory(
            image_path,
            target_size=target_resolution,
            color_mode="rgb",
            shuffle=random_seed,
            seed=1369,
            subset="training",
            batch_size=12
        )

        validation_datagen = ImageDataGenerator(**datagen_kwargs_augment)
        validation_generator = validation_datagen.flow_from_directory(
            image_path,
            target_size=target_resolution,
            color_mode="rgb",
            shuffle=True,
            seed=random_seed,
            subset="validation",
            batch_size=12
        )

        test_datagen = ImageDataGenerator(**datagen_kwargs_default)
        test_generator = training_datagen.flow_from_directory(
            image_path,
            target_size=target_resolution,
            color_mode="rgb",
            shuffle=False,
            subset="validation",
            batch_size=12,
        )

        full_datagen = ImageDataGenerator(**datagen_kwargs_default)
        full_generator = training_datagen.flow_from_directory(
            image_path,
            target_size=target_resolution,
            color_mode="rgb",
            shuffle=False,
            batch_size=12,
        )
        predictions = model.predict(full_generator)
        predictions = np.argmax(predictions, axis=1)
        #print(full_generator.classes)
        print(predictions)

        print(CLASSES[predictions[0]])

        return {'status': 'ok', 'payload': {'predicted_value': CLASSES[predictions[0]]}}, 200


    @app.route('/wiki-summary', methods=['POST'])
    def wikipedia_summary():
        body = request.get_json()
        value = body['value']

        wiki_wiki = wikipediaapi.Wikipedia('en')
        # page_py = wiki_wiki.page(value)

        page_py = wiki_wiki.page(value)

        page_py = wiki_wiki.page(value)
        print("Page - Exists: %s" % page_py.exists())
        # Page - Exists: True

        if not page_py.exists():
            word_list = value.split()

            number_of_words = len(word_list)
            if number_of_words > 1:
                page_py = wiki_wiki.page(word_list[0])
                print("Page - Exists: %s" % page_py.exists())

        if not page_py.exists():
            word_list = value.split()

            number_of_words = len(word_list)
            if number_of_words > 1:
                page_py = wiki_wiki.page(word_list[1])
                print("Page - Exists: %s" % page_py.exists())

        if not page_py.exists():
            return {'status': 'ok', 'payload': {'wiki_summary': ''}}, 200

        # print(page_py)
        return {'status': 'ok', 'payload': {'wiki_summary': page_py.summary[0:200]}}, 200


    @app.route('/similar-images', methods=['POST'])
    def similar_images():
        body = request.get_json()
        value = body['value']

        try:
            url = 'https://www.google.com/search?q={0}&tbm=isch'.format(value)
            content = requests.get(url).content
            soup = BeautifulSoup(content, 'lxml')
            images = soup.findAll('img')

            all_images = []

            for image in images:
                all_images.append(image.get('src'))
            # print(all_images)
            return {'status': 'ok', 'payload': {'img_array': all_images}}, 200
        except Exception as e:
            print(e)
            return {'status': 'fail', 'err': jsonify(e)}, 500
