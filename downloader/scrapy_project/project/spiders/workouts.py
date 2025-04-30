import datetime
import glob
import json
import os

import scrapy


class Operation1(scrapy.Spider):
    name = 'operation_1'

    def start_requests(self):
        self._data_dir = os.getenv('TP_JSON_DIR')
        self._local_tp_client = LocalTrainingPeaksApiClient(self._data_dir)
        yield scrapy.http.Request(
            f'{self.settings.get("TP_PROXY_SERVER_URL")}/users/v3/user',
            callback=self.parse_user)

    def parse_user(self, response):
        user_dict = response.json()
        athlete_id = user_dict['user']['userId']

        date_st = datetime.date(1989, 12, 4)
        # date_st = datetime.date.today() - datetime.timedelta(days=30)
        date_ed = datetime.date.today()
        date_fmt = '%Y-%m-%d'
        date_str_st = date_st.strftime(date_fmt)
        date_str_ed = date_ed.strftime(date_fmt)

        yield scrapy.http.Request(
            f'{self.settings.get("TP_PROXY_SERVER_URL")}/fitness/v6/athletes'
            f'/{athlete_id}/workouts/{date_str_st}/{date_str_ed}',
            callback=self.parse_workouts_list, dont_filter=True)
    
    def parse_workouts_list(self, response):
        # ADS HERE
        workouts_list = response.json()
        for workout_dict in workouts_list:
            yield workout_dict


class LocalTrainingPeaksApiClient:
    def __init__(self, directory):
        self.directory = directory

    def get_workout_by_id(self, workout_id: int):
        data_path = os.path.join(self.directory,
                                 'workouts',str(workout_id),'workout.json')
        if not os.path.exists(data_path):
            return
        with open(data_path, 'r') as file:
            data = json.load(file)
        return data

    def get_all_workouts(self):  # -> schema.WorkoutsList
        data_path = os.path.join(self.directory, 'workouts','*','workout.json')
        for f in glob.iglob(data_path):
            with open(f, 'r') as fp:
                yield json.load(fp)

    def get_workout_ids(self):
        data_path = os.path.join(self.directory, 'workouts/')
        return (int(f.name) for f in os.scandir(data_path) if f.is_dir())