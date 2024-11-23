import json
import os
import re
from urllib.parse import urlparse

from scrapy.exceptions import IgnoreRequest


class JSONDocumentDownloaderMiddleware:
    def __init__(self, directory):
        self.directory = directory

    @classmethod
    def from_crawler(cls, crawler):
        repo_path = crawler.settings.get('JSON_OUTPUT_DIR')
        return cls(repo_path)
    
    def process_request(self, request, spider):
        # Check if a file already exists at 
        # {JSON_OUTPUT_DIR}/{get_resource_subpath(request.url)}
        # (IF the request is not /athlete/activities)
        subpath = _get_resource_subpath(request.url)
        if subpath != '/athlete/activities' and self._data_exists(subpath):
            raise IgnoreRequest

    def process_response(self, request, response, spider):
        subpath = _get_resource_subpath(request.url)
        if subpath == '/athlete/activities':
            # Save all `SummaryActivity` entities from the list
            for summary_activity in response.json():
                relative_file_path = f'activities/{summary_activity["id"]}/summary.json'
                self._save_data(summary_activity, relative_file_path)
        elif re.match(r'^/activities/(\d+)/streams$', subpath):
            # Save the `StreamSet` entity
            relative_file_path = subpath.strip('/') + '.json'
            resource_data = response.json()
            # De-facto data validation: if the response data matches the 
            # expected format (a list of `Stream` entities), save as-is.
            # If the response data indicates an error (assumed to be 404
            # due to the activity not having streams), save an empty list
            # which is equivalent to an empty streamset. 
            if isinstance(resource_data, list):
                self._save_data(resource_data, relative_file_path)
            elif resource_data.get('error', None) == 'No resource found.':
                self._save_data([], relative_file_path)
        elif re.match(r'^/activities/(\d+)$', subpath):
            # Save the `DetailedActivity` entity
            relative_file_path = subpath.strip('/') + '.json'
            resource_data = response.json()
            self._save_data(resource_data, relative_file_path)
        return response

    def _data_exists(self, subpath):
        relative_file_path = subpath.strip('/') + '.json'
        file_path = os.path.join(self.directory, relative_file_path)
        return os.path.exists(file_path)

    def _save_data(self, data, relative_file_path):
        file_path = os.path.join(self.directory, relative_file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)        
        with open(file_path, 'w') as f:
            json.dump(data, f)

def _get_resource_subpath(url: str):
    subpath = urlparse(url).path
    if subpath.startswith('/proxy'):
        return subpath[6:]
    return subpath