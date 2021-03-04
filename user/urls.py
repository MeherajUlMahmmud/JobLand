from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),

    # user login and logout url
    path('account/login', login_page, name='login'),
    path('account/logout', logout_user, name='logout'),

    # applicant and company registration url
    path('account/applicant-registration', applicant_register, name='applicant-register'),
    path('account/company-registration', company_register, name='company-register'),

    # applicant feed url
    path('applicant/applicant-feed', applicant_feed, name='applicant-feed'),
    path('applicant/search-result', search_result, name='search-result'),

    # applicant profile, public profile and company profile url
    path('applicant/applicant-profile/<str:pk>/', applicant_profile, name='applicant-profile'),
    path('applicant/applicant-public-profile/<str:pk>', applicant_public_profile, name='applicant-public-profile'),
    path('company/company-profile/<str:pk>/', company_profile, name='company-profile'),

    # applicant and company profile edit url
    # path('create-resume', create_resume, name='create-resume'),
    path('pdf', pdf_view, name='pdf-view'),
    path('applicant/applicant-edit-profile', applicant_edit_profile, name='applicant-edit-profile'),
    path('applicant/applicant-add-social', applicant_add_social, name='applicant-add-social'),
    path('applicant/applicant-add-phone', applicant_add_phone, name='applicant-add-phone'),
    path('applicant/applicant-add-resume', applicant_add_resume, name='applicant-add-resume'),
    path('company/company-edit-profile', company_edit_profile, name='company-edit-profile'),

    # add, edit, and delete work experience url
    path('applicant/applicant-profile/add-experience', add_experience, name='add-experience'),
    path('applicant/applicant-profile/edit-experience/<str:pk>', edit_experience, name='edit-experience'),
    path('applicant/applicant-profile/delete-experience/<str:pk>', delete_experience, name='delete-experience'),

    # add, edit, and delete education url
    path('applicant/applicant-profile/add-education', add_education, name='add-education'),
    path('applicant/applicant-profile/edit-education/<str:pk>', edit_education, name='edit-education'),
    path('applicant/applicant-profile/delete-education/<str:pk>', delete_education, name='delete-education'),

    # add, edit, and delete skill url
    path('applicant/applicant-profile/add-skill', add_skill, name='add-skill'),
    path('applicant/applicant-profile/edit-skill/<str:pk>/', edit_skill, name='edit-skill'),
    path('applicant/applicant-profile/delete-skill/<str:pk>/', delete_skill, name='delete-skill'),

    # add, edit, and delete language url
    path('applicant/applicant-profile/add-language', add_language, name='add-language'),
    path('applicant/applicant-profile/edit-language/<str:pk>/', edit_language, name='edit-language'),
    path('applicant/applicant-profile/delete-language/<str:pk>/', delete_language, name='delete-language'),

    # add, edit, and delete reference url
    path('applicant/applicant-profile/add-reference', add_reference, name='add-reference'),
    path('applicant/applicant-profile/edit-reference/<str:pk>', edit_reference, name='edit-reference'),
    path('applicant/applicant-profile/delete-reference/<str:pk>', delete_reference, name='delete-reference'),

    # add, edit, and delete award url
    path('applicant/applicant-profile/add-award', add_award, name='add-award'),
    path('applicant/applicant-profile/edit-award/<str:pk>', edit_award, name='edit-award'),
    path('applicant/applicant-profile/delete-award/<str:pk>', delete_award, name='delete-award'),

    # add, edit, and delete preferred job url
    path('applicant/applicant-profile/add-preferred-job', add_preferred_job, name='add-preferred-job'),
    path('applicant/applicant-profile/edit-preferred-job/<str:pk>', edit_preferred_job, name='edit-preferred-job'),
    path('applicant/applicant-profile/delete-preferred-jobs/<str:pk>', delete_preferred_jobs,
         name='delete-preferred-jobs'),

    # utilities
    path('confirm-email-password', authentication_view, name='authentication'),
    path('account-settings/<str:pk>/', account_settings, name='account-settings'),
    path('deactivation-successful/', deactivation_successful_view, name='deactivation-successful'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),

    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name="user/password-reset.html"),
         name="reset-password"),
    path('reset-password-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="user/password-reset-sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password-reset-form.html"),
         name="password_reset_confirm"),

    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="user/password-reset-done.html"),
         name="password_reset_complete"),
]
