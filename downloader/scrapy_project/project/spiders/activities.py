from urllib.parse import parse_qs, urlparse

import scrapy
import scrapy.exceptions
import scrapy.http


class AthleteActivitiesStravaAPISpider(scrapy.Spider):
    name = 'activities'
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
            this_pg = int(url_params.get('page', [1])[0])
            yield self._create_activities_list_request(page=this_pg + 1)

        for activity_summary in data:
            yield self._create_activity_streams_request(activity_summary)

    def parse_activity_streams(self, response):
        streams_data = response.json()
        
        if not isinstance(streams_data, list) or not len(streams_data):
            raise scrapy.exceptions.DropItem
        
        yield {
            'id': response.meta['id'],
            'start_date': response.meta['start_date'],
            'type': response.meta['type'],
            'streams': streams_data,
        }

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