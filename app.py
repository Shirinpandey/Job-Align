from flask import Flask, render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import PyPDF2
from io import BytesIO
import os 


#referencing this file
app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = '/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.config['ALLOWED_EXTENSIONS'] = ['.txt', '.pdf']

#when user goes to browser run home + get means get data post means submit data (here we did post)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods = ['POST'])
def upload():
    #array of files we find cv 
    try:
        file = request.files['cv'] 
        extension = os.path.splitext(file.filename)[1]
        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return "File should be pdf or txt"
            if file.filename.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
                contents = ''
                for page in pdf_reader.pages:
                    contents += page.extract_text() or ""

            else:
                contents = file.read().decode('uti-8')
            return render_template('results.html', cv_text = contents)

    except RequestEntityTooLarge:
        return "File is larger than 16 MB"


def storefiles():
    job = []

    for file in os.listdir("jobs"):
        with open('filename.txt', 'r') as f:
            content = f.read()
            job.append(content)
    return content
    
if __name__ == "__main__":
    app.run(debug= True)

