import os
import cv2
import wikipediaapi
import json
import requests
import numpy as np
import tensorflow as tf

from flask import Flask, request, jsonify
from random import randint
from bs4 import BeautifulSoup
from tensorflow import keras


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
            uploads_path, 'uploaded_image.'+file_type)

        # save the file into the uploads folder
        file.save(file_save_path)

        CLASSES = ['Aventurine Green', 'Aquamarine', 'Amazonite', 'Andalusite', 'Andradite', 'Almandine', 'Alexandrite', 'Ametrine', 'Amethyst', 'Amber', 'Blue Lace Agate', 'Chalcedony Blue', 'Cats Eye', 'Beryl Golden', 'Bixbite', 'Bloodstone', 'Aventurine Yellow', 'Benitoite', 'Chalcedony', 'Carnelian', 'Chrome Diopside', 'Diamond', 'Coral', 'Chrysoberyl', 'Dumortierite', 'Danburite', 'Chrysocolla', 'Citrine', 'Chrysoprase', 'Diaspore', 'Emerald', 'Fluorite', 'Jasper', 'Iolite', 'Goshenite', 'Garnet Red', 'Jade', 'Hiddenite', 'Hessonite', 'Grossular', 'Onyx Black', 'Kyanite', 'Morganite',
                   'Moonstone', 'Larimar', 'Onyx Green', 'Labradorite', 'Kunzite', 'Malachite', 'Lapis Lazuli', 'Prehnite', 'Pyrope', 'Quartz Rose', 'Opal', 'Pearl', 'Peridot', 'Onyx Red', 'Pyrite', 'Quartz Lemon', 'Quartz Beer', 'Rhodonite', 'Rhodolite', 'Sapphire Pink', 'Sapphire Blue', 'Sapphire Yellow', 'Quartz Rutilated', 'Rhodochrosite', 'Ruby', 'Sapphire Purple', 'Quartz Smoky', 'Sodalite', 'Scapolite', 'Tigers Eye', 'Serpentine', 'Sphene', 'Sunstone', 'Spinel', 'Spodumene', 'Tanzanite', 'Spessartite', 'Topaz', 'Tourmaline', 'Zoisite', 'Variscite', 'Zircon', 'Turquoise', 'Tsavorite']

        model_path = os.path.join(content_path, 'predicted_model.h5')
        print(model_path)

        model = keras.models.load_model(model_path)

        image_path = file_save_path

        # print(image_path)
        new_image = cv2.imread(image_path)

        image = cv2.resize(new_image, (128, 128))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = tf.image.resize(image, size=[128, 128])
        image = tf.reshape(image, [1, 128, 128, 3])
        predict_x = model.predict(image)
        classes_x = np.argmax(predict_x, axis=1)

        print(CLASSES[classes_x[0]])

        return {'status': 'ok', 'payload': {'predicted_value': CLASSES[classes_x[0]] or 'Alexandrite'}}, 200

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
