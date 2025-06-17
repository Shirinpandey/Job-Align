from flask import Flask, render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
from io import BytesIO

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

#referencing this file
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#when user goes to browser run home + get means get data post means submit data (here we did post)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['cv']
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
            contents = ''
            for page in pdf_reader.pages:
                contents += page.extract_text() or ""

        else:
            contents = file.read().decode('uti-8')
        return render_template('results.html', cv_text = contents)
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug= True)

