import datetime

import pandas as pd
import scrapy.exceptions

import dddhns.domain.language as lang
from dddhns.domain.model import ActivityData, Timeseries
from project.items import Record


class StravaAPIResponseRecordAdapter:
    def generate_records(self, response):
        response_translator = StravaAPIResponseActivityDataTranslator()
        activity_data = response_translator.to_activity_data(response)
        ts_df = activity_data.get_timeseries()
        for ix, row in ts_df.iterrows():
            kwargs = dict(
                activity_id=activity_data.id,
                activity_type=activity_data.type,
                timestamp=ix,
            )
            kwarg_to_var_dict = dict(
                lat=lang.LAT,
                lon=lang.LON,
                distance=lang.DISTANCE,
                elevation=lang.ELEVATION,
                speed=lang.SPEED,
                cadence=lang.CADENCE,
                heartrate=lang.HEARTRATE,
                grade_smooth=lang.GRADE_SMOOTH,
            )
            kwargs.update({kwarg: row.get(var)
                           for kwarg, var in kwarg_to_var_dict.items()})
            yield Record(**kwargs)


class StravaAPIResponseActivityDataTranslator:
    def to_activity_data(self, response) -> ActivityData:
        self._validate(response)

        return ActivityData(id=response.meta['id'], 
                            type=response.meta['type'],
                            timeseries=self._to_timeseries(response))

    def _validate(self, response):
        streams_data = response.json()
        if not isinstance(streams_data, list) or not len(streams_data):
            raise scrapy.exceptions.DropItem
        
    def _to_timeseries(self, response) -> Timeseries:
        dataframe = pd.DataFrame({stream['type']: stream['data']
                                  for stream in response.json()})

        start_dt_utc = datetime.datetime.strptime(response.meta['start_date'], 
                                                  '%Y-%m-%dT%H:%M:%SZ')
        dataframe[lang.TIMESTAMP] = start_dt_utc   \
            + pd.to_timedelta(dataframe[lang.TIME], unit='s')
        dataframe = dataframe.set_index(lang.TIMESTAMP)

        if 'latlng' in dataframe.columns:
            dataframe[[lang.LAT, lang.LON]] = [(val[0], val[1])
                                               for val in dataframe['latlng']]

        available_variables = set(lang.VARIABLES) & set(dataframe.columns)
        dataframe = dataframe[list(available_variables)]
        
        return Timeseries(dataframe)