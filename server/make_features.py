import pandas as pd
import datetime as dt
import sklearn
from sklearn.linear_model import LinearRegression
# 

class DFFeatures:
    def __init__(self, df):
        # build base datasets
        self.base_time_data = self.set_up_time_data(df)
        self.base_day_data = self.sum_by_day(self.base_time_data)
        self.base_week_data = self.sum_data_byWeek(self.base_day_data)
        self.day_with_week_data = self.merge_week_and_day_data(
            self.base_week_data, self.base_day_data)

        # separate out weekend and week data
        weekday_DF = self.day_with_week_data[
            self.day_with_week_data['wknd_or_hldy'] == False]
        weekend_DF = self.day_with_week_data[
            self.day_with_week_data['wknd_or_hldy'] == True]
        
        # include predictions
        self.weekday_DF = self.findDayPredictionsBasedOnTemp(
            weekday_DF)
        self.weekend_DF= self.findDayPredictionsBasedOnTemp(
            weekend_DF)

    def set_up_time_data(self, df):
        df['datetime'] = pd.to_datetime(df['time'])
        del df["time"]
        df['just_date'] = pd.to_datetime(df['datetime'].dt.date)
        df['just_time'] = df['datetime'].dt.time
        return df

    def sum_by_day(self, df):
        dfByDate = df.groupby(['just_date'], as_index=False).agg(
            {'electricity_usage': ['sum'], 'out_door_temp': ['mean']})
        # format data
        dfByDate.reset_index()
        dfByDate.columns = dfByDate.columns.droplevel(1)
        dfByDate['electricity_usage_sum_byDate'] = dfByDate['electricity_usage']
        del dfByDate['electricity_usage']
        dfByDate['out_door_temp_mean_byDate'] = dfByDate['out_door_temp']
        del dfByDate['out_door_temp']

        dfByDate = self.build_in_day_features(dfByDate)

        return dfByDate

    def build_in_day_features(self, df):
        df['day_num'] = df['just_date'].dt.weekday
        df['week_num'] = df['just_date'].dt.strftime("%V")
        df['year'] = df['just_date'].dt.strftime("%Y")
        df['yr_and_week_num'] = df['year'].map(
            str) + '-' + df['week_num'].map(str)
        return df

    def sum_data_byWeek(self, df):
        weekDF = df.groupby('yr_and_week_num', as_index=False).agg({'electricity_usage_sum_byDate': [
            'sum', 'mean', 'std'], 'out_door_temp_mean_byDate': ['mean']})
        # format subheaders
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

        week_df_withDateRef = self.integrate_week_dateRef(
            weekDF, self.base_day_data)
        sorted_week_df_withDateRef = week_df_withDateRef.sort_values(
            by=['monday_of_that_week'])
        return sorted_week_df_withDateRef

    def integrate_week_dateRef(self, week_data, day_data):
        day_data_byMondays = day_data[day_data['day_num'] == 0]
        day_data_byMondays_filtered = day_data_byMondays.filter(
            ['just_date', 'yr_and_week_num'])
        merged_week_df_withDateRef = pd.merge(day_data_byMondays_filtered, week_data,
                                              on='yr_and_week_num', how='inner')

        merged_week_df_withDateRef['monday_of_that_week'] = merged_week_df_withDateRef['just_date']
        del merged_week_df_withDateRef['just_date']
        return merged_week_df_withDateRef

    def merge_week_and_day_data(self, DF_byWeek, DF_byDay,):
        DF_byDay_with_weekdata = pd.merge(
            DF_byDay, DF_byWeek, on='yr_and_week_num')

        def if_wknd(df):
            if df.day_num > 4:
                return True
            else:
                return False

        DF_byDay_with_weekdata['wknd'] = DF_byDay_with_weekdata.apply(
            if_wknd, axis=1)

        weekend_DF_byTime = DF_byDay_with_weekdata[DF_byDay_with_weekdata['wknd'] == True]

        def if_wknd_or_holiday(df):
            local_wknd_df = weekend_DF_byTime[weekend_DF_byTime['yr_and_week_num']
                                              == df['yr_and_week_num']]
            localwkndmean = local_wknd_df['electricity_usage_sum_byDate'].mean(
            )
            if df['wknd']:
                return True
            if float(df.electricity_usage_sum_byDate) < localwkndmean + float(df.electricity_usage_std_byWeek) * 1:
                return True
            else:
                return False

        DF_byDay_with_weekdata['wknd_or_hldy'] = DF_byDay_with_weekdata.apply(
        if_wknd_or_holiday, axis=1)

        return DF_byDay_with_weekdata
    
    def findDayPredictionsBasedOnTemp(self, day_DF_byDay):
        # specify data to model
        day_data_with_expected_usage_noNA = day_DF_byDay.dropna()
        X_day_data_with_expected_usage_filtered = day_data_with_expected_usage_noNA.filter(
            ['out_door_temp_mean_byDate'])
        y_day_data_with_expected_usage_filtered = day_data_with_expected_usage_noNA.filter(
            ['electricity_usage_sum_byDate'])
        # convert to numpy arrays
        y = y_day_data_with_expected_usage_filtered.values
        X = X_day_data_with_expected_usage_filtered.values
        

        linreg = LinearRegression()

        # # consider the testing score
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
              X, y, test_size=0.3, random_state=42)
        linreg.fit(X_train, y_train)
        y_pred = linreg.predict(X_test)
        print(linreg.score(X_test, y_test))

        day_data_with_expected_usage_noNA['predictions'] = linreg.predict(X)
        
        weekday_DF_byDay_withPreds = day_data_with_expected_usage_noNA.sort_values(
            by=['just_date'])
        # integrate diff with predictions 
        weekday_DF_byDay_withPreds["pred_diff"] = weekday_DF_byDay_withPreds['predictions'] - \
            weekday_DF_byDay_withPreds['electricity_usage_sum_byDate']

        return weekday_DF_byDay_withPreds

    
    
