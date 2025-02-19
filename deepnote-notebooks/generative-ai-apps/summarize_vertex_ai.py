import os

from PyPDF2 import PdfReader
from google.cloud import aiplatform as vertex_ai
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

def summarize_text_with_vertex_ai(project, location, model_name, text, max_input_tokens=1024):

    vertex_ai.init(project=project, location=location)

    model = vertex_ai.TextGenerationModel.from_pretrained(model_name)

    if len(text.split()) > max_input_tokens:
        text = " ".join(text.split()[:max_input_tokens])

    response = model.predict(text)

    return response.text

def process_pdf_with_vertex_ai(bucket_name, source_blob_name, destination_file_name, project, location, model_name):

    download_pdf_from_gcp(bucket_name, source_blob_name, destination_file_name)

    text = extract_text_from_pdf(destination_file_name)

    summary = summarize_text_with_vertex_ai(project, location, model_name, text)

    os.remove(destination_file_name)  # Clean up the downloaded file

    return summary
