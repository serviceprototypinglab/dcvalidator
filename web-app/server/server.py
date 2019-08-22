import os
import sys
from flask import Flask, flash, request, redirect, url_for, session
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(level=logging.INFO)

# logger = logging.getLogger('HELLO WORLD')



UPLOAD_FOLDER = './'
# ALLOWED_EXTENSIONS = set(['yml', 'yaml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)
# @app.route('/upload', methods=['POST'])
# def fileUpload():
#     target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
#     if not os.path.isdir(target):
#         os.mkdir(target)
#     logger.info("welcome to upload`")
#     file = request.files['file'] 
#     filename = secure_filename(file.filename)
#     destination="/".join([target, filename])
#     file.save(destination)
#     session['uploadFilePath']=destination
#     response="Whatever you wish too return"
#     return response
class fileUpload(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
        print("Get post req", request.get_data())
        if not os.path.isdir(target):
            os.mkdir(target)
        print("dir ", str(target), " created")
        # logger.info("welcome to upload`")
        # ploaded_files = flask.request.files.getlist("file[]")
        Dfiles = request.files.getlist('file[]')
        print("files: ", Dfiles)
        # logger.info(str(type(files)))
        for f in Dfiles:
            # print(f)
            # # logger.info(str(f))
            filename = secure_filename(f.filename)
            destination="/".join([target, filename])
            print("for: ", f, "\n", "name: ", filename, "\n", "destination: ", destination)
            f.save(destination)
            print("File Saved!")
            session['uploadFilePath']=destination
        response="Whatever you wish too return"
        return response

api.add_resource(fileUpload, '/upload')

# @app.route('/test', methods=['POST'])
# def test():
#     response="Whatever you wish too return"
#     return response

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="localhost",use_reloader=False)