import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import FileUpload, Covid19Data, TimeSeriesData
import pandas as pd

class ProcessExcelFile:
    """
    This class provides methods to process Excel files containing COVID-19 data
    and load them into the database.
    """
    def __init__(self):
        """
        Initialize the ProcessExcelFile instance.
        """
        pass

    def load_covid19_data(self, filepath):
        """
        Load COVID-19 data from a CSV file into the database.

        Args:
            filepath (str): The path to the CSV file.
        """
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip the header row
            if header is None:
                raise ValueError("CSV file is empty or incorrectly formatted")
            
            for row in reader:
                if len(row) < 8:  # Ensuring the row has all required data
                    continue  # Skip rows that don't have enough columns
                Covid19Data.objects.create(
                    observation_date=self.parse_date(row[1]),
                    province_state=row[2] if row[2] else None,
                    country_region=row[3],
                    last_update=self.parse_date(row[4]),
                    confirmed=self.parse_int(row[5]),
                    deaths=self.parse_int(row[6]),
                    recovered=self.parse_int(row[7])
                )
        print('COVID-19 data loaded successfully')

    def load_time_series_data(self, filepath, data_type):
        """
        Load time series data related to COVID-19 from a CSV file.

        Args:
            filepath (str): The path to the CSV file.
            data_type (str): The type of data (e.g., 'confirmed', 'deaths', 'recovered').
        """
        df = pd.read_csv(filepath)
        df_melted = df.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"],
                            var_name="Date", value_name=data_type.capitalize())
        df_melted['Date'] = pd.to_datetime(df_melted['Date'])
        
        for _, row in df_melted.iterrows():
            obj, created = TimeSeriesData.objects.get_or_create(
                date=row['Date'],
                country_region=row['Country/Region'],
                province_state=row['Province/State']
            )
            setattr(obj, data_type, self.parse_int(row[data_type.capitalize()]))
            obj.save()
        print(f'{data_type.capitalize()} data loaded successfully')

    def parse_date(self, date_str):
        """
        Parse a date string into a datetime object.

        Args:
            date_str (str): The date string to be parsed.

        Returns:
            datetime: The parsed date.

        Raises:
            ValueError: If no valid date format is found.
        """
        for fmt in ('%m/%d/%Y %H:%M', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%m/%d/%y %H:%M', '%Y-%m-%dT%H:%M:%S'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f'No valid date format found for {date_str}')

    def parse_int(self, value):
        """
        Safely parse a string to an integer, defaulting to 0 on failure.

        Args:
            value (str): The string to parse.

        Returns:
            int: The parsed integer, or 0 if conversion fails.
        """
        try:
            return int(float(value))
        except ValueError:
            return 0  # Fallback to 0 if parsing fails

class Command(BaseCommand, ProcessExcelFile):
    """
    Django management command to load data from COVID-19 CSV files into the database.
    """
    help = 'Load data from COVID-19 CSV files into the database'

    def add_arguments(self, parser):
        """
        Add command-line arguments to the command.

        Args:
            parser (ArgumentParser): The parser for command-line arguments.
        """
        parser.add_argument('file_id', type=int, help='ID of the FileUpload instance')

    def handle(self, *args, **kwargs):
        """
        Handle the command input.

        Args:
            *args: Variable arguments.
            **kwargs: Keyword arguments.
        """
        file_id = kwargs['file_id']
        file_upload = FileUpload.objects.filter(id=file_id).first()

        if not file_upload:
            self.stdout.write(self.style.ERROR('FileUpload instance does not exist'))
            return

        file_path = os.path.join(settings.MEDIA_ROOT, file_upload.file.name)

        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            self.stdout.write(self.style.ERROR(f'File {file_path} is empty or does not exist'))
            return
        try:
            # Determine which type of data to load based on the file title
            if 'covid_19_data' in file_upload.title.lower():
                self.load_covid19_data(file_path)
            elif 'time_series_covid_19_confirmed' in file_upload.title.lower():
                self.load_time_series_data(file_path, 'confirmed')
            elif 'time_series_covid_19_deaths' in file_upload.title.lower():
                self.load_time_series_data(file_path, 'deaths')
            elif 'time_series_covid_19_recovered' in file_upload.title.lower():
                self.load_time_series_data(file_path, 'recovered')

            self.stdout.write(self.style.SUCCESS('File processed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {e}'))