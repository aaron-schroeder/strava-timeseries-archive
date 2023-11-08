from .adapters import (
    MultiActivityDataCSVFileExportRepository,
    StravaAPIScrapyItemActivityDataTranslator,
)

class MultiActivityDataCSVPipeline:
    def __init__(self, directory):
        self.repository = MultiActivityDataCSVFileExportRepository(directory)

    @classmethod
    def from_crawler(cls, crawler):
        repo_path = crawler.settings.get('CSV_OUTPUT_DIR')
        return cls(repo_path)
    
    def process_item(self, item, spider):
        translator = StravaAPIScrapyItemActivityDataTranslator()
        activity_data = translator.to_activity_data(item)
        self.repository.save(activity_data)
        
        return item
