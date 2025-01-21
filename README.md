# PDF to Insights Pipeline
![image](https://github.com/user-attachments/assets/32fca968-f0a2-42df-8c8e-57378e4cecd1)


This project implements an **Airflow pipeline** that extracts text from a PDF, generates embeddings for the extracted text, and analyzes the embeddings to derive insights. The pipeline is designed to process PDF files, convert them into meaningful data representations (embeddings), and then analyze and save these insights.

## Features

- **Text Extraction**: Extracts text from a PDF file using `pdfminer.six`.
- **Text Chunking**: Splits extracted text into smaller chunks for efficient processing.
- **Text Embeddings**: Uses `SentenceTransformer` to generate embeddings for each chunk.
- **Embedding Analysis**: Analyzes embeddings for insights (e.g., clustering or similarity).
- **Output**: Saves the generated embeddings and insights into JSON files.

## Requirements

Before running this pipeline, ensure that you have the following dependencies installed:

- **Apache Airflow**: Orchestrates the workflow and tasks.
- **pdfminer.six**: Extracts text from PDF files.
- **sentence-transformers**: Generates embeddings from text chunks.
- **transformers**: Provides natural language processing models like BART for summarization.
- **json**: For handling JSON data.
- **os**: For file handling.

To install the necessary dependencies, use the following command:

```bash
pip install -r requirements.txt
```

### Requirements file (`requirements.txt`):

```txt
apache-airflow==2.5.0
pdfminer.six==20201018
sentence-transformers==2.2.0
transformers==4.24.0
```

## Setup

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/pdf-to-insights-pipeline.git
cd pdf-to-insights-pipeline
```

2. **Setup the Airflow environment**:
   If you don’t have Airflow installed, you can set it up by following the instructions in the official [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/installation/).

3. **Directory Structure**:
   - `input/`: Place your PDF files here (e.g., `Raisin_Dataset.pdf`).
   - `output/`: The pipeline will generate `insights.json` and `embeddings.json` in this directory.

## Usage

1. Place your PDF file (e.g., `Raisin_Dataset.pdf`) in the `input/` directory.

2. **Start the Airflow webserver** (if not already running):

```bash
airflow webserver -p 8080
```

3. **Start the Airflow scheduler** (if not already running):

```bash
airflow scheduler
```

4. **Trigger the DAG**:
   You can trigger the DAG manually from the Airflow UI by navigating to [http://localhost:8080](http://localhost:8080), logging in, and manually triggering the `pdf_to_insights_pipeline` DAG.

5. The pipeline will:
   - Extract text from the PDF.
   - Chunk the text into smaller pieces.
   - Generate text embeddings for each chunk.
   - Analyze the embeddings for insights.
   - Save the embeddings and insights as JSON files in the `output/` directory.

## Output

After the DAG runs successfully, the following files will be generated in the `output/` directory:

- `embeddings.json`: Contains the embeddings for each chunk of text extracted from the PDF.
- `insights.json`: Contains the analysis or insights derived from the embeddings (e.g., similarity analysis).

## Example of `insights.json`

```json
{
  "insights": [
    {
      "chunk_id": 1,
      "embedding": [0.12, 0.45, ...],
      "similarity_score": 0.98
    },
    {
      "chunk_id": 2,
      "embedding": [0.33, 0.22, ...],
      "similarity_score": 0.92
    }
  ]
}
```

## DAG Details

### Tasks in the DAG:
1. **extract_text**: Extracts text from the PDF file.
2. **chunk_text**: Splits the extracted text into manageable chunks.
3. **generate_embeddings**: Creates embeddings for each text chunk using the `SentenceTransformer` model.
4. **analyze_embeddings_for_insights**: Analyzes the embeddings to generate insights (e.g., clustering or similarity).
5. **save_insights**: Saves the insights (in `insights.json`).
6. **save_embeddings**: Saves the embeddings (in `embeddings.json`).

### Dependencies:

- Task 1 (`extract_text`) must run before Task 2 (`chunk_text`).
- Task 2 must complete before Task 3 (`generate_embeddings`).
- Task 3 must complete before Task 4 (`analyze_embeddings_for_insights`).
- Task 4 must complete before Task 5 (`save_insights`).
- Task 3 must also complete before Task 6 (`save_embeddings`).



# Apache Airflow Installation on Windows

We will install Apache Airflow on Windows using the Windows Subsystem for Linux (WSL) environment.

## 1. Install WSL Environment

To install WSL and set up Ubuntu, run the following command in your CMD terminal:

```bash
wsl --install Ubuntu
```

## 2. Install Apache Airflow in WSL

Once WSL is installed, type `wsl` in the CMD terminal to open Ubuntu. Follow the steps below to install Apache Airflow.

### 2.1 Update System Packages

Update your system packages:

```bash
sudo apt update
sudo apt upgrade
```

### 2.2 Install PIP

To install Python’s package installer (PIP), run the following commands:

```bash
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python-setuptools
sudo apt install python3-pip
```

### 2.3 Modify `wsl.conf` File

Run `sudo nano /etc/wsl.conf` and insert the block below. Save and exit using `Ctrl+S` and `Ctrl+X`:

```ini
[automount]
root = /
options = "metadata"
```

### 2.4 Set Up Airflow Home Directory

To set up your Airflow home directory, run:

```bash
nano ~/.bashrc
```

Insert the following line in the `.bashrc` file, save, and exit:

```bash
export AIRFLOW_HOME=/mnt/c/users/YOURNAME/airflowhome
```

For example:

```bash
export AIRFLOW_HOME=/mnt/c/users/Devanshu/airflowhome
```

### 2.5 Install Virtualenv

Install `virtualenv` to create a virtual environment:

```bash
sudo apt install python3-virtualenv
```

### 2.6 Create and Activate Virtual Environment

Create and activate your virtual environment with the following commands:

```bash
python3 -m venv airflow_env
source airflow_env/bin/activate
```

### 2.7 Install Apache Airflow

Now, install Apache Airflow:

```bash
pip install apache-airflow
```

### 2.8 Verify Airflow Installation

To check if Airflow was installed properly, run:

```bash
airflow info
```

If there are no errors, proceed. If any dependencies are missing, install them.

### 2.9 Initialize Airflow Database

To initialize the database (by default, SQLite is used), run:

```bash
airflow db init
```

If you get an "Operation is not Permitted" error, ensure you have write access to the `$AIRFLOW_HOME` directory from WSL. You can give write permission with the following command:

```bash
sudo chmod -R 777 /mnt/c/Users/YourName/Documents/airflow/
```

### 2.10 Create Airflow User

To create an Airflow user, run:

```bash
airflow users create \
  --email johndoe@example.com \
  --firstname John \
  --lastname Doe \
  --password password123 \
  --role Admin \
  --username johndoe
```

### 2.11 Start the Webserver

Start the Airflow webserver by running:

```bash
airflow webserver
```

Visit `http://localhost:8080/` in your browser. If any errors appear, check the logs for missing dependencies.

#### Example Web UI Screenshots

**Airflow Web UI:**

![img](https://github.com/user-attachments/assets/fef01a51-5579-424e-8b57-7c6a20a7adab)

**Next UI Page:**

![img](https://github.com/user-attachments/assets/06ecdd3f-acb4-42a0-a6cc-c07a7abe61cc)

---

## 3. Start Airflow Scheduler

In a new terminal, enter WSL and activate your virtual environment again:

```bash
wsl
source airflow_env/bin/activate
```

Then start the scheduler:

```bash
airflow scheduler
```

---

## 4. Troubleshooting Configuration

If you encounter an error about the "job table not found," ensure the following setting exists in the `airflow.cfg` file:

```ini
[webserver]
rbac = True
```

---

## 5. Create a DAG Folder

In your Airflow home directory on your C: drive, create a `dags` folder:

```bash
mkdir -p /mnt/c/users/YOURNAME/airflowhome/dags
```

Place your DAG Python files inside the `dags` folder.

like the working.py file uploaded
Sure! Here's how you can structure the content for your GitHub `README.md` file using proper markdown format:


### Explanation of Folder Structure:
- **`airflow.cfg`**: The main configuration file for Airflow.
- **`airflow.db`**: The default SQLite database where Airflow stores metadata. (This may vary depending on your database configuration.)
- **`dags/`**: Contains your Directed Acyclic Graphs (DAGs), which define your workflows in Airflow.
- **`logs/`**: Logs for each task in your DAGs are stored here.
- **`plugins/`** (optional): Custom Airflow plugins.
- **`unittests/`** (optional): Unit tests for your DAGs or other components.

You can modify or add additional folders based on your project’s requirements.

## 6. Refresh Airflow UI

Finally, refresh the Airflow UI at `http://localhost:8080/` to view your DAGs.

---

That's it! You've successfully set up Apache Airflow on Windows using WSL.
```
