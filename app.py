import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

st.set_page_config(page_title="Analisis Energi Gedung", layout="wide")

# Load CSS eksternal
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
    }
    h1 {
        color: #0d47a1;
    }
    h2 {
        color: #1565c0;
        font-weight: 600;
    }
    .css-1d391kg {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .css-1ht1j8u {
        font-size: 18px;
        font-weight: bold;
        color: #1a237e;
    }
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #90caf9;
        border-radius: 3px;
    }
    .css-1fcdlhz {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .header {
            background-color: #0d47a1;
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .company {
            font-size: 18px;
            font-weight: bold;
        }
        .location {
            font-size: 16px;
        }
    </style>
    <div class="header">
        <div class="company">PT. Serasi Tunggal Mandiri</div>
        <div class="location">Wisma Indocement</div>
        <h1 style="margin-top:10px;">🔌 Aplikasi Analisis & Prediksi Konsumsi Energi Gedung</h1>
    </div>
""", unsafe_allow_html=True)

st.title("⚡ Analisis Konsumsi Energi Gedung (LWBP & WBP)")

uploaded_file = st.file_uploader("📂 Upload file Excel", type=["xlsx"])

def parse_excel(file):
    xls = pd.ExcelFile(file)
    cleaned_data = []

    for idx, sheet_name in enumerate(xls.sheet_names[:3]):
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        df = df.dropna(how='all').reset_index(drop=True)
        month = idx + 1

        for i in range(2, len(df), 2):
            try:
                day = int(df.iloc[i, 0])
                lwbp = float(df.iloc[i, 1])
                wbp = float(df.iloc[i + 1, 2])
                cleaned_data.append({
                    "Tanggal": pd.Timestamp(f"2025-{month:02d}-{day:02d}"),
                    "Panel": "WBP1",
                    "LWBP": lwbp,
                    "WBP": wbp
                })
            except:
                continue

    return pd.DataFrame(cleaned_data)

if uploaded_file:
    df = parse_excel(uploaded_file)

    panel_list = df['Panel'].unique().tolist()
    selected_panel = st.selectbox("🔘 Pilih Panel", panel_list)
    df_filtered = df[df['Panel'] == selected_panel]

    df_filtered['LWBP Tinggi'] = df_filtered['LWBP'] > 10000
    df_filtered['WBP Tinggi'] = df_filtered['WBP'] > 1000

    st.subheader(f"📋 Data Konsumsi - Panel: {selected_panel}")
    st.dataframe(df_filtered)

    total_lwbp = df_filtered['LWBP'].sum()
    total_wbp = df_filtered['WBP'].sum()

    col1, col2 = st.columns(2)
    col1.metric("🔋 Total LWBP", f"{total_lwbp:,.2f} kWh")
    col2.metric("🔌 Total WBP", f"{total_wbp:,.2f} kWh")

    st.subheader("📈 Grafik Konsumsi Harian")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df_filtered['Tanggal'], df_filtered['LWBP'], label='LWBP', marker='o', linestyle='-', color='#1f77b4')
    ax.plot(df_filtered['Tanggal'], df_filtered['WBP'], label='WBP', marker='s', linestyle='-', color='#ff7f0e')

    high_lwbp = df_filtered[df_filtered['LWBP Tinggi']]
    high_wbp = df_filtered[df_filtered['WBP Tinggi']]
    ax.scatter(high_lwbp['Tanggal'], high_lwbp['LWBP'], color='red', label='LWBP Tinggi', zorder=5, s=70)
    ax.scatter(high_wbp['Tanggal'], high_wbp['WBP'], color='orange', label='WBP Tinggi', zorder=5, s=70)

    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Konsumsi Energi (kWh)", fontsize=12)
    ax.set_title("📊 Konsumsi Energi Harian Berdasarkan Panel", fontsize=14, fontweight='bold')
    ax.legend(frameon=True, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    st.caption("🔴 Titik merah = LWBP > 10.000 kWh | 🟠 Titik oranye = WBP > 1.000 kWh")

    # === Machine Learning Prediksi Irit/Boros ===
    df_filtered['Label'] = np.where((df_filtered['LWBP'] > 10000) | (df_filtered['WBP'] > 1000), 1, 0)
    X = df_filtered[['LWBP', 'WBP']]
    y = df_filtered['Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    # === Tampilkan hasil klasifikasi dengan format tabel yang rapi ===
    report_dict = classification_report(y_test, y_pred, target_names=["Irit", "Boros"], output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose().round(2).reset_index()
    report_df.rename(columns={"index": "Label"}, inplace=True)

    st.subheader("🤖 Hasil Prediksi Machine Learning")
    st.dataframe(report_df.style.set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#e3f2fd'), ('color', '#0d47a1'), ('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ]))

    df_filtered['Prediksi'] = clf.predict(df_filtered[['LWBP', 'WBP']])
    df_filtered['Prediksi Label'] = df_filtered['Prediksi'].map({0: "Irit", 1: "Boros"})

    st.subheader("📊 Data dengan Hasil Prediksi")
    st.dataframe(df_filtered[['Tanggal', 'LWBP', 'WBP', 'Prediksi Label']])

    # === Visualisasi Prediksi ===
    st.subheader("📉 Grafik Prediksi Irit vs Boros")
    fig2, ax2 = plt.subplots(figsize=(14, 5))
    ax2.plot(df_filtered['Tanggal'], df_filtered['Prediksi'], marker='o', linestyle='-', color='#4caf50')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Irit', 'Boros'])
    ax2.set_title("Prediksi Konsumsi Energi Harian", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Tanggal")
    ax2.set_ylabel("Prediksi")
    ax2.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

else:
    st.info("Silakan upload file Excel dulu buat mulai analisis.")

st.markdown("""
    <hr style="margin-top:50px;">
    <div style='text-align: center; color: gray; font-size: 14px;'>
        📍 Wisma Indocement, Jl. Jend. Sudirman Kav. 70-71, Jakarta Selatan 12910<br>
        🔧 Aplikasi dibuat saat magang di PT. Serasi Tunggal Mandiri<br>
        © Copyright by Muhammad Fiqih Tampati<br>
        © 2025 All rights reserved.<br>
    </div>
""", unsafe_allow_html=True)
