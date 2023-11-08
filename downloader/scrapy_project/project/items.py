from scrapy.item import Item, Field


class Record(Item):
    activity_id = Field()
    activity_type = Field()
    timestamp = Field()
    lat = Field()
    lon = Field()
    distance = Field()
    elevation = Field()
    speed = Field()
    cadence = Field()
    heartrate = Field()
    grade_smooth = Field()
    # temp = Field()
    # watts = Field()
    