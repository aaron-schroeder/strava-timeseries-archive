from urllib.parse import parse_qs, urlparse

import scrapy
import scrapy.exceptions
import scrapy.http

from project.adapters_v2 import StravaAPIResponseRecordAdapter


class AthleteActivitiesStravaAPISpider(scrapy.Spider):
    name = 'activities_v2'
    url_base = 'http://localhost:5000/proxy'

    def start_requests(self):
        yield self._create_activities_list_request(page=1)
    
    def parse_summary_list_page(self, response):
        data = response.json()

        # crude format validation
        if not isinstance(data, list):
            raise scrapy.exceptions.DropItem

        # If the Strava API returned exactly the requested number of results, 
        # there *might* be more activities on the next page.
        if len(data) == 200:
            url_params = parse_qs(urlparse(response.request.url).query)
            next_pg = int(url_params.get('page', [1])[0]) + 1
            yield self._create_activities_list_request(page=next_pg)

        for activity_summary in data:
            yield self._create_activity_streams_request(activity_summary)

    def parse_activity_streams(self, response):
        response_adapter = StravaAPIResponseRecordAdapter()
        for record in response_adapter.generate_records(response):
            yield record

    def _create_activities_list_request(self, page=1):
        return scrapy.http.Request(
            f'{self.url_base}/athlete/activities?per_page=200&page={page}',
            callback=self.parse_summary_list_page, dont_filter=True)
    
    def _create_activity_streams_request(self, activity_summary):
        all_available_keys = ('time,cadence,distance,altitude,velocity_smooth,'
                              'heartrate,latlng,watts,temp,moving,grade_smooth')

        streams_resource_url = (
            f'{self.url_base}/activities/{activity_summary["id"]}/streams'
            f'?keys={all_available_keys}')
        
        return scrapy.http.Request(
            streams_resource_url,
            meta={'id': activity_summary['id'],
                  'start_date': activity_summary['start_date'],
                  'type': activity_summary['type']},
            callback=self.parse_activity_streams
        )