from flask import Flask, render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import PyPDF2
import os,nltk, json
from io import BytesIO
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


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
    try:
        file = request.files['cv']
        if not file:
            return "No file uploaded"
        contents = cv_reading(file)
        new_file = storefiles()
        clean_data(contents)
        return render_template('results.html', job_listing = new_file)
    except RequestEntityTooLarge:
        return "File is larger than 16 MB"
    

def storefiles():
    with open(os.path.join("jobs", "job.json"), 'r') as f:
        jobs = json.load(f)
        

    return jobs


def clean_data(jobs):
    lower_jobs = jobs.lower()
    cleaned_char = []
    for char in lower_jobs:
        if char.isalnum() or char.isspace():
            cleaned_char.append(char)
    cleaned_data = ''.join(cleaned_char)
    cleaned_no_space = ' '.join(cleaned_data.split())

    stops = set(stopwords.words('english'))
    word = cleaned_no_space.split()
    filtered_words = [w for w in word if w not in stops]

    return ' '.join(filtered_words)


def cv_reading(file):
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
            contents = file.read().decode('utf-8')
    return contents

    
if __name__ == "__main__":
    app.run(debug= True)

