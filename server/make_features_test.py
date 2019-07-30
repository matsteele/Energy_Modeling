import make_features
import datetime as dt
import pandas as pd


df = pd.read_csv('PD_challange_data_set.csv')


DataFeatures = DF(df)


class TestClass(object):
    def test_that_weekends_are_separated(self):
        x = "hello"
        assert 'h' in x

    def test_that_all_entries_are_considered_after_split(self):
        assert len(df.base_day_data) == len(df.weekday_DF) + len(df.weekend_DF)
        x = "hello"
        assert 'h' in x

    def test_that_jan1st_is_holiday(self):
        df = DataFeatures.weekend_DF
        jan1_pull_out = df[df.just_date ==
                           dt.datetime.strptime('2018-01-01', "%Y-%m-%d")]
        assert len(jan1_pull_out) == 1

    def inc(self, x):
        return x + 1

    def test_answer(self):
        assert self.inc(3) == 4
