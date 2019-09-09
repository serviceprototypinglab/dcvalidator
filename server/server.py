import os
import shutil
import sys
from flask import Flask, flash, request, redirect, url_for, session, send_from_directory, abort
# from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

sys.path.insert(1, '../')
from validator import Validator
my_validator = Validator()




BASE_FOLDER = './'
ALLOWED_EXTENSIONS = set(['yml', 'yaml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = BASE_FOLDER
# api = Api(app)
CORS(app)
# parser = reqparse.RequestParser()

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
    target=os.path.join(BASE_FOLDER,'docker-compose-file')
    if not os.path.isdir(target):
        os.mkdir(target)
        file_name_list = open(os.path.join(target,"list.txt"), "w+")
        
    print("dir ", str(target), " created")
    try: 
        Dfiles = request.files.getlist('file[]')
        file_name_list = open(os.path.join(target,"list.txt"), "w+")
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
            # file_name_list.writelines(filename)
            print(filename, file=file_name_list)
            print("File Saved!")
            session['uploadFilePath']=destination
        file_name_list.close()
        return response, status


@app.route('/getlabels', methods=['GET'])
def send_labels():
    labels = ['Duplicate Keys', 'Duplicate ports']
    return {'labels' : labels}

@app.route('/analyzing', methods=['POST'])
def analyzing():
    target=os.path.join(BASE_FOLDER,'docker-compose-file')
    if not os.path.isdir(target):
        os.mkdir(target)
        file_name_list = open(os.path.join(target,"list.txt"), "w+")
        
    print("dir ", str(target), " created")
    try: 
        Dfiles = request.files.getlist('file[]')
        file_name_list = open(os.path.join(target,"list.txt"), "w+")
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
            # file_name_list.writelines(filename)
            print(filename, file=file_name_list)
            print("File Saved!")
            session['uploadFilePath']=destination
        file_name_list.close()
    print('label_filter:')
    label_filter = request.form.getlist('labels[]')
    print(label_filter)
    print('URL:')
    reqURL = request.form.get('URL')
    print(reqURL)
    file_name_list = os.path.join(target, 'list.txt')
    with open(file_name_list) as dokcer_compose_files:
        dokcer_compose_list = dokcer_compose_files.read()
        dokcer_compose_list = dokcer_compose_list.split('\n')
        dokcer_compose_list = dokcer_compose_list[:-1]
    if len(dokcer_compose_list) >= 1:    
        for docker_compose in dokcer_compose_list: 
            my_validator.validator(autosearch=None, filebasedlist=None, urlbased=None, eventing=None, filebased=os.path.join(target, docker_compose), labelArray=label_filter)
    my_validator.validator(autosearch=None, filebasedlist=None, urlbased=reqURL, eventing=None, filebased=None, labelArray=label_filter)
    logs = []
    shutil.rmtree("./docker-compose-file")
    with open("logs.txt", "r") as logsFile:
        for _, line in enumerate(logsFile):
            logs.append(line)
    os.remove("logs.txt")
    status = 200
    return {'logs': logs}


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="localhost",use_reloader=False)