from typing import Dict, List, Optional, Type

import pandas as pd

from dddhns.domain import language as lang


class Entity:
    pass


class AggregateRoot(Entity):
    pass


class ValueObject:
    pass


class Timeseries(ValueObject):
    def __init__(self, data: pd.DataFrame):
        errors = self.get_validation_errors(data)
        if len(errors):
            raise ValueError('Errors: \n', '\n'.join(errors))
        self.data = data

    @staticmethod
    def get_validation_errors(data: pd.DataFrame) -> List[str]:
        errors = []
        if data.empty:
            errors.append('Timeseries data is empty.')
        # if not data.index.is_unique:
        #     duplicated_ix = data.index[data.index.duplicated()]
        #     errors.append('Timeseries index must be unique and ascending. '
        #                   'Duplicated index(es): ' + str(duplicated_ix))
        if not data.columns.isin(lang.VARIABLES).all():
            errors.append('Unexpected columns found in timeseries DataFrame: '
                          + str(list(data.columns)))
        return errors

    def get_time_elapsed(self) -> int:
        time_st = self.data.index.iloc[0]
        time_ed = self.data.index.iloc[-1]
        naive = time_ed - time_st
        return naive

    # The following methods seem to belong to a kind of a specialsauce 
    # trainingpeaks adapter. I think?

    # def get_trainingpeaks_tss(
    #     self,
    #     graded_speed_column_label,
    #     speed_ftp: float,
    # ) -> float:
    #     time_hours = self.get_time_elapsed('time') / 3600  # tmp HACK
    #     normalized_graded_speed = self.calculate_trainingpeaks_normalized_speed(graded_speed_column_label)

    #     return trainingpeaks.calculate_tss(time_hours, 
    #                                        normalized_graded_speed, 
    #                                        speed_ftp)

    # def get_trainingpeaks_graded_speed(
    #     self,
    #     speed_column_label,
    #     grade_column_label,
    # ) -> pd.Series:
    #     return self.data[speed_column_label]  \
    #         * trainingpeaks.adjustment_factor(self.data[grade_column_label])

    # # def with_trainingpeaks_graded_speed(
    # #     self,
    # #     speed_column_label,
    # #     grade_column_label,
    # # ) -> Type['Timeseries']:
    # #     new_data = self.data.copy()
    # #     new_data['graded_speed'] = new_data[speed_column_label]  \
    # #         * trainingpeaks.adjustment_factor(new_data[grade_column_label])
    # #     return Timeseries(new_data)

    # def get_trainingpeaks_intensity_factor(
    #     self,
    #     column_label,
    #     speed_ftp: float,
    # ) -> float:
    #     speed_normalized = self.get_trainingpeaks_normalized_speed(column_label)
    #     return speed_normalized / speed_ftp
    
    # def get_trainingpeaks_normalized_speed(
    #     self,
    #     column_label
    # ) -> float:
    #     return trainingpeaks.lactate_norm(self.data[column_label])
    


# Domain model I think? Entity? uhhhh
# currently anemic if so.
class ActivityData(AggregateRoot):
    def __init__(
        self,
        id: object,
        type: Optional[str] = None,
        timeseries: Optional[Timeseries] = None,
        # summary: Optional[Dict] = None,
        # 'external_id': object,
        # {name, title}: str,
        # 'sport': str,
        # 'timestamp__start': datetime.datetime,
        # 'distance__total': float,
        # 'time__moving': int,
        # 'time__elapsed': int,
        # 'elevation__gain': float,
        # 'external_upload_id': {int? object?}
    ):
        self.id = id
        self.type = type
        self.timeseries = timeseries
        
        # self.summary = summary

        # Invariant idea: timeseries cannot have a duplicate index,
        # because that represents time.

    def get_timeseries(self, scitype='series') -> pd.DataFrame:
        if self.timeseries is None:
            # Could raise a warning idk
            return
        # df = self.timeseries.data.copy()
        # if scitype.lower() == 'panel':
        #     df['activity_id'] = self.id
        #     # return df.set_index('id', append=True)
        # df['activity_type'] = self.type
        # return df
        return self.timeseries.data.copy()


    # def get_trainingpeaks_tss(
    #     self,
    # ) -> float:
    #     if self.timeseries is None:
    #         return
    #     if 'graded_speed' not in self.timeseries.columns:
    #         return
    #         # self.timeseries = self.timeseries.with_trainingpeaks_graded_speed('speed', 'grade_smooth')
    #     return self.timeseries.get_trainingpeaks_tss('graded_speed', 4.4)
    #     # return 100.0 * time_hours * intensity_factor ** 2 


