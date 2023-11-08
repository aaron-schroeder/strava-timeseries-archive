## Step 1: Start the Strava API middleware service

### Option 1: Run the Docker container

Create a `secrets.env` file, and include values for `STRAVA_OAUTH_CLIENT_ID`
and `STRAVA_OAUTH_CLIENT_SECRET`. Then run the following command:

```
docker-compose --env-file secrets.env up
```

### Option 2: Install and run the Flask app

```
cd strava-api-middleware/
pip install -r requirements.txt
STRAVA_OAUTH_CLIENT_ID=${CLIENT_ID}  \
STRAVA_OAUTH_CLIENT_SECRET=${CLIENT_SECRET}  \
STRAVA_OAUTH_TOKEN_STORAGE_DIR=../../data  \
flask --app flask_app.app run
```

# Step 1.5: Complete a one-time handshake with the Strava API

The Strava API middleware service exposes an endpoint at http://127.0.0.1:5000.
On your first time using the service, you'll need to grant it permission
to access your personal Strava data through the API. From you point of view,
there is really no "other" party to whom you're provide access; you are simply
granting permission for the app you're running to access your own data.
I imagine it like shaking hands with myself.

## Step 2: Run `downloader`

### Setup: Install spider dependencies

Activate the downloader's virtual environment, then:
```
pip install -r downloader/requirements.txt
```

### Setup: Adjust spider settings

Modify `downloader/project/settings.py`: adjust `DOWNLOAD_DELAY` and `AUTOTHROTTLE_TARGET_CONCURRENCY` to suit your app's rate limit situation. 
At the time of this writing (November 8, 2023) the default limits for new
apps are 100 requests per 15 minute interval and 1000 requests per day.^[https://communityhub.strava.com/t5/developer-knowledge-base/rate-limits/ta-p/4289]/

### Run spider

```
cd downloader/project
scrapy crawl activities
```
