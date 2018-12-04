import os
from flask import Flask, flash,request, render_template, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from script import procesar_video

UPLOAD_FOLDER = './public/videos'
ALLOWED_EXTENSIONS = set(['gif','avi','mp4', 'mov'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import string
import random

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def new_random_name_title ():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(28))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
	    # check if the post request has the file part
		if 'file' not in request.files:
			return jsonify({'status':404,'message':'file empty'})
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			return jsonify({'status':404,'message':'file empty'})
		if file and allowed_file(file.filename):
			id = new_random_name_title()
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			procesar_video(filename,id)
			if os.path.isfile('./public/videos/'+id+'.mp4'):
				return  jsonify({'status':202, 'url':'/uploads/'+id+'.mp4'})
			else:
				return jsonify({'status':404,'message':'your video could not be processed'})
		return jsonify({'status':404,'message':'format not allowed'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)