from flask import Flask, request, jsonify
# to avoid cors error in different frontend like react js or any other
from flask_cors import CORS

import src.routes.upload_gem as Image_Upload_Routes

app = Flask(__name__)
CORS(app)


@ app.route('/', methods=['GET'])
def hello_world():
    return ('hello world'), 200


@ app.route('/health', methods=['GET'])
def test():
    return ('Healthy'), 200


Image_Upload_Routes.init_auth_routes(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
