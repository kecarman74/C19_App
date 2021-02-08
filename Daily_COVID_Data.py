import pandas as pd
import numpy as np
import requests
import csv
import pathlib
import datetime
from datetime import date
import lxml.html as lh
from bs4 import BeautifulSoup
import urllib.request


class GetCovidData:

    def __init__(self):
        self.covid_url = "https://api.covidtracking.com/v1/states/daily.csv"
        self.covid_file_name = "daily_covid_data.csv"
        self.covid_df = None
        self.variant_url = "https://www.cdc.gov/mmwr/volumes/70/wr/mm7003e2.htm"
        self.variant_file_name = "daily_variant_data.csv"
        self.variant_df = None
        self.download_covid_data()
        self.download_variant_data()

    def was_file_modified_today(self, filename=None):
        file_name = pathlib.Path(filename)
        file_modification_time = datetime.datetime.fromtimestamp(file_name.stat().st_mtime)
        now = date.today()

        # if the file is more than a day old, return false
        if now > file_modification_time.date():
            return False
        else:
            return True

    # fetch the updated covid data for every state
    # the data is a large csv, so only refresh it once a day
    def download_covid_data(self):

        # if the file is more than a day old, refresh the file
        if not self.was_file_modified_today(self.covid_file_name):
            # download the csv from COVID project
            self.covid_df = pd.read_csv(self.covid_url)

            # create date columns
            self.covid_df['year'] = self.covid_df['date'][:5]
            self.covid_df['month'] = self.covid_df['date'][4:7]
            self.covid_df['day'] = self.covid_df['date'][7:]

            # output to csv for storage
            self.covid_df.to_csv(self.covid_file_name)

        # otherwise load the csv already downloaded
        else:
            self.covid_df = pd.read_csv(self.covid_file_name)

    # reads the current variant update from the CDC website
    # writes results to csv and stores for date
    def download_variant_data(self):

        # if the file is more than a day old, refresh the file
        if not self.was_file_modified_today(self.variant_file_name):
            # scrape data from cdc website and load into df
            df_list = pd.read_html(self.variant_url)
            df = df_list[0]

            #rename columns
            col_names = ["Variant designation",
                         "Location",
                         "Date",
                         "Characteristic mutations",
                         "United States",
                         "Worldwide",
                         "No. of countries with sequences"]
            df.columns = col_names

            # add todays date to df
            df['date'] = date.today()

            # load previous data and append today's data and write to csv
            df2 = pd.read_csv(self.variant_file_name)
            self.variant_df = df2.append(df)
            self.variant_df.to_csv(self.variant_file_name, index=False)

        #otherwise just load the data
        else:
            self.variant_df = pd.read_csv(self.variant_file_name)
