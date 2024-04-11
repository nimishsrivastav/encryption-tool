from flask import Flask, render_template, request, redirect, send_file

import os

# Importing encryption and decryption functions
from tool.encrypt_file import encrypt_file
from tool.decrypt_file import decrypt_file

app = Flask(__name__)

# Folder structure and allowed file extensions
BASE_FOLDER = 'files'
UPLOADED_FOLDER = os.path.join(BASE_FOLDER, 'uploaded_files')
ENCRYPTED_FOLDER = os.path.join(BASE_FOLDER, 'encrypted_files')
DECRYPTED_FOLDER = os.path.join(BASE_FOLDER, 'decrypted_files')
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'json', 'xml'}

# Create folder structure if doesn't exist
for folder in [BASE_FOLDER, UPLOADED_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOADED_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['DECRYPTED_FOLDER'] = DECRYPTED_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded.')
    
    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No file selected.')
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect('/encrypt-decrypt/' + file.filename)
    
    return redirect(request.url)

@app.route('/encrypt-decrypt/<filename>', methods=['GET', 'POST'])
def encrypt(filename):
    if request.method == 'POST':
        password = request.form['password']

        encrypt_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['ENCRYPTED_FOLDER'], filename), password)
        
        return redirect('/download/' + filename)
    
    return render_template('encrypt-decrypt.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename), as_attachment=True)

@app.route('/encrypt-decrypt/<filename>', methods=['GET', 'POST'])
def decrypt(filename):
    if request.method == 'POST':
        password = request.form['password']

        decrypt_file(os.path.join(app.config['ENCRYPTED_FOLDER'], filename), os.path.join(app.config['DECRYPTED_FOLDER'], filename), password)
        
        return redirect('/download_decrypted/' + filename)
    
    return render_template('decrypt.html', filename=filename)

@app.route('/download_decrypted/<filename>')
def download_decrypted(filename):
    return send_file(os.path.join(app.config['DECRYPTED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
