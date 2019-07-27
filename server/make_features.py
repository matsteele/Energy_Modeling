import pandas as pd
import datetime as dt


class DFFeatures:
    def __init__(self, df):
        self.base_time_data = self.set_up_time_data(df)
        self.base_day_data = self.sum_by_day(self.base_time_data)
        self.base_week_data = self.sum_data_byWeek(self.base_day_data)
        self.weekdata_with_day_data = self.merge_week_and_day_data(
            self.base_day_data, self.base_week_data)
        self.weekday_DF_byTime = self.weekdata_with_day_data[
            self.weekdata_with_day_data['wknd_or_hldy'] == False]
        self.weekend_DF_byTime = self.weekdata_with_day_data[
            self.weekdata_with_day_data['wknd_or_hldy'] == True]

    def set_up_time_data(self, df):
        df['datetime'] = pd.to_datetime(df['time'])
        del df["time"]
        df['just_date'] = df['datetime'].dt.date
        df['just_time'] = df['datetime'].dt.time
        return df

    def sum_by_day(self, df):
        dfByDate = df.groupby(['just_date'], as_index=False).agg(
            {'electricity_usage': ['sum'], 'out_door_temp': ['mean']})
        #format data 
        dfByDate.reset_index()
        dfByDate.columns = dfByDate.columns.droplevel(1)
        dfByDate['electricity_usage_sum_byDate'] = dfByDate['electricity_usage']
        del dfByDate['electricity_usage']
        dfByDate['out_door_temp_mean_byDate'] = dfByDate['out_door_temp']
        del dfByDate['out_door_temp']

        dfByDate = self.build_in_day_features(dfByDate)

        return dfByDate

    def build_in_day_features(self, df):
        df['just_date'] = pd.to_datetime(df['just_date'])
        df['day_num'] = df['just_date'].dt.weekday
        df['week_num'] = df['just_date'].dt.strftime("%V")
        df['year'] = df['just_date'].dt.strftime("%Y")
        df['yr_and_week_num'] = df['year'].map(
            str) + '-' + df['week_num'].map(str)
        return df

    def sum_data_byWeek(self, df):
        weekDF = df.groupby('yr_and_week_num', as_index=False).agg({'electricity_usage_sum_byDate': [
            'sum', 'mean', 'std'], 'out_door_temp_mean_byDate': ['mean']})
        #format subheaders
        weekDF['electricity_usage_sum_byWeek'] = weekDF[(
            'electricity_usage_sum_byDate', 'sum')]
        weekDF['electricity_usage_mean_byWeek'] = weekDF[(
            'electricity_usage_sum_byDate', 'mean')]
        weekDF['electricity_usage_std_byWeek'] = weekDF[(
            'electricity_usage_sum_byDate', 'std')]
        weekDF['out_door_temp_mean_byWeek'] = weekDF[(
            'out_door_temp_mean_byDate', 'mean')]

        del weekDF["electricity_usage_sum_byDate"]
        del weekDF["out_door_temp_mean_byDate"]

        weekDF.reset_index()
        weekDF.columns = weekDF.columns.droplevel(1)

        return weekDF


    def merge_week_and_day_data(self, DF_byDay, DF_byWeek):
        DF_byDay_with_weekdata = pd.merge(
            DF_byDay, DF_byWeek, on='yr_and_week_num')
        DF_byDay_with_weekdata.head()

        def _ifHolidayorWeekend(df):
            if df.day_num > 4 or float(df.electricity_usage_sum_byDate) < float(df.electricity_usage_mean_byWeek) - float(df.electricity_usage_std_byWeek) * .50:
                return True
            else:
                return False

        DF_byDay_with_weekdata['wknd_or_hldy'] = DF_byDay_with_weekdata.apply(
            _ifHolidayorWeekend, axis=1)

        return DF_byDay_with_weekdata




