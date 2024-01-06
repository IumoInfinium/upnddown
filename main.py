import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# variables loaded from `.env` file
UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER', '')
PORT: int = os.environ.get('PORT', None)
SECRET_KEY: str = os.environ.get('SECRET_KEY', '')

BASE_URL: str = f"{os.environ.get('BASE_URL', '')}:{PORT}"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():

    # if request type is not post, do not allow
    if request.method != 'POST':
        return "You are allowed to send this type of request!"

    # if there is no file found, respond that no file found
    if 'file_upload_input' not in request.files:
        return redirect(location='/', code = 200)
    
    # get list of all the uploaded files
    uploaded_files = request.files.getlist("file_upload_input")

    print(uploaded_files)
    if len(uploaded_files)  <= 0:
        return redirect(location=url_for('homepage'), code = 200)
    
    # get current date to store the uploads in date-wise format 
    folder_name = datetime.today().strftime('%d_%m_%Y')

    if folder_name  == '':
        return 'Could not create folder'
    
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name.strip())

    # create the upload date folder, in case there is no folder
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    # create through the files in the buffer and save them at the `UPLOAD_FOLDER/{folder_name}` location
    for file in uploaded_files:
        try:
            file_path = os.path.join(folder_path, file.filename)
            
            if not os.path.exists(file_path):
                file.save(dst=file_path)
            else:
                file.save(dst = file_path + '_copy')

        except Exception as e:
            print(f'error saving the file with exception : {e}')
            return 'error occured in saving file'
    
    # return the index page with populated data
    return render_template(
        'index.html',
        uploaded_files = [file.filename for file in uploaded_files]
    )

if __name__ == "__main__":
    app.run(
        port = PORT,
        debug = True
    )