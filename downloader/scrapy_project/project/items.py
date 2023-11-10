from scrapy.item import Field, Item


class StravaAPIResourceItem(Item):
    # athlete_id = Field()
    activity_id = Field()
    data = Field()


class SummaryActivity(StravaAPIResourceItem):
    # At the moment, I just want to save all fields without validating them.
    pass


class StreamSet(StravaAPIResourceItem):
    # the actual JSON response from Strava API is in `data`
    start_date = Field()
    type = Field()