from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
from utils.cambridge_scraper import get_word_info

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/start', methods=['GET', 'POST'])
def index():
    result_data = []
    search_words = []

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                return "不支援的檔案格式"

            search_words = df.iloc[:, 0].dropna().astype(str).tolist()

            for word in search_words:
                info = get_word_info(word)
                result_data.append(info)

            combined = zip(search_words, result_data)
            return render_template('start.html', combined=combined)

    return render_template('start.html', combined=[])

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
