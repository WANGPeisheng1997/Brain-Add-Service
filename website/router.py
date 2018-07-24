from app import app, photos
from flask import render_template, request, redirect, url_for, abort
import cv2 as cv
from utils import predict

logger = app.logger


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST' and 'photo' in request.files:
        photo = photos.save(request.files['photo'])
        image_name = 'Image Relative Path'
        gray = cv.imread(image_name, 0)
        out = predict(gray)
        cv.imwrite('uploads/output.png', out)

        return redirect(url_for('show', name=photo))

    return render_template('index.html')


@app.route('/photo/<name>')
def show(name):
    if name is None:
        abort(404)
    url = photos.url(name)
    return render_template('show.html', url=url, name=name)
