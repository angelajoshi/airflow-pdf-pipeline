from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint


def _train_model(model):
    """
    Simulate model training and return a random accuracy between 1 and 10.
    """
    return randint(1, 10)

def _evaluate_accuracy(ti):
    """
    Evaluate which model met the accuracy threshold.
    Pull the accuracies from the XComs, check if they meet the threshold.
    """
    accuracies = ti.xcom_pull(task_ids=[
        'train_model_text',
        'train_model_summary',
        'train_model_embedding'
    ])
    
    thresholds = {
        'text': 7,
        'summary': 6,
        'embedding': 8
    }

    results = []
    for model_id, accuracy in zip(['text', 'summary', 'embedding'], accuracies):
        if accuracy >= thresholds[model_id]:
            results.append(f"Model {model_id} met threshold with accuracy: {accuracy}")
        else:
            results.append(f"Model {model_id} did not meet threshold with accuracy: {accuracy}")
    
    
    return "\n".join(results)

def _process_textual_data():
    """
    Simulate the extraction of textual data for the PDF.
    """
    return "Extracted Textual Data: This is a sample text to be embedded in the PDF."

def _process_summary_data():
    """
    Simulate summarizing the extracted textual data.
    """
    return "Summarized Text: Key points extracted from the document."

def _process_embedding_data():
    """
    Simulate the embedding of data for the PDF.
    """
    return "Embedding Data: Embedding the summarized and extracted text."


with DAG("text_to_pdf_pipeline",
         start_date=datetime(2023, 1, 1), 
         schedule_interval='@daily', 
         catchup=False) as dag:

    
    train_model_text = PythonOperator(
        task_id='train_model_text',
        python_callable=_train_model,
        op_kwargs={"model": "text"}
    )
    
    train_model_summary = PythonOperator(
        task_id='train_model_summary',
        python_callable=_train_model,
        op_kwargs={"model": "summary"}
    )
    
    train_model_embedding = PythonOperator(
        task_id='train_model_embedding',
        python_callable=_train_model,
        op_kwargs={"model": "embedding"}
    )
    
    
    process_textual_data = PythonOperator(
        task_id='process_textual_data',
        python_callable=_process_textual_data
    )
    
    process_summary_data = PythonOperator(
        task_id='process_summary_data',
        python_callable=_process_summary_data
    )
    
    process_embedding_data = PythonOperator(
        task_id='process_embedding_data',
        python_callable=_process_embedding_data
    )

    
    evaluate_accuracy = PythonOperator(
        task_id="evaluate_accuracy",
        python_callable=_evaluate_accuracy
    )

    
    generate_pdf = BashOperator(
        task_id="generate_pdf",
        bash_command="echo 'PDF generated with the data extracted and embedded.'"
    )

    
    [train_model_text, train_model_summary, train_model_embedding] >> evaluate_accuracy
    evaluate_accuracy >> [process_textual_data, process_summary_data, process_embedding_data] >> generate_pdf
