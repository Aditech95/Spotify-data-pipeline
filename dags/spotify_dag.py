import sys
sys.path.insert(0, "/opt/airflow/dags")

from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="spotify_etl_pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["spotify", "etl"],
)
def spotify_pipeline():

    @task
    def extract():

        from spotify_api_extract import extract_spotify_data

        return extract_spotify_data()

    @task
    def transform_and_load(data):

        from transformation_load import (
            create_dataframes,
            load_to_postgres
        )

        album_df, artists_df, song_df = create_dataframes(data)

        load_to_postgres(
            album_df,
            artists_df,
            song_df
        )

    raw_data = extract()

    transform_and_load(raw_data)


spotify_pipeline()