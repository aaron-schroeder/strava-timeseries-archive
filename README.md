# strava-timeseries-archive
> Download all the time series data in your Strava account history
> - into a single CSV file
> - into JSON files, one per activity

This app solves a number of problems you'd encounter when downloading personal
activity data in bulk from the Strava API.
- Guides you through Strava's OAuth 2.0 flow and manages your credentials
- Provides a proxy server that forwards your HTTP requests to Strava's API server.
  - The proxy automatically adds your OAuth credentials to requests. 
  - The app also monitors your rate limit status with the Strava API and avoids 
    sending requests to the live resource server when a rate limit is in effect.
    This is important because these requests stil count towards the rate limit,
    even though the server returns no information. A "gotcha" moment can occur
    when you exhaust your app's 24-hour request allowance during a shorter-term
    15-minute rate limit.
- Provides a scrapy spider as a straightforward way to download all your time 
  series data, representing potentially thousands of activity time series, each with 
  potentially thousands of samples, from the Strava API by way of the proxy server.

# How to download your data

## Step 1: Start up the Strava API middleware service

### Step 1.0: Create a Strava API Application (one time only)

Follow the [instructions here](https://developers.strava.com/docs/getting-started/#account) 
(just the part about creating an acount). Make a note of your app's
client ID and client secret; you will need them in a bit.

### Step 1.1: Run the application

#### Option A: Run the Docker container

Create a `secrets.env` file, and include values for `STRAVA_OAUTH_CLIENT_ID`
and `STRAVA_OAUTH_CLIENT_SECRET`. Then run the following command:

```
docker-compose --env-file secrets.env up
```

#### Option B: Install and run the Flask app

```
cd strava-api-middleware/
pip install -r requirements.txt
STRAVA_OAUTH_CLIENT_ID=${CLIENT_ID}  \
STRAVA_OAUTH_CLIENT_SECRET=${CLIENT_SECRET}  \
STRAVA_OAUTH_TOKEN_STORAGE_DIR=../../data  \
flask --app flask_app.app run
```

### Step 1.2: Complete a handshake with the Strava API (one-time)

The Strava API middleware service exposes an endpoint at http://127.0.0.1:5000.
On your first time using the service, you'll need to grant it permission
to access your activity data through the Strava API. From you point of view,
there is really no "other" party to whom you're providing access; you are simply
granting permission for the app you're running to access your own data.
I imagine shaking hands with myself.

## Step 2: Run `downloader`

### Step 2.0: Install spider dependencies (one-time)

Activate the downloader's virtual environment, then:
```
pip install -r downloader/requirements.txt
```

### Step 2.1: Adjust spider settings

Modify `downloader/scrapy_project/project/settings.py` to meet your needs.

Decide whether you'd like to download your time series data into a single
large CSV file, many small JSON files, or both. Designate your choice by
commenting/uncommenting each pipeline within the `ITEM_PIPELINES` setting.
Be sure to set the desired output directory for each activated pipeline
using the settings `CSV_OUTPUT_DIR` and/or `JSON_OUTPUT_DIR`.

Adjust `DOWNLOAD_DELAY` and `AUTOTHROTTLE_TARGET_CONCURRENCY` to suit your
app's rate limit situation. At the time of this writing (November 8, 2023)
the default limits for new apps are 100 requests per 15 minute interval and
1000 requests per day.^[https://communityhub.strava.com/t5/developer-knowledge-base/rate-limits/ta-p/4289]

### Step 2.2: Run the spider

```
cd downloader/project
scrapy crawl activities
```
