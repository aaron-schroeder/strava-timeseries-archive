BOT_NAME = "project"

SPIDER_MODULES = ["project.spiders"]
NEWSPIDER_MODULE = "project.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "project.pipelines.MultiActivityDataCSVPipeline": 333,
    "project.pipelines.JSONDocumentPipeline": 343,
}

CSV_OUTPUT_DIR = "."  # used with MultiActivityDataCSVPipeline

JSON_OUTPUT_DIR = "." # used with JSONDocumentPipeline

# DOWNLOAD_DELAY = 0       # default 0?
# CONCURRENT_ITEMS = 10    # default 100
# CONCURRENT_REQUESTS = 5  # default 16

AUTOTHROTTLE_ENABLED = True             # default False
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.67  # default 1.0
AUTOTHROTTLE_MAX_DELAY = 60             # default 60

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
TWISTED_REACTOR = "twisted.internet.epollreactor.EPollReactor"
FEED_EXPORT_ENCODING = "utf-8"