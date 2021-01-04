from django.shortcuts import render, redirect
from user.decorators import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .utils import *


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def post_job(request):
    task = "Add"
    form = PostJobForm()

    if request.method == 'POST':
        form = PostJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            form.save()
            send_mail_to_applicants(job)
            return redirect('company-profile', request.user.id)
        else:
            return redirect('post-job')

    context = {
        'task': task,
        'form': form
    }
    return render(request, 'job/post-job.html', context)


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def edit_job(request, pk):
    task = "Edit"
    job = JobModel.objects.get(id=pk)
    form = PostJobForm(instance=job)
    if request.method == 'POST':
        form = PostJobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            send_mail_to_applicants(job)
            return redirect('job-profile', job.id)
        else:
            return redirect('edit-job', request.JobModel.id)

    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'job/post-job.html', context)


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def delete_job(request, pk):
    job = JobModel.objects.get(id=pk)

    feedback_form = JobFilledForm()

    if request.method == 'POST':
        filled = request.POST['jobFilled']
        feedback_form = JobFilledForm(request.POST)
        if feedback_form.is_valid():
            feedback_form = feedback_form.save(commit=False)
            if filled == "Yes":
                feedback_form.company = request.user.email
                feedback_form.job = job.job_title
                feedback = request.POST['feedback']
                feedback_form.feedback = feedback
                send_mail_delete_job(request.user, job, feedback)
                feedback_form.save()
                job.delete()
                return redirect('company-profile', request.user.id)
            else:
                feedback = request.POST['feedback']
                send_mail_delete_job(request.user, feedback)
                job.delete()
                return redirect('company-profile', request.user.id)
        else:
            return redirect('company-profile', request.user.id)

    context = {
        'item': job,
    }
    return render(request, 'job/delete-job.html', context)


@login_required(login_url='login')
def job_profile(request, pk):
    job = JobModel.objects.get(id=pk)
    location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

    if job.location is not None:
        locations = job.location.split(' ')
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

    try:
        applicant_applied = AppliedJobModel.objects.get(applicant=request.user, job=job)
    except:
        applicant_applied = None

    if request.GET.get('deactivateJob'):
        job.is_active = False
        job.save()
        return redirect('job-profile', job.id)

    if request.GET.get('activateJob'):
        job.is_active = True
        job.save()
        return redirect('job-profile', job.id)

    application_form = ApplicationForm()
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.job = job
            application.applicant = request.user
            if applicant_applied is None:
                percentage = match_percentage(request.user, job)
                application.percentage = percentage
                application.save()

                return redirect('job-profile', job.id)
            else:
                applicant_applied = AppliedJobModel.objects.get(applicant=request.user, job=job)
                applicant_applied.delete()
                return redirect('job-profile', job.id)
        else:
            return redirect('job-profile', job.id)

    context = {
        'job': job,
        'location_link': location_link,
        'application_form': application_form,
        'applicant_applied': applicant_applied,
    }
    return render(request, 'job/job-profile.html', context)


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def applicant_list(request, pk):
    job = JobModel.objects.get(id=pk)
    applications = AppliedJobModel.objects.filter(job=job)

    context = {
        'job': job,
        'applications': applications
    }
    return render(request, 'job/applicant-list.html', context)
