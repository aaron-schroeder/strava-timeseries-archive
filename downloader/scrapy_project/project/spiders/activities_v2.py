from urllib.parse import parse_qs, urlparse

import scrapy
import scrapy.exceptions
import scrapy.http

from ..items import SummaryActivity, StreamSet


class NewAthleteActivitiesStravaAPISpider(scrapy.Spider):
    name = 'activities_v2'
    # url_base = 'http://localhost:5000/proxy'

    def start_requests(self):
        yield self.create_athlete_activities_request(page=1)
    
    def parse_athlete_activities_page(self, response):
        data = response.json()

        # crude format validation
        if not isinstance(data, list):
            raise scrapy.exceptions.DropItem

        # If the Strava API returned exactly the requested number of results, 
        # there *might* be more activities on the next page.
        if len(data) == 200:
            url_params = parse_qs(urlparse(response.request.url).query)
            this_pg = int(url_params.get('page', [1])[0])
            yield self.create_athlete_activities_request(page=this_pg + 1)

        for activity_summary in data:
            yield self.create_activity_streams_request(activity_summary)

    def parse_activity_streams(self, response):
        return None
        # streams_data = response.json()
        # if not isinstance(streams_data, list) or not len(streams_data):
        #     raise scrapy.exceptions.DropItem
        # yield streams_data

    def parse_activity_streams_error(self, failure):
        return None
        # if failure.value.response.status == 404:
        #     # insert item as a bad response
        #     return None

    def create_athlete_activities_request(self, page=1):
        return scrapy.http.Request(
            f'{self.settings.get("STRAVA_PROXY_SERVER_URL")}/athlete/activities'
            f'?per_page=200&page={page}',
            callback=self.parse_athlete_activities_page, dont_filter=True)

    def create_activity_streams_request(self, activity_summary):     

        all_available_keys = ('time,cadence,distance,altitude,velocity_smooth,'
                              'heartrate,latlng,watts,temp,moving,grade_smooth')

        activity_id = activity_summary['id']
        
        resource_url = (f'{self.settings.get("STRAVA_PROXY_SERVER_URL")}/'
                        f'activities/{activity_id}/streams'
                        f'?keys={all_available_keys}')

        return scrapy.http.Request(resource_url,
                                   callback=self.parse_activity_streams,
                                   errback=self.parse_activity_streams_error)
    