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

AIRFLOW_HOME/
│
├── airflow.cfg            # Main Airflow configuration file
├── airflow.db             # SQLite database (or other DB depending on configuration)
├── dags/                  # Folder containing your DAGs (Python files)
│   ├── example_dag.py     # Example DAG file (if any)
│   └── ...                # Other DAG files you create
├── logs/                  # Folder to store task logs
│   ├── <dag_id>/          # Logs are stored per DAG
│   │   ├── <task_id>/     # Logs are stored per task within a DAG
│   │   └── <execution_date>/  # Logs for each task instance
│   └── ...                # Logs for other DAGs and tasks
├── plugins/               # Folder for Airflow plugins (optional)
│   └── ...                # Custom plugins for Airflow
└── unittests/             # Folder for unit tests (optional)


---

## 6. Refresh Airflow UI

Finally, refresh the Airflow UI at `http://localhost:8080/` to view your DAGs.

---

That's it! You've successfully set up Apache Airflow on Windows using WSL.
```
