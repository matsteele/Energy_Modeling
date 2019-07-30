import make_features 
import datetime as dt
import pandas as pd


df = pd.read_csv('PD_challange_data_set.csv')


DF = make_features.DFFeatures(df)


class TestClass(object):
    def test_that_weekends_are_separated(self):
        x = "hello"
        assert 'h' in x

    def test_that_all_entries_are_considered_after_split(self):
        assert len(DF.base_day_data) == len(DF.weekday_DF) + len(DF.weekend_DF)

    def test_that_jan1st_is_holiday(self):
        df = DataFeatures.weekend_DF
        jan1_pull_out = df[df.just_date ==
                           dt.datetime.strptime('2018-01-01', "%Y-%m-%d")]
        assert len(jan1_pull_out) == 1

    def inc(self, x):
        return x + 1

    def test_answer(self):
        assert self.inc(3) == 4
