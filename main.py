import os
import urllib.request
import uuid
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from datetime import date

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message': 'File successfully uploaded', 'file_size': os.stat(filename).st_size, 'id':  uuid.uuid4(), 'upload_date': str(date.today()), 'file_name': filename, 'url': str(os.path.abspath(filename))})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are pdf, png, jpg, jpeg'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run(port = 5002)
