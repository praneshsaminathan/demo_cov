from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.core.management import call_command
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Covid19Data, TimeSeriesData, FileUpload, Comment
from .serializers import Covid19DataSerializer, TimeSeriesDataSerializer, FileUploadSerializer, CommentSerializer
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Covid19DataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling COVID-19 data entries.
    """
    queryset = Covid19Data.objects.all()
    serializer_class = Covid19DataSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset by date range.
        """
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                observation_date__range=[start_date, end_date]
            )
        return queryset

class TimeSeriesDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling time series data entries.
    """
    queryset = TimeSeriesData.objects.all()
    serializer_class = TimeSeriesDataSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset by date range.
        """
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                date__range=[start_date, end_date]
            )
        return queryset

class FileUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling file uploads.
    """
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer

    @action(detail=True, methods=['post'])
    def process_file(self, request, pk=None):
        """
        Processes the uploaded file by running a management command.
        """
        file_upload = self.get_object()
        file_upload.status = 'Processing'
        file_upload.save()
        call_command('process_uploaded_file', pk)
        return redirect('upload-page')

class CommentPagination(PageNumberPagination):
    """
    Pagination class for comments.
    """
    page_size = 10

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')  # Ensure the queryset is ordered
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    
    def get_queryset(self):
        """
        Retrieves the queryset of comments, optionally filtered by a specific date.
        """
        print(self.request.query_params)
        queryset = Comment.objects.all().order_by('-created_at')
        date_str = self.request.query_params.get('date')
        if date_str:
            date = parse_date(date_str)
            if date:
                queryset = queryset.filter(created_at__date=date)
        return queryset

def covid19_data_api(request):
    """
    API endpoint for global COVID-19 data aggregated by month.
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        data = Covid19Data.objects.filter(
            observation_date__range=[start_date, end_date]
        ).values('observation_date').annotate(
            total_confirmed=Sum('confirmed'),
            total_deaths=Sum('deaths'),
            total_recovered=Sum('recovered')
        )
    else:
        data = Covid19Data.objects.values('observation_date').annotate(
            total_confirmed=Sum('confirmed'),
            total_deaths=Sum('deaths'),
            total_recovered=Sum('recovered')
        )
    
    df = pd.DataFrame(list(data))
    if not df.empty:
        df['observation_date'] = pd.to_datetime(df['observation_date'])
        df['year_month'] = df['observation_date'].dt.to_period('M')

        monthly_data = df.groupby('year_month').agg({
            'total_confirmed': 'sum',
            'total_deaths': 'sum',
            'total_recovered': 'sum'
        }).reset_index()
        monthly_data['year_month'] = monthly_data['year_month'].astype(str)
        response_data = monthly_data.to_dict(orient='records')
    else:
        response_data = []
    return JsonResponse(response_data, safe=False)

def covid19_country_data_api(request):
    """
    API endpoint for country-wise COVID-19 data aggregated by month.
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        data = Covid19Data.objects.filter(
            observation_date__range=[start_date, end_date]
        ).values('country_region', 'observation_date').annotate(
            total_confirmed=Sum('confirmed'),
            total_deaths=Sum('deaths'),
            total_recovered=Sum('recovered')
        )
    else:
        data = Covid19Data.objects.values('country_region', 'observation_date').annotate(
            total_confirmed=Sum('confirmed'),
            total_deaths=Sum('deaths'),
            total_recovered=Sum('recovered')
        )
    
    df = pd.DataFrame(list(data))
    if not df.empty:
        df['observation_date'] = pd.to_datetime(df['observation_date'])
        df['year_month'] = df['observation_date'].dt.to_period('M')

        country_month_data = df.groupby(['country_region', 'year_month']).agg({
            'total_confirmed': 'sum',
            'total_deaths': 'sum',
            'total_recovered': 'sum'
        }).reset_index()
        country_month_data['year_month'] = country_month_data['year_month'].astype(str)
        response_data = country_month_data.to_dict(orient='records')
    else:
        response_data = []
    return JsonResponse(response_data, safe=False)

def chart_page(request):
    """
    Renders the chart page.
    """
    return render(request, 'charts.html')

def home_page(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html')

def upload_page(request):
    """
    Handles file uploads and displays uploaded files.
    """
    if request.method == 'POST':
        file = request.FILES['file']
        title = file.name.split('.')[0]
        file_upload = FileUpload(title=title, file=file)
        file_upload.save()
        
        return redirect('upload-page')
    
    files = FileUpload.objects.all()
    return render(request, 'upload.html', {'files': files})

def process_file(request, pk):
    
    # Retrieve the FileUpload instance or return a 404 if not found
    file_upload = get_object_or_404(FileUpload, pk=pk)
    
    # Update the status to 'Processing'
    file_upload.status = 'Processing'
    file_upload.save()

    try:
        # Call the custom management command to process the uploaded file
        call_command('process_uploaded_file', pk)
    except Exception as e:
        # Update the status to 'Failed' if an error occurs
        file_upload.status = 'Failed'
        file_upload.save()
        logger.error(f"Error processing file {pk}: {e}")
        return redirect('upload-page')

    # Update the status to 'Processed' if the command succeeds
    file_upload.status = 'Processed'
    file_upload.save()
    
    return redirect('upload-page')
    
def get_comments(request):
    date_str = request.GET.get('date')
    if date_str:
        date = parse_date(date_str)
        comments = Comment.objects.filter(created_at__date=date)
    else:
        comments = Comment.objects.all()

    # Serialize and return comments
    # Assuming you have a serializer or a simple JsonResponse setup
    return JsonResponse({'comments': list(comments.values())})