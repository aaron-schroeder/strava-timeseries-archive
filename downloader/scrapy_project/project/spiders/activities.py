from urllib.parse import parse_qs, urlparse

import scrapy
import scrapy.exceptions
import scrapy.http

from ..items import SummaryActivity, StreamSet


class AthleteActivitiesStravaAPISpider(scrapy.Spider):
    name = 'activities'
    url_base = 'http://localhost:5000/proxy'

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
            summary_activity = SummaryActivity({
                'activity_id': activity_summary['id'],
                'data': activity_summary,
            })

            yield summary_activity

            yield self.create_activity_streams_request(summary_activity)

    def parse_activity_streams(self, response):
        streams_data = response.json()

        if not isinstance(streams_data, list) or not len(streams_data):
            raise scrapy.exceptions.DropItem

        yield StreamSet({
            'activity_id': response.meta['activity_id'],
            'start_date': response.meta['start_date'],
            'type': response.meta['type'],
            'data': streams_data,
        })

    def create_athlete_activities_request(self, page=1):
        return scrapy.http.Request(
            f'{self.url_base}/athlete/activities?per_page=200&page={page}',
            callback=self.parse_athlete_activities_page, dont_filter=True)

    def create_activity_streams_request(self, summary_activity: SummaryActivity):
        all_available_keys = ('time,cadence,distance,altitude,velocity_smooth,'
                              'heartrate,latlng,watts,temp,moving,grade_smooth')

        activity_id = summary_activity['activity_id']
        
        resource_url = (f'{self.url_base}/activities/{activity_id}'
                        f'/streams?keys={all_available_keys}')

        return scrapy.http.Request(
            resource_url,
            meta={'activity_id': activity_id,
                  'start_date': summary_activity['data']['start_date'],
                  'type': summary_activity['data']['type']},
            callback=self.parse_activity_streams
        )