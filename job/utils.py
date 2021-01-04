from django.core.mail import send_mail
from datetime import date
from django.template import loader
from user.models import ApplicantProfileModel, SkillSetModel, PreferredJobModel, WorkExperienceModel


def calculate_exp(exp):
    end_date = exp.left
    start_date = exp.started
    if end_date is not None:
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    else:
        end_date = date.today()
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)


def match_percentage(applicant, job):
    skill_list = SkillSetModel.objects.filter(user=applicant)
    experience_list = WorkExperienceModel.objects.filter(user=applicant)
    percentage = 0

    if job.experience is None:
        for skill in skill_list:
            split_text = skill.skill_title.lower().split(' ')

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)

                if index >= 0 or index1 >= 0:
                    percentage = 50
                    print("at exp none and skill", percentage)

        for exp in experience_list:
            split_text = exp.job_title.lower().split(' ')

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)
                if index >= 0 or index1 >= 0:
                    if percentage == 0:
                        percentage = 50
                        print("at exp none and exp", percentage)
                        return percentage

                    else:
                        percentage = 100
                        print("at exp none and exp", percentage)
                        return percentage
    else:

        for exp in experience_list:
            split_text = exp.job_title.lower().split(' ')
            work_exp = calculate_exp(exp)

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)

                if index >= 0 or index1 >= 0:
                    if work_exp >= job.experience:
                        percentage = 70
                        print("at exp not none and exp+year", percentage)
                    else:
                        percentage = 45
                        print("at exp not none and exp", percentage)

        for skill in skill_list:
            split_text = skill.skill_title.lower().split(' ')

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)

                if index >= 0 or index1 >= 0:
                    if percentage == 0:
                        percentage = 30
                        print("at exp not none and skill", percentage)
                        return percentage
                    elif percentage == 45:
                        percentage = 75
                        print("at exp not none and skill+exp", percentage)
                        return percentage

                    else:
                        percentage = 100
                        print("at exp not none and skill+exp+year", percentage)
                        return percentage

    return percentage


def match_skill(applicant, job):
    skill_list = SkillSetModel.objects.filter(user=applicant.user)
    preferred_job_list = PreferredJobModel.objects.filter(user=applicant.user)

    send_mail_var = False
    for skill in skill_list:
        split_text = skill.skill_title.lower().split(' ')

        for s in split_text:
            index = job.requirements.lower().find(s)
            index1 = job.job_title.lower().find(s)

            if index >= 0 or index1 >= 0:
                send_mail_var = True

    for preferred_job in preferred_job_list:
        split_text = preferred_job.details.lower().split(' ')

        for s in split_text:
            index = job.requirements.lower().find(s)
            index1 = job.job_title.lower().find(s)
            if index >= 0 or index1 >= 0:
                send_mail_var = True

    return send_mail_var


def send_mail_to_applicants(job):
    applicants = ApplicantProfileModel.objects.all()
    applicant_list = []
    for applicant in applicants:
        if match_skill(applicant, job):
            applicant_list.append(applicant)

    send_new_job_mail_func(applicant_list, job)
    return


def send_new_job_mail_func(applicant_list, job):
    for applicant in applicant_list:
        subject = "A New Job Matches Your Speciality"
        from_email = 'officialjobland777@gmail.com'

        home_link = "http://127.0.0.1:8000"
        job_link = "http://127.0.0.1:8000/job/job-profile/" + str(job.id) + "/"
        context = {
            "applicant": applicant,
            "home_link": home_link,
            "job_link": job_link,
        }
        msg_plain = loader.render_to_string('email/job-notification.txt', context)
        msg_html = loader.render_to_string('email/job-notification.html', context)

        send_mail(subject, msg_plain, from_email, [applicant.user.email], fail_silently=True, html_message=msg_html)
    return


def send_mail_delete_job(user, job, details):
    subject = "'" + job.job_title + "'" + " has been deleted."
    from_email = user.email
    message = "'" + details + "'  said by " + from_email

    send_mail(
        subject + " from " + from_email,
        message,
        from_email,
        ['officialjobland777@gmail.com', ],
        # the mail address that the email will be sent to
    )
