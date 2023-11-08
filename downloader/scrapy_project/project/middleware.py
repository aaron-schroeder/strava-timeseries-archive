from scrapy.exceptions import IgnoreRequest

from .adapters import MultiActivityDataCSVFileExportRepository


class MultiActivityDataCSVDownloaderMiddleware:
    def __init__(self, directory):
        self.repository = MultiActivityDataCSVFileExportRepository(directory)

    @classmethod
    def from_crawler(cls, crawler):
        repo_path = crawler.settings.get('CSV_OUTPUT_DIR')
        return cls(repo_path)
    
    def process_request(self, request, spider):
        activity_id = request.meta.get('activity_id', False)
        if activity_id and self.repository.exists(activity_id):
            raise IgnoreRequest(f'Ignoring Activity #{activity_id}. Repository '
                                f'already contains ActivityData with this ID.')
