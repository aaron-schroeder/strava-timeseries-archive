## Start the Strava API middleware service
```
docker-compose --env-file secrets.env up
```

Without docker:
```
cd strava-api-middleware/
pip install -r requirements.txt
STRAVA_OAUTH_CLIENT_ID=${CLIENT_ID}  \
STRAVA_OAUTH_CLIENT_SECRET=${CLIENT_SECRET}  \
STRAVA_OAUTH_TOKEN_STORAGE_DIR=../../data  \
flask --app flask_app.app run
```

## Install spider dependencies
Activate virtual environment, then:
```
pip install -r downloader/requirements.txt
cd downloader/scrapy_project
```

## Adjust spider settings
```
cd downloader/
```
Modify scrapy_project/settings.py: adjust DOWNLOAD_DELAY for your RL situation

## Run spider
```
scrapy crawl activities -s CSV_OUTPUT_DIR=${OUT_DIR}
```
