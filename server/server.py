from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from extractImage import extract
import os
import csv
from zipfile import ZipFile
from extractTable import getTable

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    folder_path = "./uploads"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    file = request.files['file']
    file.save("./uploads/"+ file.filename)
    extract(file.filename)
    # generate the table
    print("./uploads/"+ file.filename)

    file_path = "./uploads/" + file.filename


    getTable(file_path)
    return {'message': 'File uploaded successfully'}

@app.route('/images')
def get_images_names():
    images = []
    for filename in os.listdir('./uploads'):
        if filename.endswith('.jpeg') or filename.endswith('.png'):
            images.append(filename)
    return jsonify(images)


@app.route('/download')
def download_all_files():
    # specify the directory where the images are stored
    directory = './uploads'
    # get a list of all the files in the directory
    file_list = os.listdir(directory)
    # create a new zip file
    zip_file = ZipFile('all_images.zip', 'w')
    # loop through the file list and add each file to the zip file
    for file in file_list:
        # check if the file is an image file
        if file.endswith('.jpg') or file.endswith('.png'):
            zip_file.write(os.path.join(directory, file), file)
    # close the zip file
    zip_file.close()
    # send the zip file to the user as an attachment
    return send_file('all_images.zip', as_attachment=True)


@app.route('/image/<filename>')
def get_image(filename):
    return send_file(f'./uploads/{filename}', mimetype='image/jpg')


# @app.route('/csv')
# def return_csv():
#     csv_file_path = './csvFile/output.csv'
#     return send_file(csv_file_path,
#                      mimetype='text/csv',
#                      attachment_filename='mydata.csv',
#                      as_attachment=True)


# @app.route('/csvdownload')
# def download():
#     filename = './csvFile/output1.csv'
#     return send_file(filename, as_attachment=True)

@app.route('/csvdownload')
def download():
    root_dir = './csvFile'  # path to the directory containing the files to be zipped
    zip_filename = 'output.zip'  # name of the zip file to be created
    zip_filepath = os.path.join(root_dir, zip_filename)  # path to the zip file to be created
    with ZipFile(zip_filepath, 'w') as zip_file:
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                zip_file.write(file_path, os.path.relpath(file_path, root_dir))
    return send_file(zip_filepath, as_attachment=True)  


if __name__ == '__main__':
    app.run()
