import django_filters
from django_filters import CharFilter
from job.models import JobModel
from .models import PreferredJobModel


class JobFilter(django_filters.FilterSet):
    job_title = CharFilter(field_name='job_title', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = JobModel
        fields = ('job_title', 'location', 'job_type')


class EmployeeFilter(django_filters.FilterSet):
    details = CharFilter(field_name='details', lookup_expr='icontains')

    class Meta:
        model = PreferredJobModel
        fields = ('details',)
