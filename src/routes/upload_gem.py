from flask import Flask, request, jsonify
import os
import wikipediaapi
import requests
from bs4 import BeautifulSoup
import json

basedir = os.path.abspath(os.path.dirname(__file__))
# assume you have created a uploads folder
uploads_path = os.path.join(basedir, '../uploads')


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

        # save the file into the uploads folder
        file.save(os.path.join(uploads_path, 'uploaded_image.'+file_type))
        return {'status': 'ok', 'payload': {'predicted_value': 'Diamond'}}, 200

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
            return {'status': 'ok', 'payload': {'wiki_summary': ''}}, 200

        # print(page_py)
        return {'status': 'ok', 'payload': {'wiki_summary': page_py.summary[0:200]}}, 200

    @app.route('/similar-images', methods=['POST'])
    def similar_images():
        body = request.get_json()
        value = body['value']

        url = 'https://www.google.com/search?q={0}&tbm=isch'.format(value)
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'lxml')
        images = soup.findAll('img')

        all_images = []

        for image in images:
            # print(image.get('src'))
            all_images.append(image.get('src'))
        # print(all_images)

        return {'status': 'ok', 'payload': {'img_array': all_images}}, 200
