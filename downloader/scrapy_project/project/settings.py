BOT_NAME = "project"

SPIDER_MODULES = ["project.spiders"]
NEWSPIDER_MODULE = "project.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "project.pipelines.MultiActivityDataCSVPipeline": 333
}

# CSV_OUTPUT_DIR = "."

# DOWNLOAD_DELAY = 1

# DOWNLOAD_DELAY = 0       # dft 0?
# CONCURRENT_ITEMS = 10    # dft 100
# CONCURRENT_REQUESTS = 5  # dft 16

AUTOTHROTTLE_ENABLED = True             # dft False
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.67  # dft 1.0
AUTOTHROTTLE_MAX_DELAY = 60             # dft 60

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
TWISTED_REACTOR = "twisted.internet.epollreactor.EPollReactor"
FEED_EXPORT_ENCODING = "utf-8"