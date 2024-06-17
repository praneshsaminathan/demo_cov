from django.test import TestCase
from rest_framework.test import APIClient
from .models import Covid19Data, TimeSeriesData, FileUpload
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class Covid19DataTests(TestCase):
    """
    Test cases for the Covid19Data model and its related API endpoints.
    """
    def setUp(self):
        """
        Set up the test client and initial data for Covid19Data.
        """
        self.client = APIClient()
        Covid19Data.objects.create(
            observation_date='2020-01-22',
            province_state='Hubei',
            country_region='China',
            last_update=datetime.strptime('2020-01-22 17:00:00', '%Y-%m-%d %H:%M:%S'),
            confirmed=548,
            deaths=17,
            recovered=28
        )

    def test_get_covid19data(self):
        """
        Test retrieving Covid19Data entries via the API.
        """
        response = self.client.get('/api/covid19data/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country_region'], 'China')

    def test_create_covid19data(self):
        """
        Test creating a new Covid19Data entry via the API.
        """
        data = {
            "observation_date": "2020-01-23",
            "province_state": "Hubei",
            "country_region": "China",
            "last_update": "2020-01-23T17:00:00",
            "confirmed": 600,
            "deaths": 20,
            "recovered": 30
        }
        response = self.client.post('/api/covid19data/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Covid19Data.objects.count(), 2)

class TimeSeriesDataTests(TestCase):
    """
    Test cases for the TimeSeriesData model and its related API endpoints.
    """
    def setUp(self):
        """
        Set up the test client and initial data for TimeSeriesData.
        """
        self.client = APIClient()
        TimeSeriesData.objects.create(
            date='2020-01-22',
            country_region='China',
            province_state='Hubei',
            confirmed=548,
            deaths=17,
            recovered=28
        )

    def test_get_timeseriesdata(self):
        """
        Test retrieving TimeSeriesData entries via the API.
        """
        response = self.client.get('/api/timeseriesdata/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country_region'], 'China')

    def test_create_timeseriesdata(self):
        """
        Test creating a new TimeSeriesData entry via the API.
        """
        data = {
            "date": "2020-01-23",
            "country_region": "China",
            "province_state": "Hubei",
            "confirmed": 600,
            "deaths": 20,
            "recovered": 30
        }
        response = self.client.post('/api/timeseriesdata/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TimeSeriesData.objects.count(), 2)

class FileUploadTests(TestCase):
    """
    Test cases for the FileUpload model and its related API endpoints.
    """
    def setUp(self):
        """
        Set up the test client for FileUpload.
        """
        self.client = APIClient()

    def test_file_upload(self):
        """
        Test uploading a file via the API.
        """
        with open('path_to_test_file/testfile.csv', 'rb') as file:
            upload_file = SimpleUploadedFile(name='testfile.csv', content=file.read(), content_type='text/csv')
            response = self.client.post('/api/fileupload/', {'title': 'Test File', 'file': upload_file}, format='multipart')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(FileUpload.objects.count(), 1)
            self.assertEqual(FileUpload.objects.first().title, 'Test File')