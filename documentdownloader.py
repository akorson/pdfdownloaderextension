import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from PyPDF2 import PdfConverter, PdfFileReader
import textract
import streamlit as st
import pandas as pd

def is_downloadable(url):
    extensions = ['.doc', '.docx', '.rtf', '.txt', '.pdf']
    parsed = urllib.parse.urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext.lower() in extensions

def convert_to_pdf(file_path):
    file_format = os.path.splitext(file_path)[1].lower()
    if file_format == '.pdf':
        return file_path
    else:
        pdf_path = os.path.splitext(file_path)[0] + '.pdf'
        if file_format == '.txt':
            text = open(file_path, 'rb').read()
        else:
            text = textract.process(file_path)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_writer = PdfConverter()
            pdf_writer.addPage(PdfFileReader(text, strict=False).pages[0])
            pdf_writer.write(pdf_file)
        return pdf_path

def scrape_and_convert_documents(url, save_directory, username=None, password=None):
    session = requests.Session()
    if username and password:
        session.auth = (username, password)
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and is_downloadable(href):
            file_name = os.path.basename(href)
            file_path = os.path.join(save_directory, file_name)
            document_response = session.get(href)
            with open(file_path, 'wb') as document_file:
                document_file.write(document_response.content)
            pdf_path = convert_to_pdf(file_path)
            st.write(f"Downloaded and converted: {pdf_path}")

# Streamlit app
st.title("Document Scraper and Converter")

# Option selection
option = st.radio("Select Option:", ("Scrape from URL", "Scrape from File"))

if option == "Scrape from URL":
    url = st.text_input("Enter the URL:")
    requires_login = st.checkbox("Requires Login")

    if requires_login:
        username = st.text_input("Enter username:")
        password = st.text_input("Enter password:", type="password")
    else:
        username = None
        password = None

    save_directory = st.text_input("Save Directory")

    if st.button("Browse"):
        save_directory = st.file_browser(title="Select Directory", type=2)

    if st.button("Scrape and Convert"):
        if url and save_directory:
            scrape_and_convert_documents(url, save_directory, username, password)
        else:
            st.warning("Please enter a valid URL and select a save directory.")

elif option == "Scrape from File":
    file = st.file_uploader("Upload file", type=["csv", "doc", "docx", "pdf", "xlsx"])
    save_directory = st.text_input("Save Directory")

    if st.button("Browse"):
        save_directory = st.file_browser(title="Select Directory", type=2)

    if st.button("Scrape and Convert"):
        if file and save_directory:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension == ".csv":
                df = pd.read_csv(file)
            elif file_extension == '.xlsx':
                df = pd.read_excel(file)

            if file_extension in ['.csv', '.xlsx']:
                for _, row in df.iterrows():
                    url = row['URL']
                    scrape_and_convert_documents(url, save_directory)
        else:
            st.warning("Please select a file and provide a save directory."