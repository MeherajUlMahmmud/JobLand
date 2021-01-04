from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'last_login', 'is_admin', 'is_applicant', 'is_company')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('email',)
    # list_filter = ()
    fieldsets = ()
    list_filter = ('is_admin', 'is_active', 'is_applicant', 'is_company')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password', 'date_joined', 'last_login', )}),
    #     ('Info', {'fields': ('name',)}),
    #     ('Permissions', {'fields': ('is_admin', 'is_applicant' 'is_company')}),
    # )


class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('gender',)


class CompanyProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'website',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class WorkExperienceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company', 'location',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('job_title',)


class EducationModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'degree', 'department', 'cgpa',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class SkillSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_title', 'proficiency')
    search_fields = ('user', 'skill_title',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('skill_title',)


class ReferenceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'designation')
    search_fields = ('user', 'name',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'proficiency',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('language',)


class AwardModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'detail',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class PreferredJobModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'details',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('details',)


class RatingModelAdmin(admin.ModelAdmin):
    list_display = ('company', 'applicant', 'rate',)
    search_fields = ('company', 'applicant', 'rate',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ('company', 'applicant', 'rate',)


class ProfileViewAdmin(admin.ModelAdmin):
    list_display = ('viewedBy', 'viewed', 'timestamp')
    search_fields = ('viewedBy', 'viewed', 'timestamp')
    readonly_fields = ('timestamp',)

    filter_horizontal = ()
    ordering = ('timestamp',)
    fieldsets = ()
    list_filter = ('timestamp',)


class EmployeeSearchAdmin(admin.ModelAdmin):
    list_display = ('searched_by', 'searched_for', 'timestamp')
    search_fields = ('searched_by', 'searched_for', 'timestamp')
    readonly_fields = ('timestamp',)

    filter_horizontal = ()
    ordering = ('timestamp',)
    fieldsets = ()
    list_filter = ('timestamp',)


class JobSearchAdmin(admin.ModelAdmin):
    list_display = ('searched_by', 'searched_for', 'timestamp')
    search_fields = ('searched_by', 'searched_for', 'timestamp')
    readonly_fields = ('timestamp',)

    filter_horizontal = ()
    ordering = ('timestamp',)
    fieldsets = ()
    list_filter = ('timestamp',)


admin.site.register(User, AccountAdmin)
admin.site.register(ApplicantProfileModel, ApplicantProfileAdmin)
admin.site.register(CompanyProfileModel, CompanyProfileModelAdmin)
admin.site.register(WorkExperienceModel, WorkExperienceModelAdmin)
admin.site.register(EducationModel, EducationModelAdmin)
admin.site.register(SkillSetModel, SkillSetAdmin)
admin.site.register(ReferenceModel, ReferenceModelAdmin)
admin.site.register(LanguageModel, LanguageModelAdmin)
admin.site.register(AwardModel, AwardModelAdmin)
admin.site.register(PreferredJobModel, PreferredJobModelAdmin)
admin.site.register(RatingModel, RatingModelAdmin)
admin.site.register(ProfileViewDetails, ProfileViewAdmin)
admin.site.register(EmployeeSearchKeywordModel, EmployeeSearchAdmin)
admin.site.register(JobSearchKeywordModel, JobSearchAdmin)
