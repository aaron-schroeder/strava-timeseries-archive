import datetime
import os
import pathlib

import pandas as pd

from dddhns.domain.model import ActivityData, Timeseries
import dddhns.domain.language as lang
from dddhns.repository import AbstractExportRepository
from dddhns.translation import AbstractActivityDataTranslator


class MultiActivityDataCSVFileExportRepository(AbstractExportRepository):
    def __init__(self, directory):
        os.makedirs(directory, exist_ok=True)
        self.directory = directory

        self.repo_file_path = os.path.join(self.directory, 'multi-activity.csv')
        self.metadata_file_path = os.path.join(self.directory, 'metadata.json')
        
        # Expected headers in csv file, in order.
        self.headers = lang.VARIABLES.copy()
        self.headers.extend(['id', 'type'])

        if not os.path.exists(self.repo_file_path):
            self._write_headers()

        pathlib.Path(self.metadata_file_path).touch()

    def save(self, activity_data: ActivityData):
        timeseries_df = activity_data.get_timeseries(scitype='panel')
        timeseries_df['id'] = activity_data.id
        timeseries_df['type'] = activity_data.type
        template_df = pd.DataFrame(columns=self.headers[1:])
        merged_df = pd.concat([template_df, timeseries_df], 
                              axis=0)
        merged_df.to_csv(self.repo_file_path, mode='a', header=False)

        self._write_metadata(activity_data)

    def exists(self, key) -> bool:
        with open(self.metadata_file_path, 'r') as metadata_file:
            for line in metadata_file:
                if str(key) in line:
                    return True
        return False

    def _write_metadata(self, activity_data):
        with open(self.metadata_file_path, 'a') as f:
            f.write(f'{activity_data.id}\n')

    def _write_headers(self):
        with open(self.repo_file_path, 'w') as f:
            f.write(','.join(self.headers))
            f.write('\n')


class StravaAPIScrapyItemActivityDataTranslator(AbstractActivityDataTranslator):
    def to_activity_data(self, item) -> ActivityData:
        id = item['id']
        type = item['type']
        timeseries = self._to_timeseries(item)
        return ActivityData(id, type, timeseries)

    def _to_timeseries(self, item) -> Timeseries:
        dataframe = pd.DataFrame({stream['type']: stream['data']
                                  for stream in item['streams']})

        start_dt_utc = datetime.datetime.strptime(item['start_date'], 
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