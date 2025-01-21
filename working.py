from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os
import json

# Helper functions
def extract_text_from_pdf(file_path, **kwargs):
    """Extract text from a PDF."""
    text = extract_text(file_path)
    return text

def chunk_text(text, chunk_size=500, **kwargs):
    """Split the extracted text into chunks of a specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def generate_text_embeddings(chunks, **kwargs):
    """Generate embeddings for each text chunk."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    return json.dumps(embeddings.tolist())  # Store embeddings as JSON

def analyze_embeddings_for_insights(embeddings, **kwargs):
    """Generate insights based on the embeddings."""
    # Example: Find the most similar chunks using cosine similarity or cluster them
    # For simplicity, let's say we return the embeddings as the 'insights'
    return json.dumps(embeddings)  # In practice, apply clustering or other analysis here

def save_output(data, output_path, **kwargs):
    """Save the output (embeddings or insights) to a file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(data)

# Default arguments for the DAG
default_args = {
    'owner': 'user',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 20),
}

# Define the Airflow DAG
with DAG(
    'pdf_to_insights_pipeline',
    default_args=default_args,
    description='Extract text, generate embeddings, and insights from a PDF',
    schedule_interval=None,
) as dag:

    # Task 1: Extract text from the PDF
    extract_text_task = PythonOperator(
        task_id='extract_text',
        python_callable=extract_text_from_pdf,
        op_kwargs={'file_path': '/mnt/c/Users/Devanshu/airflow/input/Raisin_Dataset.pdf'},
    )

    # Task 2: Chunk the text
    chunk_text_task = PythonOperator(
        task_id='chunk_text',
        python_callable=chunk_text,
        provide_context=True,
    )

    # Task 3: Generate embeddings
    generate_embeddings_task = PythonOperator(
        task_id='generate_embeddings',
        python_callable=generate_text_embeddings,
        provide_context=True,
    )

    # Task 4: Analyze embeddings for insights (e.g., clustering, similarity)
    analyze_embeddings_task = PythonOperator(
        task_id='analyze_embeddings_for_insights',
        python_callable=analyze_embeddings_for_insights,
        provide_context=True,
    )

    # Task 5: Save insights to a file
    save_insights_task = PythonOperator(
        task_id='save_insights',
        python_callable=save_output,
        provide_context=True,
        op_kwargs={'output_path': '/mnt/c/Users/Devanshu/airflow/output/insights.json'},
    )

    # Task 6: Save embeddings to a file
    save_embeddings_task = PythonOperator(
        task_id='save_embeddings',
        python_callable=save_output,
        provide_context=True,
        op_kwargs={'output_path': '/mnt/c/Users/Devanshu/airflow/output/embeddings.json'},
    )

    # Task dependencies
    extract_text_task >> chunk_text_task
    chunk_text_task >> generate_embeddings_task
    generate_embeddings_task >> analyze_embeddings_task
    analyze_embeddings_task >> save_insights_task
    generate_embeddings_task >> save_embeddings_task

