import os
import sys
from flask import Flask, flash, request, redirect, url_for, session
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin




UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['yml', 'yaml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)
class fileUpload(Resource):
    
    def post(self):
        target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
        print("Get post req", request.get_data())
        if not os.path.isdir(target):
            os.mkdir(target)
        print("dir ", str(target), " created")
        Dfiles = request.files.getlist('file[]')
        print("files: ", Dfiles)
        for f in Dfiles:
            filename = secure_filename(f.filename)
            destination="/".join([target, filename])
            print("for: ", f, "\n", "name: ", filename, "\n", "destination: ", destination)
            f.save(destination)
            print("File Saved!")
            session['uploadFilePath']=destination
        response="Whatever you wish too return"
        return response

api.add_resource(fileUpload, '/upload')

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="localhost",use_reloader=False)