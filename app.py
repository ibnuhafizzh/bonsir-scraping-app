from flask import Flask, render_template, request, send_file, jsonify
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from utils.scrape import scraping_result
from utils.giro import process_and_score_dirty_data  # Impor dari giro.py

app = Flask(__name__)

# Folder tempat menyimpan file yang diunggah dan hasil proses
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route for the homepage with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Route for Customer Exposure
@app.route('/scraping')
def menu_a():
    return render_template('scrape.html')

# Route for Customer Scoring
@app.route('/giro')
def menu_b():
    return render_template('giro.html')

# Route to handle file upload and scoring for Customer Scoring
@app.route('/upload_scoring', methods=['POST'])
def upload_scoring():
    if 'file' not in request.files or 'sheet' not in request.form:
        return 'No file uploaded or no sheet selected', 400
    
    file = request.files['file']
    sheet_name = request.form['sheet']
    if file.filename == '':
        return 'No file selected', 400
    
    # Simpan file yang diunggah
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)
    
    # Proses file yang diunggah dan hasilnya disimpan di file Excel baru
    output_file_path = os.path.join(UPLOAD_FOLDER, 'cleaned_data_with_scores.xlsx')
    process_and_score_dirty_data(file_path, sheet_name, output_file_path)
    
    # Mengirim file hasil ke pengguna
    return send_file(output_file_path, as_attachment=True)

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get user input from form
    company_names = request.form.getlist('company[]')

    # Call scraping function
    sorted_companies = scraping_result(company_names)

    if (sorted_companies == "99"): 
        return render_template('scrape.html', error=sorted_companies)
    # Render the same template with sorted companies
    return render_template('scrape.html', sorted_companies=sorted_companies)

if __name__ == '__main__':
    app.run(debug=True)