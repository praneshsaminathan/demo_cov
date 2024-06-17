from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Covid19Data)
admin.site.register(TimeSeriesData)
admin.site.register(FileUpload)