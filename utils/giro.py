import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename

# Folder tempat menyimpan file yang diunggah dan hasil proses
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to process and score dirty data
def process_and_score_dirty_data(file_path, sheet_name, output_file_path):
    dirty_df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Filter hanya untuk KOCAB 12100
    dirty_df = dirty_df[dirty_df['KOCAB'] == 12100]
    
    dirty_df_cleaned = clean_data(dirty_df)
    dirty_df_cleaned = calculate_potential_giro_score(dirty_df_cleaned)
    
    # Mengurutkan berdasarkan Skor Potensi Giro secara descending
    dirty_df_cleaned = dirty_df_cleaned.sort_values(by='Skor Potensi Giro', ascending=False)
    
    dirty_df_cleaned.to_excel(output_file_path, index=False)

# Fungsi clean_data
def clean_data(df):
    df_renamed = df.rename(columns={
        'posisi': 'Posisi',
        'CIF': 'CIF',
        'NAMA': 'NAMA',
        'STATUS': 'Status Tabungan',
        'R3K': 'Rekening',
        'sccode': 'Jenis Tabungan',
        'officr': 'Jenis Nasabah',
        'cbalrp': 'Current Balance',
        'lmcbalrp': 'Last Month Balance',
        'lycbalrp': 'Last Year Balance',
        'avgbal': 'Average Balance',
        'datop6': 'CIF Dibuat',
        'cforg6': 'Tabungan Dibuat',
        'datst6': 'Tabungan Inactive',
        'ybalrp': 'Year Balance'
    })
    
    df_cleaned = df_renamed.drop(columns=['actype', 'k'])
    df_cleaned['Jenis Nasabah'].fillna(df_cleaned['Jenis Nasabah'].mode()[0], inplace=True)
    df_cleaned['Last Month Balance'].fillna(0, inplace=True)
    df_cleaned['Tabungan Inactive'].fillna('Aktif', inplace=True)
    df_cleaned['CIF Dibuat'] = df_cleaned['CIF Dibuat'].apply(convert_to_date)
    df_cleaned['Tabungan Dibuat'] = df_cleaned['Tabungan Dibuat'].apply(convert_to_date)
    
    return df_cleaned

# Fungsi convert_to_date
def convert_to_date(value):
    value_str = str(int(value))
    if len(value_str) == 6:
        day = value_str[:2]
        month = value_str[2:4]
        year = value_str[4:6]
    elif len(value_str) == 5:
        day = value_str[0]
        month = value_str[1:3]
        year = value_str[3:5]
    else:
        return None
    return f"{day}/{month}/20{year}"

# Fungsi calculate_potential_giro_score
def calculate_potential_giro_score(df):
    df['Jenis Nasabah'] = df['Jenis Nasabah'].apply(lambda x: 'BMP' if 'BMP' in x else x)
    df['Jenis Tabungan'] = df['Jenis Tabungan'].replace({
        'TABBISNIS': 'TABBIS',
        'TABBIS-USD': 'TABBIS',
        'TABBIS-SGD': 'TABBIS',
        'TABBIS-EUR': 'TABBIS',
        'TABBIS-HKD': 'TABBIS',
        'TABBIS-GBP': 'TABBIS',
        'MTBINV-OL': 'MTBI',
        'MTBINVRK': 'MTBI',
        'MTBINV': 'MTBI'
    })
    
    jenis_nasabah_scores = {'PVB42': 5, 'BMP': 4, 'SM100': 3, 'MM100': 2, 'MB100': 1}
    jenis_tabungan_scores = {'MTBI': 5, 'TABBIS': 3}
    status_scores = {1: 5, 4: 2, 7: 1, 9: 1}
    today = pd.to_datetime('today')
    df['Tabungan Inactive'] = pd.to_datetime(df['Tabungan Inactive'], format='%d/%m/%Y', errors='coerce')
    df['Tabungan Inactive'] = df['Tabungan Inactive'].apply(lambda x: 'Aktif' if pd.isna(x) or x > today else 'Non-Aktif')
    status_tabungan_scores = {'Aktif': 5, 'Non-Aktif': 1}
    
    df['Skor Jenis Nasabah'] = df['Jenis Nasabah'].map(jenis_nasabah_scores)
    df['Skor Jenis Tabungan'] = df['Jenis Tabungan'].map(jenis_tabungan_scores)
    df['Skor Status'] = df['Status Tabungan'].map(status_scores)
    df['Skor Status Tabungan'] = df['Tabungan Inactive'].map(status_tabungan_scores)
    
    df['Log Average Balance'] = np.log1p(df['Average Balance'])
    df['Umur CIF (tahun)'] = (today - pd.to_datetime(df['Tabungan Dibuat'], format='%d/%m/%Y')).dt.days / 365
    df['Umur Tabungan (tahun)'] = (today - pd.to_datetime(df['CIF Dibuat'], format='%d/%m/%Y')).dt.days / 365
    
    df['Normalized Umur CIF'] = df['Umur CIF (tahun)'] / df['Umur CIF (tahun)'].max()
    df['Normalized Umur Tabungan'] = df['Umur Tabungan (tahun)'] / df['Umur Tabungan (tahun)'].max()

    weights = {
        'Jenis Nasabah': 0.25,
        'Jenis Tabungan': 0.15,
        'Status': 0.10,
        'Saldo Rata-Rata': 0.25,
        'Umur CIF': 0.10,
        'Umur Tabungan': 0.10,
        'Status Tabungan': 0.05
    }
    
    df['Skor Potensi Giro'] = (
        (weights['Jenis Nasabah'] * df['Skor Jenis Nasabah']) +
        (weights['Jenis Tabungan'] * df['Skor Jenis Tabungan']) +
        (weights['Status'] * df['Skor Status']) +
        (weights['Saldo Rata-Rata'] * df['Log Average Balance']) +
        (weights['Umur CIF'] * df['Normalized Umur CIF']) +
        (weights['Umur Tabungan'] * df['Normalized Umur Tabungan']) +
        (weights['Status Tabungan'] * df['Skor Status Tabungan'])
    )
    
    return df