import os
import sys
from flask import Flask, flash, request, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin




UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['yml', 'yaml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# api = Api(app)
CORS(app)
parser = reqparse.RequestParser()

# class fileUpload(Resource):
    
#     def post(self):
#         target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
#         print("Get post req", request.get_data())
#         if not os.path.isdir(target):
#             os.mkdir(target)
#         print("dir ", str(target), " created")
#         Dfiles = request.files.getlist('file[]')
#         # print("files: ", Dfiles)
#         for f in Dfiles:
#             filename = secure_filename(f.filename)
#             destination="/".join([target, filename])
#             print("for: ", f, "\n", "name: ", filename, "\n", "destination: ", destination)
#             f.save(destination)
#             print("File Saved!")
#             session['uploadFilePath']=destination
#         response="Whatever you wish too return"
#         return response

# class URLReciver(Resource):
    
#     def get(self):
#         print("Get get req", request.full_path)
#         # print("URL is: ", )
#         response=request.full_path
#         return {'url':response}

# class Filters(Resource):
    
#     def post(self):
#          label_filter = request.form.getlist('labels')
#          print(label_filter)
#          return 'Got it!', 200




# api.add_resource(fileUpload, '/upload')
# api.add_resource(URLReciver, '/url')
# api.add_resource(Filters, '/filters')
@app.route("/upload", methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
    print("Get post req", request.get_data())
    if not os.path.isdir(target):
        os.mkdir(target)
        file_name_list = open(target+"/list.txt", "w+")
        
    print("dir ", str(target), " created")
    try: 
        Dfiles = request.files.getlist('file[]')
        file_name_list = open(target+"/list.txt", "w+")
        status = 200
        response="Files received!"
    except:
        status = 400
        response="Something wrong!"
        return response, status
    else:
        for f in Dfiles:
            filename = secure_filename(f.filename)
            destination="/".join([target, filename])
            print("for: ", f, "\n", "name: ", filename, "\n", "destination: ", destination)
            f.save(destination)
            file_name_list.writelines(filename)
            print("File Saved!")
            session['uploadFilePath']=destination
        file_name_list.close()
        return response, status


@app.route('/getlabels', methods=['GET'])
def send_labels():
    labels = ['Duplicate service name', 'Duplicate container name', 'Duplicate image', 'Duplicate port']
    return {'labels' : labels}

@app.route('/analyzing', methods=['POST'])
def analyzing():
    target=os.path.join(UPLOAD_FOLDER,'docker-compose-file')
    print("Get post req", request.get_data())
    if not os.path.isdir(target):
        os.mkdir(target)
        file_name_list = open(target+"/list.txt", "w+")
        
        print("dir ", str(target), " created")
        try: 
            Dfiles = request.files.getlist('file[]')
            status = 200
        except:
            status = 400
            response="Something wrong!"
            return response, status
        else:
            for f in Dfiles:
                filename = secure_filename(f.filename)
                destination="/".join([target, filename])
                print("for: ", f, "\n", "name: ", filename, "\n", "destination: ", destination)
                f.save(destination)
                file_name_list.writelines(filename)
                print("File Saved!")
                session['uploadFilePath']=destination
            file_name_list.close()
    print('label_filter:')
    label_filter = request.form.getlist('labels[]')
    print(label_filter)
    print('URL:')
    reqURL = request.form.get('URL')
    print(reqURL)
    response="Analyzing"
    status = 200
    return response, status


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="localhost",use_reloader=False)