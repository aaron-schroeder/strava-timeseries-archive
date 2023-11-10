import json
import os

from .adapters import (
    MultiActivityDataCSVFileExportRepository,
    StravaAPIScrapyItemActivityDataTranslator,
)
from .items import SummaryActivity, StreamSet


class MultiActivityDataCSVPipeline:
    def __init__(self, directory):
        self.repository = MultiActivityDataCSVFileExportRepository(directory)

    @classmethod
    def from_crawler(cls, crawler):
        repo_path = crawler.settings.get('CSV_OUTPUT_DIR')
        return cls(repo_path)
    
    def process_item(self, item, spider):
        if isinstance(item, StreamSet):
            translator = StravaAPIScrapyItemActivityDataTranslator()
            activity_data = translator.to_activity_data(item)
            self.repository.save(activity_data)
        
        return item


class JSONDocumentPipeline:
    def __init__(self, directory):
        self.directory = directory

    @classmethod
    def from_crawler(cls, crawler):
        repo_path = crawler.settings.get('JSON_OUTPUT_DIR')
        return cls(repo_path)
    
    def process_item(self, item, spider):
        if isinstance(item, (SummaryActivity, StreamSet)):
            activity_directory = os.path.join(self.directory, 
                                              'activities/',
                                              str(item.get('activity_id')))
            fname = 'summary.json' if isinstance(item, SummaryActivity)  \
                    else 'streams.json'
            file_path = os.path.join(activity_directory, fname)

            resource_data = item.get('data')

            os.makedirs(activity_directory, exist_ok=True)

            with open(file_path, 'w') as f:
                json.dump(resource_data, f)
        
        return item