import streamlit as st
import pandas as pd
import os
import re
from io import BytesIO


st.set_page_config(page_title="Konversi Kontak ke CSV Google", page_icon="📇")
st.title("📇 Konversi Data Kontak ke Format Google Contacts CSV")


uploaded_file = st.file_uploader("📤 Upload file Excel kamu", type=["xlsx", "xls"])

if uploaded_file is not None:
 
    base_name = os.path.splitext(uploaded_file.name)[0]

    event_name = re.split(r'\d+', base_name)[0].strip()
    event_name = re.sub(r'\s*-\s*Data Kontak.*$', '', base_name, flags=re.IGNORECASE)
    event_name = event_name.strip().title()

    st.success(f"Nama event terdeteksi: **{event_name}**")

    df = pd.read_excel(uploaded_file)

    if 'Nama' not in df.columns or 'Nomor Whatsapp' not in df.columns:
        st.error("❌ File harus memiliki kolom 'Nama' dan 'Nomor Whatsapp'.")
    else:
        df['Nomor Whatsapp'] = df['Nomor Whatsapp'].astype(str)
        df['Nomor Whatsapp'] = df['Nomor Whatsapp'].str.replace(r'^\+62', '0', regex=True)
        df['Nomor Whatsapp'] = df['Nomor Whatsapp'].str.replace(r'^62', '0', regex=True)

        df['Nama Lengkap'] = df['Nama'].astype(str) + f' {event_name}'

        google_df = pd.DataFrame({
            'Name': df['Nama Lengkap'],
            'Given Name': "",
            'Additional Name': "",
            'Family Name': "",
            'Yomi Name': "",
            'Given Name Yomi': "",
            'Additional Name Yomi': "",
            'Family Name Yomi': "",
            'Name Prefix': "",
            'Name Suffix': "",
            'Initials': "",
            'Nickname': "",
            'Short Name': "",
            'Maiden Name': "",
            'Birthday': "",
            'Gender': "",
            'Location': "",
            'Billing Information': "",
            'Directory Server': "",
            'Mileage': "",
            'Occupation': "",
            'Hobby': "",
            'Sensitivity': "",
            'Priority': "",
            'Subject': "",
            'Notes': "",
            'Language': "",
            'Photo': "",
            'Group Membership': "",
            'Phone 1 - Type': "",
            'Phone 1 - Value': df['Nomor Whatsapp']
        })

        # Tampilkan pratinjau hasil
        st.subheader("🔍 Pratinjau Hasil Konversi")
        st.dataframe(google_df.head())

        # Simpan ke CSV
        output = BytesIO()
        output_filename = f"{event_name} - Kontak Import Google.csv"
        google_df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)

        # Tombol download
        st.download_button(
            label="📥 Download CSV untuk Google Contacts",
            data=output,
            file_name=output_filename,
            mime="text/csv"
        )

        st.success("✅ File siap diunduh dan bisa langsung diimport ke Google Contacts!")
else:
    st.info("⬆️ Silakan upload file Excel dengan kolom 'Nama' dan 'Nomor Whatsapp'.")
