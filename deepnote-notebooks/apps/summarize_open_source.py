import os

from PyPDF2 import PdfReader
from gensim.summarization import summarize  # Open source library
from google.cloud import storage


def download_pdf_from_gcp(bucket_name, source_blob_name, destination_file_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}")

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

def summarize_text(text, word_count=100):

    try:
        summary = summarize(text, word_count=word_count)
    except ValueError as e:
        summary = "Input text is too short to summarize.\n" + str(e)
    return summary

def process_pdf(bucket_name, source_blob_name, destination_file_name, word_count=100):

    download_pdf_from_gcp(bucket_name, source_blob_name, destination_file_name)
    text = extract_text_from_pdf(destination_file_name)
    summary = summarize_text(text, word_count)
    os.remove(destination_file_name)  # Clean up the downloaded file
    return summary

