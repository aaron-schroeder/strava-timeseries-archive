import datetime

import flask


class RateLimit:
    def __init__(self):
        self.lifts_at = datetime.datetime.utcnow()

    def update_from(self, response: flask.Response):
        if response.status_code == 429:
            self.lifts_at = get_next_quarter_hour()
        # TODO: Finish
        # usage = response.headers.get('X-Ratelimit-Usage') ...

    @property
    def is_active(self):
        return self.lifts_at > datetime.datetime.utcnow()
    

def get_next_quarter_hour():
    now = datetime.datetime.utcnow()
    fifteen_mins_from_now = now + datetime.timedelta(minutes=15)
    next_qtr_hr = fifteen_mins_from_now.replace(second=0, microsecond=0)  \
        + datetime.timedelta(minutes=-(fifteen_mins_from_now.minute % 15))
    return next_qtr_hr