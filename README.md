# Spotify Data Pipeline 🎵

An end-to-end ETL (Extract, Transform, Load) data pipeline built with Python and PostgreSQL.

## Architecture

Spotify API → Python (Extract) → Pandas (Transform) → PostgreSQL (Load)

## What it does

- **Extracts** playlist data from Spotify API using Spotipy
- **Transforms** raw nested JSON into clean, structured tables
- **Loads** data into a local PostgreSQL database

## Database Schema

**albums** — album_id, album_name, release_date, total_tracks  
**artists** — artist_id, artist_name  
**songs** — song_id, song_name, duration_ms, added_at, album_id, artist_id

## Tech Stack

- Python 3.x
- Spotipy (Spotify API wrapper)
- Pandas
- PostgreSQL
- psycopg2

## Setup

1. Clone the repository
   
   git clone https://github.com/Aditech95/spotify-data-pipeline

2. Install dependencies
   
   pip install -r requirements.txt

3. Create `.env` file with your credentials
   
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
   DB_HOST=localhost
   DB_NAME=spotify_db
   DB_USER=postgres
   DB_PASSWORD=your_password

4. Run the pipeline
   
   python transfromation_load.py

## Project Structure

spotify-data-pipeline/
├── spotify_api_extract.py      # Extract: Spotify API se data fetch
├── transfromation_load.py      # Transform + Load: Clean data → PostgreSQL
├── .env                        # Credentials (not pushed to GitHub)
├── .gitignore
└── README.md

## Output

Pipeline successfully loads 3 normalized tables into PostgreSQL:
- Songs with duration and timestamps
- Artists deduplicated across tracks  
- Albums with release dates
