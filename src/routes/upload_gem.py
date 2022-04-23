from flask import Flask, request, jsonify
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# assume you have created a uploads folder
uploads_path = os.path.join(basedir, '../uploads')


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
        return {'status': 'ok'}, 200
