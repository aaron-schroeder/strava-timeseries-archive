from typing import List, Optional

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
        if not data.columns.isin(lang.VARIABLES).all():
            errors.append('Unexpected columns found in timeseries DataFrame: '
                          + str(list(data.columns)))
        return errors

    def get_time_elapsed(self) -> int:
        time_st = self.data.index.iloc[0]
        time_ed = self.data.index.iloc[-1]
        naive = time_ed - time_st
        return naive    


class ActivityData(AggregateRoot):
    def __init__(
        self,
        id: object,
        type: Optional[str] = None,
        timeseries: Optional[Timeseries] = None,
    ):
        self.id = id
        self.type = type
        self.timeseries = timeseries

    def get_timeseries(self, scitype='series') -> pd.DataFrame:
        if self.timeseries is None:
            # Could raise a warning idk
            return
        
        return self.timeseries.data.copy()
