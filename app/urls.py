from django.urls import path, include
from .views import home_page, upload_page, process_file, chart_page, covid19_data_api, covid19_country_data_api, get_comments
from rest_framework.routers import DefaultRouter
from .views import Covid19DataViewSet, TimeSeriesDataViewSet, FileUploadViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'covid19data', Covid19DataViewSet)
router.register(r'timeseriesdata', TimeSeriesDataViewSet)
router.register(r'fileupload', FileUploadViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', home_page, name='home-page'),
    path('charts/', chart_page, name='chart-page'),
    path('upload/', upload_page, name='upload-page'),
    path('process-file/<int:pk>/', process_file, name='process-file'),
    path('api/', include(router.urls)),
    path('api/comments/', get_comments, name='api-comments'),
    path('api/covid19-data/', covid19_data_api, name='covid19-data-api'),
    path('api/covid19-country-data/', covid19_country_data_api, name='covid19-country-data-api'),
]
