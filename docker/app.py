from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from flask import Flask, Response, request
from stat import S_ISREG, ST_CTIME, ST_MODE
from hashlib import sha1
from shutil import rmtree
import json
import os
from html_var import hello_html, login_ok, image_upload
from upload_image import broadcast, save_normalized_image, safe_addr, receive, event_stream
from flask_cors import CORS
MAX_IMAGES = 1
DATA_DIR = 'data'
user = {'name': 'orhan', 'pw': '12345'}
app = Flask(__name__)  # app = Flask(__name__, static_folder=DATA_DIR)
CORS(app)


def results(filename):
    previous_model = load_model('./64_by_64.h5')  # 128x128
    TEST_IMAGE_URL = "data/" + filename
    test_image = image.load_img(TEST_IMAGE_URL, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    return previous_model.predict(test_image)


@app.route('/post', methods=['POST'])
def post():
    """Handle image uploads."""
    sha1sum = sha1(request.data).hexdigest()
    target = os.path.join(DATA_DIR, '{}.jpg'.format(sha1sum))
    message = json.dumps({'src': target,
                          'ip_addr': safe_addr(request.access_route[0])})
    try:
        if save_normalized_image(target, request.data):
            broadcast(message)  # Notify subscribers of completion
    except Exception as exception:  # Output errors
        return '{}'.format(exception)
    return 'UPLOAD SUCCESSFULLY COMPLETED'


@app.route('/')
def home():
    rmtree(DATA_DIR, True)
    os.mkdir(DATA_DIR)
    image_infos = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        file_stat = os.stat(filepath)
        if S_ISREG(file_stat[ST_MODE]):
            image_infos.append((file_stat[ST_CTIME], filepath))
    images = []
    for i, (_, path) in enumerate(sorted(image_infos, reverse=True)):
        if i >= MAX_IMAGES:
            os.unlink(path)
            continue
        images.append(f'<div><img alt="image is in :" src="{path}" /></div>')
    return image_upload


@app.route('/predict')
def predict():
    images = 0
    result = "OK"
    for filename in os.listdir(DATA_DIR):
        print(filename)
        result = results(filename)
        images += 1

    if images > 0:
        print("+++++++++there is some images")
        # result = results(filename)
    else:
        print("--------------there no images")
    return "prediction result is{}".format(result)


@ app.route('/stream')
def stream():
    """Handle long-lived SSE streams."""
    return Response(event_stream(request.access_route[0]),
                    mimetype='text/event-stream')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", threaded=True, debug=True, port=port)
