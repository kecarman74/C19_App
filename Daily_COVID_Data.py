import pandas as pd
import pathlib
import datetime
from datetime import date
from datetime import datetime


class GetCovidData:

    def __init__(self):
        self.covid_url = "https://api.covidtracking.com/v1/states/daily.csv"
        self.covid_file_name = "daily_covid_data.csv"
        self.covid_df = None
        self.today = datetime.today().strftime('%m%d%Y')
        self.variant_url = "https://www.cdc.gov/coronavirus/2019-ncov/downloads/transmission/" + self.today + "_Web-UpdateCSV-TABLE.csv"
        self.variant_file_name = "daily_variant_data.csv"
        self.variant_df = None
        try:
            self.download_covid_data()
        except:
            print("error downloading COVID data ")
        try:
            self.download_variant_data()
        except:
            print("")
        self.data_analysis()
        # output to csv for storage
        self.covid_df.to_csv(self.covid_file_name, index=False)
        self.variant_df.to_csv(self.variant_file_name, index=False)

    def was_file_modified_today(self, filename=None):

        try:
            file_name = pathlib.Path(filename)
            file_modification_time = datetime.datetime.fromtimestamp(file_name.stat().st_mtime)
            now = date.today()
            # if the file is more than a day old, return false
            if now > file_modification_time.date():
                return False
            else:
                return True
        except:
            return False

    # fetch the updated covid data for every state
    # the data is a large csv, so only refresh it once a day
    def download_covid_data(self):

        # if the file is more than a day old, refresh the file
        if not self.was_file_modified_today(self.covid_file_name):
            # download the csv from COVID project
            self.covid_df = pd.read_csv(self.covid_url)

            # create date column
            self.covid_df['date_obj'] = pd.to_datetime(self.covid_df['date'], format='%Y%m%d')

        # otherwise load the csv already downloaded
        else:
            self.covid_df = pd.read_csv(self.covid_file_name)

    # reads the current variant update from the CDC website
    # writes results to csv and stores for date
    def download_variant_data(self):

        # if the file is more than a day old, refresh the file
        if not self.was_file_modified_today(self.variant_file_name):
            # download the csv from CDC
            self.variant_df = pd.read_csv(self.variant_file_name)
            df = pd.read_csv(self.variant_url)

            # create date column
            df['date'] = pd.Timestamp("today").strftime("%m/%d/%Y")

            # append together
            self.variant_df.append(df)

        # otherwise load the csv already downloaded
        else:
            self.variant_df = pd.read_csv(self.variant_file_name)

    def data_analysis(self):
        df = pd.read_csv("population.csv")
        if 'population_x' in self.covid_df:
            self.covid_df.drop('population_x', axis=1, inplace=True)
        if 'population' in self.covid_df:
            self.covid_df.drop('population', axis=1, inplace=True)
        self.covid_df = self.covid_df.merge(df, on='state')
        self.covid_df['pos_per_capita'] = self.covid_df['positive'] / self.covid_df['population']
        self.covid_df['cases_per_100k'] = self.covid_df['positive'] / self.covid_df['population'] * 100000
        self.covid_df['daily_pos_rate'] = self.covid_df['positiveIncrease'] / self.covid_df['totalTestResultsIncrease'] * 100
        self.covid_df['total_pos_rate'] = self.covid_df['positive'] / self.covid_df['totalTestResults'] * 100


if __name__ == '__main__':
    new_data = GetCovidData()

