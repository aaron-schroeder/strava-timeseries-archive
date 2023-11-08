from scrapy import signals
from scrapy.exceptions import IgnoreRequest

from .adapters import (
    MultiActivityDataCSVFileExportRepository,
    StravaAPIScrapyItemActivityDataTranslator,
)

class MultiActivityDataCSVExporter:
    def __init__(self, crawler):
        repo_path = crawler.settings.get('CSV_OUTPUT_DIR')
        self.repository = MultiActivityDataCSVFileExportRepository(repo_path)
        
        crawler.signals.connect(self.request_reached_downloader, 
                                signal=signals.request_reached_downloader)
        crawler.signals.connect(self.process_item, 
                                signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def request_reached_downloader(self, request, spider):
        activity_id = request.meta.get('activity_id', False)
        if activity_id and self.repository.exists(activity_id):
            raise IgnoreRequest(f'Ignoring Activity #{activity_id}. Repository '
                                f'already contains ActivityData with this ID.')
    def process_item(self, item, spider):
        translator = StravaAPIScrapyItemActivityDataTranslator()
        activity_data = translator.to_activity_data(item)
        self.repository.save(activity_data)
        
        return item