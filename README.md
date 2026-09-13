 🎵 Spotify Data Engineering Pipeline

An end-to-end **Spotify data engineering pipeline** that extracts data from the Spotify API, transforms it using Python and Pandas, and loads it into PostgreSQL. The entire ETL workflow is orchestrated using **Apache Airflow** and containerized with **Docker**.

---

 🚀 Project Overview

This project demonstrates a complete batch ETL pipeline:

```text
Spotify API
     │
     ▼
Python / Spotipy
     │
     ▼
Raw JSON Data
     │
     ▼
Pandas Transformation
     │
     ├──────────────┐
     ▼              ▼
Albums          Artists
     │              │
     └──────┬───────┘
            ▼
          Songs
            │
            ▼
       PostgreSQL
```

Apache Airflow is used to orchestrate the entire workflow.

---

 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │    Spotify API   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Python / Spotipy │
                    │     Extract      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Airflow Task   │
                    │     Extract      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Pandas Transform │
                    │  Data Cleaning   │
                    └────────┬─────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │       PostgreSQL            │
              │                             │
              │  ┌────────┐ ┌──────────┐   │
              │  │ albums │ │ artists  │   │
              │  └────────┘ └──────────┘   │
              │       ┌─────────┐           │
              │       │  songs  │           │
              │       └─────────┘           │
              └─────────────────────────────┘

                 Orchestrated by
                  Apache Airflow
                 Dockerized Setup
```

---

## ⚙️ ETL Workflow

### 1. Extract

The pipeline connects to the Spotify API using **Spotipy** and retrieves recently played Spotify track information.

The extracted response contains information such as:

* Song
* Artist
* Album
* Album release date
* Track duration
* Track ID
* Artist ID
* Album ID
* Added timestamp

---

### 2. Transform

Python and Pandas are used to convert the API response into structured DataFrames.

Three datasets are generated:

#### Albums

```text
album_id
album_name
release_date
total_tracks
```

#### Artists

```text
artist_id
artist_name
```

#### Songs

```text
song_id
song_name
duration_ms
added_at
album_id
artist_id
```

The transformation process also:

* Removes duplicate albums
* Removes duplicate artists
* Converts release dates to datetime
* Converts song timestamps to datetime
* Structures nested Spotify API responses into tabular data

---

### 3. Load

The transformed data is loaded into PostgreSQL.

Three tables are created:

```text
albums
artists
songs
```

Primary keys are used to prevent duplicate records.

The pipeline uses:

```sql
ON CONFLICT DO NOTHING
```

to avoid inserting duplicate records when the pipeline runs again.

---

## 🔄 Airflow Orchestration

Apache Airflow manages the ETL workflow through two tasks:

```text
extract
   │
   ▼
transform_and_load
```

### Extract Task

Responsible for:

* Calling Spotify API
* Retrieving Spotify data
* Passing the extracted data to the next task

### Transform & Load Task

Responsible for:

* Creating Pandas DataFrames
* Cleaning and transforming data
* Connecting to PostgreSQL
* Creating database tables
* Loading transformed records

The DAG is configured with:

```python
schedule="@daily"
catchup=False
```

---

## 🐳 Docker

The Airflow environment is containerized using Docker.

The project uses:

* Apache Airflow
* PostgreSQL
* Redis
* CeleryExecutor
* Docker Compose

The Airflow services include:

```text
airflow-webserver
airflow-scheduler
airflow-worker
airflow-triggerer
```

Docker provides a reproducible environment for running the orchestration layer.

---

## 🗄️ Database Design

The PostgreSQL database contains three primary tables.

### Albums

```text
albums
├── album_id         PRIMARY KEY
├── album_name
├── release_date
└── total_tracks
```

### Artists

```text
artists
├── artist_id        PRIMARY KEY
└── artist_name
```

### Songs

```text
songs
├── song_id          PRIMARY KEY
├── song_name
├── duration_ms
├── added_at
├── album_id
└── artist_id
```

The tables provide a simple relational structure for storing Spotify listening data.

---

## 🛠️ Tech Stack

| Technology     | Purpose                    |
| -------------- | -------------------------- |
| Python         | ETL development            |
| Spotipy        | Spotify API integration    |
| Pandas         | Data transformation        |
| PostgreSQL     | Data storage               |
| psycopg2       | PostgreSQL connectivity    |
| Apache Airflow | Workflow orchestration     |
| Docker         | Containerization           |
| Docker Compose | Multi-container management |
| Redis          | Airflow Celery broker      |

---

## 📁 Project Structure

```text
Spotify_datapipeline/
│
├── dags/
│   ├── spotify_dag.py
│   ├── spotify_api_extract.py
│   └── transformation_load.py
│
├── config/
├── logs/
├── plugins/
├── airflow_cache/
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── README.md
└── .env
```

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aditech95/Spotify-data-pipeline.git

cd Spotify-data-pipeline
```

### 2. Configure environment variables

Create a `.env` file containing your Spotify API and PostgreSQL configuration.

Example:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

SPOTIFY_DB_HOST=your_database_host
SPOTIFY_DB_NAME=spotify_db
SPOTIFY_DB_USER=postgres
SPOTIFY_DB_PASSWORD=your_password
```

**Never commit your actual credentials or `.env` file to GitHub.**

### 3. Start the Docker environment

```bash
docker compose up -d
```

### 4. Check running services

```bash
docker compose ps
```

### 5. Open Airflow

Open:

```text
http://localhost:8081
```

Login using the Airflow credentials configured in your environment.

### 6. Trigger the DAG

<img width="1891" height="780" alt="Screenshot 2026-09-13 220301" src="https://github.com/user-attachments/assets/3891d4aa-bab5-4811-a86f-f05d017a18b4" />




Open:

```text
spotify_etl_pipeline
```

and trigger the DAG manually.

---

## 📊 Pipeline Result

After a successful DAG execution, the PostgreSQL database contains:

```text
spotify_db
│
└── public
    ├── albums
    ├── artists
    └── songs
```

<img width="1360" height="742" alt="Screenshot 2026-09-13 222722" src="https://github.com/user-attachments/assets/b309a4e5-bd34-4e5a-aa0b-db3442bb42f6" />
<img width="992" height="712" alt="Screenshot 2026-09-13 222755" src="https://github.com/user-attachments/assets/6c2970af-eff2-4706-88ff-fde2bfe2a137" />
<img width="1653" height="790" alt="Screenshot 2026-09-13 222833" src="https://github.com/user-attachments/assets/841def29-141e-486b-8944-cac81fc667f6" />




The pipeline can then be queried using PostgreSQL or viewed through **pgAdmin 4**.

---

## 🎯 Key Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* REST API ingestion
* ETL pipeline development
* Python data processing
* Pandas transformations
* Relational database design
* PostgreSQL
* SQL
* Workflow orchestration
* Apache Airflow DAGs
* Docker containerization
* Docker Compose
* Celery-based task execution
* Idempotent database loading
* Handling duplicate records
* Environment-based configuration

---

## 🔮 Future Improvements

Possible improvements to make the pipeline more production-oriented:

* ☁️ Store raw data in Amazon S3
* ⚡ Add incremental ingestion
* 🔍 Add data quality checks
* 📊 Add a BI dashboard
* 🏢 Move analytics workloads to a cloud data warehouse
* 🔄 Add retry and failure notification mechanisms
* 🧱 Introduce dbt for analytics transformations
* ⚡ Introduce PySpark for larger datasets
* 📈 Add monitoring and pipeline observability

---

## 👨‍💻 Author

**Aditya Chauhan**

GitHub: [Aditech95](https://github.com/Aditech95)

---

⭐ If you found this project useful, feel free to explore the repository and connect with me on LinkedIn.
