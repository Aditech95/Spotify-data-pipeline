import sys
sys.path.insert(0, "/opt/airflow/dags")

import os
import pandas as pd
from dotenv import load_dotenv
from spotify_api_extract import extract_spotify_data
import psycopg2

load_dotenv()


def album(data):
    album_list = []

    for row in data['items']:
        album_id = row['item']['album']['id']
        album_name = row['item']['album']['name']
        album_release_date = row['item']['album']['release_date']
        album_total_tracks = row['item']['album']['total_tracks']

        album_element = {
            'album_id': album_id,
            'album_name': album_name,
            'release_date': album_release_date,
            'total_tracks': album_total_tracks
        }

        album_list.append(album_element)

    return album_list


def artists(data):
    artist_list = []

    for row in data['items']:
        for artist in row['item']['artists']:

            artist_element = {
                'artist_id': artist['id'],
                'artist_name': artist['name']
            }

            artist_list.append(artist_element)

    return artist_list


def songs(data):
    song_list = []

    for row in data['items']:

        song_element = {
            'song_id': row['item']['id'],
            'song_name': row['item']['name'],
            'duration_ms': row['item']['duration_ms'],
            'added_at': row['added_at'],
            'album_id': row['item']['album']['id'],
            'artist_id': row['item']['artists'][0]['id']
        }

        song_list.append(song_element)

    return song_list


def create_dataframes(data):

    album_df = pd.DataFrame(album(data))
    artists_df = pd.DataFrame(artists(data))
    song_df = pd.DataFrame(songs(data))

    # Remove duplicate albums and artists
    album_df = album_df.drop_duplicates(subset=['album_id'])
    artists_df = artists_df.drop_duplicates(subset=['artist_id'])

    # Convert date columns
    album_df['release_date'] = pd.to_datetime(
        album_df['release_date']
    )

    song_df['added_at'] = pd.to_datetime(
        song_df['added_at']
    )

    return album_df, artists_df, song_df


def load_to_postgres(album_df, artists_df, song_df):

    conn = psycopg2.connect(
        host=os.getenv('SPOTIFY_DB_HOST'),
        database=os.getenv('SPOTIFY_DB_NAME'),
        user=os.getenv('SPOTIFY_DB_USER'),
        password=os.getenv('SPOTIFY_DB_PASSWORD')
    )

    cur = conn.cursor()

    # -------------------------
    # Albums table
    # -------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            album_id VARCHAR PRIMARY KEY,
            album_name VARCHAR,
            release_date DATE,
            total_tracks INT
        )
    """)

    # -------------------------
    # Artists table
    # -------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            artist_id VARCHAR PRIMARY KEY,
            artist_name VARCHAR
        )
    """)

    # -------------------------
    # Songs table
    # -------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            song_id VARCHAR PRIMARY KEY,
            song_name VARCHAR,
            duration_ms INT,
            added_at TIMESTAMP,
            album_id VARCHAR,
            artist_id VARCHAR
        )
    """)

    # -------------------------
    # Insert Albums
    # -------------------------

    for _, row in album_df.iterrows():

        cur.execute("""
            INSERT INTO albums (
                album_id,
                album_name,
                release_date,
                total_tracks
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (album_id) DO NOTHING
        """, (
            row['album_id'],
            row['album_name'],
            row['release_date'],
            row['total_tracks']
        ))

    # -------------------------
    # Insert Artists
    # -------------------------

    for _, row in artists_df.iterrows():

        cur.execute("""
            INSERT INTO artists (
                artist_id,
                artist_name
            )
            VALUES (%s, %s)
            ON CONFLICT (artist_id) DO NOTHING
        """, (
            row['artist_id'],
            row['artist_name']
        ))

    # -------------------------
    # Insert Songs
    # -------------------------

    for _, row in song_df.iterrows():

        cur.execute("""
            INSERT INTO songs (
                song_id,
                song_name,
                duration_ms,
                added_at,
                album_id,
                artist_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (song_id) DO NOTHING
        """, (
            row['song_id'],
            row['song_name'],
            row['duration_ms'],
            row['added_at'],
            row['album_id'],
            row['artist_id']
        ))

    # Commit changes
    conn.commit()

    # Close connection
    cur.close()
    conn.close()

    print("Data successfully loaded to PostgreSQL!")


# This section runs only when this file is executed directly.
# Airflow will call the functions above instead.
if __name__ == "__main__":

    data = extract_spotify_data()

    album_df, artists_df, song_df = create_dataframes(data)

    print("=========== ALBUMS =========")
    print(album_df)

    print("=========== ARTISTS =========")
    print(artists_df)

    print("=========== SONGS =========")
    print(song_df)

    load_to_postgres(
        album_df,
        artists_df,
        song_df
    )