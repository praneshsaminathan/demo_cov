from django.db import models

class Covid19Data(models.Model):
    """
    Model representing individual records of COVID-19 data, capturing details about observation dates,
    regions, and case counts.
    """
    observation_date = models.DateField(help_text="The date on which the data was observed.")
    province_state = models.CharField(max_length=100, null=True, blank=True, help_text="The province or state of the observation, if applicable.")
    country_region = models.CharField(max_length=100, help_text="The country or region of the observation.")
    last_update = models.DateTimeField(help_text="The timestamp of the last update to this data.")
    confirmed = models.IntegerField(help_text="The number of confirmed cases.")
    deaths = models.IntegerField(help_text="The number of deaths.")
    recovered = models.IntegerField(help_text="The number of recoveries.")

    def __str__(self):
        """
        Returns a string representation of the object, which is helpful for admin displays.
        """
        return f"{self.country_region} - {self.observation_date}"

class TimeSeriesData(models.Model):
    """
    Model to store time series data for COVID-19, allowing tracking of cases over time within specific regions.
    """
    date = models.DateField(help_text="The date for this entry of the time series data.")
    country_region = models.CharField(max_length=100, help_text="The country or region for this entry.")
    province_state = models.CharField(max_length=100, null=True, blank=True, help_text="The province or state for this entry, if applicable.")
    confirmed = models.IntegerField(null=True, blank=True, help_text="The number of confirmed cases on this date.")
    deaths = models.IntegerField(null=True, blank=True, help_text="The number of deaths on this date.")
    recovered = models.IntegerField(null=True, blank=True, help_text="The number of recoveries on this date.")

    def __str__(self):
        """
        Returns a string representation of the object, which is helpful for admin displays.
        """
        return f"{self.country_region} - {self.date}"

class FileUpload(models.Model):
    """
    Model to represent the upload of files, specifically for uploading CSV or other data files containing
    COVID-19 data to be processed.
    """
    title = models.CharField(max_length=100, help_text="The title or name of the file.")
    file = models.FileField(upload_to='uploads/', help_text="The path to the uploaded file.")
    status = models.CharField(max_length=50, default='Uploaded', help_text="The current status of the file processing (e.g., Uploaded, Processing, Completed).")

    def __str__(self):
        """
        Returns the title of the file, used in admin displays and logging.
        """
        return self.title

class Comment(models.Model):
    """
    Model for storing comments made by users, potentially about the data or the application.
    """
    user = models.CharField(max_length=100, help_text="The user who made the comment.")
    text = models.TextField(help_text="The content of the comment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the comment was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time the comment was last updated.")

    def __str__(self):
        """
        Returns a string that includes the commenter's name, useful for admin displays.
        """
        return f"Comment by {self.user}"