import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Covid19Data, TimeSeriesData
import pandas as pd
import os

from app.process_excel_file import ProcessExcelFile

class Command(BaseCommand, ProcessExcelFile):
    """
    Django management command to load data from COVID-19 CSV files into the database.
    Inherits from BaseCommand and ProcessExcelFile.
    """
    help = 'Load data from COVID-19 CSV files'  # Description of the command

    def handle(self, *args, **kwargs):
        """
        The entry point for the command. This method is called when the command is executed.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Load COVID-19 data from the specified CSV file into the Covid19Data model
        self.load_covid19_data(os.path.join(settings.BASE_DIR, 'data/covid_19_data.csv'))

        # Load time series data for confirmed cases
        self.load_time_series_data(os.path.join(settings.BASE_DIR, 'data/time_series_covid_19_confirmed.csv'), 'confirmed')

        # Load time series data for deaths
        self.load_time_series_data(os.path.join(settings.BASE_DIR, 'data/time_series_covid_19_deaths.csv'), 'deaths')

        # Load time series data for recovered cases
        self.load_time_series_data(os.path.join(settings.BASE_DIR, 'data/time_series_covid_19_recovered.csv'), 'recovered')