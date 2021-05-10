from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import strip_tags
from job.models import *
from .decorators import *
from .filters import *
from .forms import *
from .utils import *


@unauthenticated_user
def home(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)
    jobs = JobModel.objects.all()
    filled_job = FilledJobModel.objects.all()
    
    context = {
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
        'jobs': jobs,
        'jobs_len': jobs.count(),
        'filled_job_len':filled_job.count(),
    }
    return render(request, 'user/index.html', context)


@unauthenticated_user
def login_page(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_applicant:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('applicant-feed')
            elif user and user.is_company:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('company-profile', user.id)
            else:
                messages.error(request, 'Username or Password is incorrect.')
                return redirect('login')
        else:
            return render(request, 'user/login.html', {'form': form})
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def applicant_register(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            ApplicantProfileModel.objects.create(user=user)
            send_registration_mail(user)
            return redirect('applicant-feed')
        else:
            return render(request, 'user/applicant/applicant-register.html', {"form": form})

    form = ApplicantRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'user/applicant/applicant-register.html', context)


@unauthenticated_user
def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            CompanyProfileModel.objects.create(user=user)
            # send_registration_mail(user)
            return redirect('company-profile', user.id)
        else:
            return render(request, 'user/company/company-register.html', {"form": form})

    form = CompanyRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'user/company/company-register.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_feed(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)

    name = extractFirstName(request.user.name)

    skill_set = SkillSetModel.objects.filter(user=request.user)
    preferred_job_list = PreferredJobModel.objects.filter(user=request.user)

    job_list = JobModel.objects.filter(is_active=True).order_by('-date_posted')

    # function calling for skill matching
    recommended_jobs = match_skill(job_list, skill_set, preferred_job_list)

    job_filter = JobFilter(request.GET, queryset=job_list)
    job_list = job_filter.qs

    job_search = request.GET.get('job_title')
    add_to_job_keyword(request.user, job_search)

    paginator = Paginator(job_list, 5)
    page = request.GET.get('page', 1)

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {
        'name': name,
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
        'jobs': jobs,
        'job_list': job_list,
        'jobs_len': job_list.count(),
        'myFilter': job_filter,
        'recommended_jobs': recommended_jobs,
        'skill_set': skill_set
    }
    return render(request, 'user/applicant/applicant-feed.html', context)


@login_required(login_url='login')
def search_result(request):
    name = extractFirstName(request.user.name)
    job_list = JobModel.objects.filter(is_active=True).order_by('-date_posted')
    job_filter = JobFilter(request.GET, queryset=job_list)
    job_list = job_filter.qs

    job_search = request.GET.get('job_title')
    add_to_job_keyword(request.user, job_search)

    paginator = Paginator(job_list, 5)
    page = request.GET.get('page', 1)

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {
        'name': name,
        'jobs': jobs,
        'job_list': job_list,
        'jobs_len': job_list.count(),
        'myFilter': job_filter,
    }
    return render(request, 'user/search-result.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_profile(request, pk):
    user = User.objects.get(id=pk)
    applicant = ApplicantProfileModel.objects.get(user=user)

    resume_link = ""
    if applicant.resume:
        resume_link = "http://127.0.0.1:8000" + applicant.resume.url

    work_experience = WorkExperienceModel.objects.filter(user=user)
    educations = EducationModel.objects.filter(user=user)
    skill_set = SkillSetModel.objects.filter(user=user)
    languages = LanguageModel.objects.filter(user=user)
    references = ReferenceModel.objects.filter(user=user)
    awards = AwardModel.objects.filter(user=user)
    preferred_jobs = PreferredJobModel.objects.filter(user=user)
    applied_jobs = AppliedJobModel.objects.filter(applicant=user)

    name = extractFirstName(request.user.name)
    age = None
    if user.applicantprofilemodel.birth_date:
        age = calculate_age(user.applicantprofilemodel.birth_date)

    context = {
        'name': name,
        'age': age,
        'user': user,
        'work_experience': work_experience,
        'educations': educations,
        'skill_set': skill_set,
        'languages': languages,
        'references': references,
        'awards': awards,
        'preferred_jobs': preferred_jobs,
        'applied_jobs': applied_jobs,
        'resume_link': resume_link,
    }
    return render(request, 'user/applicant/applicant-profile.html', context)


@login_required(login_url='login')
def applicant_public_profile(request, pk):
    user = User.objects.get(id=pk)
    applicant = ApplicantProfileModel.objects.get(user=user)

    resume_link = ""
    if applicant.resume:
        resume_link = "http://127.0.0.1:8000" + applicant.resume.url

    skill_set = SkillSetModel.objects.filter(user=user)
    languages = LanguageModel.objects.filter(user=user)
    work_experience = WorkExperienceModel.objects.filter(user=user)
    educations = EducationModel.objects.filter(user=user)
    references = ReferenceModel.objects.filter(user=user)
    awards = AwardModel.objects.filter(user=user)
    rates = RatingModel.objects.filter(applicant=user)
    rate = rateAvg(rates, rates.count())
    age = None
    if user.applicantprofilemodel.birth_date:
        age = calculate_age(user.applicantprofilemodel.birth_date)

    if request.user.is_company:
        increaseViewCount(request.user, user)

    rating_form = RatingForm()
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.company = request.user.companyprofilemodel
            rating.rate = request.POST['extra']
            rating.applicant = user
            rating.save()
            return redirect('applicant-public-profile', user.id)

        else:
            return redirect('applicant-public-profile', user.id)

    name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'age': age,
        'user': user,
        'skill_set': skill_set,
        'work_experience': work_experience,
        'educations': educations,
        'languages':languages,
        'references': references,
        'awards': awards,
        'rating_form': rating_form,
        'rates': rates,
        'rate': rate,
        'resume_link': resume_link,
    }
    return render(request, 'user/applicant/applicant-public-profile.html', context)


@login_required(login_url='login')
def company_profile(request, pk):
    # applicants = User.objects.filter(is_applicant=True)
    # companies = User.objects.filter(is_company=True)
    user = User.objects.get(id=pk)

    location_link = None

    if user.companyprofilemodel.location:
        locations = user.companyprofilemodel.location.split(' ')
        location_link = "https://maps.google.com/maps?width=100%25&amp;height=450&amp;hl=en&amp;q="

        for location in locations:
            location_link += location + "%20"

        location_link += "&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"

    job_list = JobModel.objects.filter(user=user)
    job_search = JobFilter(request.GET, queryset=job_list)

    job_list = job_search.qs

    employee_search = request.GET.get('details')

    employee_list = {}
    if employee_search is not None:
        add_to_employee_keyword(request.user, employee_search)
        employee_list = PreferredJobModel.objects.filter(Q(details__icontains=employee_search))

    if request.user.is_applicant:
        increaseViewCount(request.user, user)

    paginator = Paginator(job_list, 5)
    page = request.GET.get('page', 1)
    try:
        job_list = paginator.page(page)
    except PageNotAnInteger:
        job_list = paginator.page(1)
    except EmptyPage:
        job_list = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'location_link': location_link,
        'job_search': job_search,
        'employee_search': employee_search,
        'job_list': job_list,
        'employee_list': employee_list,
    }
    return render(request, 'user/company/company-profile.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_edit_profile(request):
    applicant = request.user.applicantprofilemodel
    form = ApplicantEditProfileForm(instance=applicant)
    if request.method == 'POST':
        form = ApplicantEditProfileForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('applicant-edit-profile')

    name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'form': form,
    }
    return render(request, 'user/applicant/applicant-edit-profile.html', context)


@login_required(login_url='login')
def create_resume(request):
    user = request.user
    applicant = user.applicantprofilemodel
    name = extractFirstName(request.user.name)
    bio = strip_tags(applicant.bio)

    skill_set = SkillSetModel.objects.filter(user=user)
    work_experience = WorkExperienceModel.objects.filter(user=user)
    educations = EducationModel.objects.filter(user=user)
    references = ReferenceModel.objects.filter(user=user)
    awards = AwardModel.objects.filter(user=user)

    if request.method == "POST":
        image_link = "http://127.0.0.1:8000" + applicant.image.url
        context = {
            'name': name,
            'image_link': image_link,
            'applicant': applicant,
            'context': request.POST
        }
        pdf = render_to_pdf('user/resume/pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

    context = {
        'user': user,
        'applicant': applicant,
        'name': name,
        'bio': bio,
        'skill_set': skill_set,
        'work_experience': work_experience,
        'educations': educations,
        'references': references,
        'awards': awards,
    }
    return render(request, "user/resume/create-resume.html", context)


@login_required(login_url='login')
def pdf_view(request):
    user = request.user
    applicant = user.applicantprofilemodel

    bio = strip_tags(applicant.bio)
    interest = strip_tags(applicant.interest)
    work_experience = WorkExperienceModel.objects.filter(user=user)
    educations = EducationModel.objects.filter(user=user)
    skill_set = SkillSetModel.objects.filter(user=user)
    languages = LanguageModel.objects.filter(user=user)
    references = ReferenceModel.objects.filter(user=user)
    awards = AwardModel.objects.filter(user=user)

    if applicant.image:
        image_link = "http://127.0.0.1:8000" + applicant.image.url
    else:
        image_link=None

    context = {
        'user': user,
        'applicant': applicant,
        'image_link': image_link,
        'bio': bio,
        'interest': interest,
        'experiences': work_experience,
        'educations': educations,
        'skills': skill_set,
        'languages': languages,
        'references': references,
        'awards': awards,
    }
    pdf = render_to_pdf('user/resume/pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_add_social(request):
    applicant = request.user.applicantprofilemodel
    form = ApplicantAddSocialForm(instance=applicant)
    if request.method == 'POST':
        form = ApplicantAddSocialForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('applicant-add-social')

    name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'form': form,
    }
    return render(request, 'user/applicant/applicant-add-social.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_add_phone(request):
    applicant = request.user.applicantprofilemodel
    form = ApplicantAddPhoneNumberForm(instance=applicant)
    if request.method == 'POST':
        form = ApplicantAddPhoneNumberForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('applicant-add-phone')

    name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'form': form,
    }
    return render(request, 'user/applicant/applicant-add-phone.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_add_resume(request):
    applicant = request.user.applicantprofilemodel
    form = ApplicantAddResumeForm(instance=applicant)
    if request.method == 'POST':
        form = ApplicantAddResumeForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('applicant-add-resume')

    name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'form': form,
    }
    return render(request, 'user/applicant/applicant-add-resume.html', context)


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def company_edit_profile(request):
    company = request.user.companyprofilemodel
    form = CompanyEditProfileForm(instance=company)
    if request.method == 'POST':
        form = CompanyEditProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company-profile', request.user.id)
        else:
            messages.error(request, 'There are a few problems')
            return redirect('company-edit-profile')

    context = {
        'form': form,
    }
    return render(request, 'user/company/company-edit-profile.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_experience(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = WorkExperienceForm()
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-experience')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-experience.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_experience(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    experience = WorkExperienceModel.objects.get(id=pk)
    form = WorkExperienceForm(instance=experience)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-experience', request.workexperiencemodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-experience.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_experience(request, pk):
    name = extractFirstName(request.user.name)
    experience = WorkExperienceModel.objects.get(id=pk)
    if request.method == 'POST':
        experience.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': experience,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-experience.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_education(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = EducationForm()
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-education')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-education.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_education(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    education = EducationModel.objects.get(id=pk)
    form = EducationForm(instance=education)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-education', request.educationmodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-education.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_education(request, pk):
    name = extractFirstName(request.user.name)
    education = EducationModel.objects.get(id=pk)
    if request.method == 'POST':
        education.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': education,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-education.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_skill(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = SkillSetForm()
    if request.method == 'POST':
        form = SkillSetForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-skill')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-skill.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_skill(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    skill = SkillSetModel.objects.get(id=pk)
    form = SkillSetForm(instance=skill)
    if request.method == 'POST':
        form = SkillSetForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-skill', request.skillsetmodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-skill.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_skill(request, pk):
    name = extractFirstName(request.user.name)
    skill = SkillSetModel.objects.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': skill,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-skill.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_language(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = LanguageSetForm()
    if request.method == 'POST':
        form = LanguageSetForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.user = request.user
            language.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-language')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-language.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_language(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    language = LanguageModel.objects.get(id=pk)
    form = LanguageSetForm(instance=language)
    if request.method == 'POST':
        form = LanguageSetForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-language', request.skillsetmodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-language.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_language(request, pk):
    name = extractFirstName(request.user.name)
    language = LanguageModel.objects.get(id=pk)
    if request.method == 'POST':
        language.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': language,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-language.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_reference(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = ReferenceForm()
    if request.method == 'POST':
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.user = request.user
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-reference')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-reference.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_reference(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    reference = ReferenceModel.objects.get(id=pk)
    form = ReferenceForm(instance=reference)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-reference', request.referencemodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-reference.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_reference(request, pk):
    name = extractFirstName(request.user.name)
    reference = ReferenceModel.objects.get(id=pk)
    if request.method == 'POST':
        reference.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': reference,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-reference.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_award(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = AwardForm()
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            award = form.save(commit=False)
            award.user = request.user
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-award')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-award.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_award(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    award = AwardModel.objects.get(id=pk)
    form = AwardForm(instance=award)
    if request.method == 'POST':
        form = AwardForm(request.POST, instance=award)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-award', request.awardmodel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }
    return render(request, 'user/applicant-details/add-edit-award.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_award(request, pk):
    name = extractFirstName(request.user.name)
    award = AwardModel.objects.get(id=pk)
    if request.method == 'POST':
        award.delete()
        return redirect('applicant-profile', request.user.id)

    context = {
        'item': award,
        'name': name,
    }
    return render(request, 'user/applicant-details/delete-award.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def add_preferred_job(request):
    task = "Add"
    name = extractFirstName(request.user.name)
    form = PreferredJobForm()
    if request.method == 'POST':
        form = PreferredJobForm(request.POST)
        if form.is_valid():
            preferred_job = form.save(commit=False)
            preferred_job.user = request.user
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('add-preferred-job')

    context = {
        'task': task,
        'form': form,
        'name': name,
    }

    return render(request, 'user/applicant-details/add-edit-preferred-jobs.html ', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def edit_preferred_job(request, pk):
    task = "Edit"
    name = extractFirstName(request.user.name)
    preferred_job = PreferredJobModel.objects.get(id=pk)
    form = PreferredJobForm(instance=preferred_job)
    if request.method == 'POST':
        form = PreferredJobForm(request.POST, instance=preferred_job)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            return redirect('edit-preferred-job', request.PreferredJobModel.id)

    context = {
        'task': task,
        'form': form,
        'name': name,
    }

    return render(request, 'user/applicant-details/add-edit-preferred-jobs.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def delete_preferred_jobs(request, pk):
    name = extractFirstName(request.user.name)
    preferred_job = PreferredJobModel.objects.get(id=pk)

    if request.method == 'POST':
        preferred_job.delete()

        return redirect('applicant-profile', request.user.id)

    context = {
        'item': preferred_job,
        'name': name,
    }

    return render(request, 'user/applicant-details/delete-preferred-jobs.html', context)


@login_required(login_url='login')
def account_settings(request, pk):
    user = User.objects.get(id=pk)
    name = extractFirstName(request.user.name)

    # deactivate_user(user)

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            if request.user.is_applicant:
                return redirect('applicant-feed')
            else:
                return redirect('company-profile', request.user.id)

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            if request.user.is_applicant:
                return redirect('applicant-feed')
            else:
                return redirect('company-profile', request.user.id)
        else:
            context = {
                'name': name,
                'information_form': information_form,
                'password_form': password_form,
            }
            return render(request, 'user/account-settings.html', context)

    context = {
        'name': name,
        'information_form': information_form,
        'password_form': password_form,
    }
    return render(request, 'user/account-settings.html', context)


@login_required(login_url='login')
def authentication_view(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.user.email
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                deactivate_user(user)
                return redirect('deactivation-successful')
            else:
                return redirect('authentication')
        else:
            return render(request, 'user/authentication.html', {'form': form})
    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, "user/authentication.html", context)


def deactivation_successful_view(request):
    return render(request, "user/deactivation_success.html")


def about(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)
    filled_job = FilledJobModel.objects.all()
    jobs = JobModel.objects.filter()
    name = ""
    if request.user.is_authenticated:
        name = extractFirstName(request.user.name)

    context = {
        'name': name,
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
        'jobs': jobs,
        'jobs_len': jobs.count(),
        'filled_job_len':filled_job.count(),
    }
    return render(request, 'user/about.html', context)


def contact(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        from_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['meherajmahmmd@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, "Feedback sent successfully.")
            return HttpResponseRedirect('contact')

    return render(request, 'user/contact.html', {})
