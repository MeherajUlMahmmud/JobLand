from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class JobModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'date_posted',)
    search_fields = ('user',)
    readonly_fields = ('date_posted',)

    filter_horizontal = ()
    ordering = ('-date_posted',)
    fieldsets = ()
    list_filter = ('user', 'job_title',)


class AppliedJobModelAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'timestamp',)
    search_fields = ('applicant',)
    readonly_fields = ('timestamp',)

    filter_horizontal = ()
    ordering = ('-timestamp',)
    fieldsets = ()
    list_filter = ('applicant', 'job',)

class FilledJobModelAdmin(admin.ModelAdmin):
    list_display = ('company', 'job', 'feedback',)
    search_fields = ('company',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('company', 'job','feedback',)

admin.site.register(JobModel, JobModelAdmin)
admin.site.register(AppliedJobModel, AppliedJobModelAdmin)
admin.site.register(FilledJobModel, FilledJobModelAdmin)

