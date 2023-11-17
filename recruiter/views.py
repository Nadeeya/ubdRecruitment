from django.shortcuts import render , redirect
from user.models import User
from mod.models import Recruiter , Application , Job
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from django.http import HttpResponse , Http404 , HttpResponseRedirect
import os
from django.conf import settings
import mimetypes
import pdfkit 
from django.template import loader
from xhtml2pdf import pisa
from shutil import make_archive
from wsgiref.util import FileWrapper



# Create your views here.
def recruiterHome(request):
    pk = request.user.id
    user = User.objects.get(id=pk)
    recruiter = Recruiter.objects.get(user=user)

    category = recruiter.category
    department = recruiter.department
    jobs = Job.objects.filter(department=department, category=category)
    applicants = Application.objects.filter(job__department=department).filter(job__category=category)
    totalJob = jobs.count()
    totalApplicants = applicants.count()

    context = {"user":user, "recruiter":recruiter, 'totalJob':totalJob , 'totalApplicants':totalApplicants}
    
    return render(request, 'recruiter/recruiterHome.html', context)

def viewJobs(request):
    pk = request.user.id
    user = User.objects.get(id=pk)
    recruiter  = Recruiter.objects.get(user=user)

    category = recruiter.category
    department = recruiter.department

    try:
        jobs = Job.objects.filter(department=department, category=category)
        totalJobs = jobs.count()
        openJobs = jobs.filter(status='OPEN').count()
        closedJobs = jobs.filter(status='CLOSED').count()

        search = request.GET.get('search') if request.GET.get('search') != None else ''
        sort = request.GET.get('sort') if request.GET.get('sort') != None else ''
        jobs = jobs.filter(name__icontains=search)
        if sort == 'earliest':
            jobs = jobs.order_by('uploadDate')
        elif sort == 'latest':
            jobs = jobs.order_by('-uploadDate')
        result = jobs.count()
        context = {'job' : jobs, 'result':result, 'totalJobs':totalJobs , 'openJobs':openJobs , 'closedJobs':closedJobs}


    except Job.DoesNotExist:
        message = "There is no job available"
        context = {'message' : message}

    
    return render(request, 'recruiter/viewJobs.html', context)


def viewApplicantsJob(request , pk):
    job = Job.objects.get(id=pk)
    NATIONALITIES_list = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']


    try:
        applicants = Application.objects.filter(job=job)
        search = request.GET.get('search') if request.GET.get('search') != None else ''
        nationality = request.GET.get('nationality') if request.GET.get('nationality') != None else ''
        order = request.GET.get('order') if request.GET.get('order') != None else ''
        status = request.GET.get('status') if request.GET.get('status') != None else ''

        # no of applicants, pending and recommended

        totalApplicants = len(applicants)
        recommended = len(applicants.filter(applicant_status='RECOMMENDED'))
        pending = len(applicants.filter(applicant_status='PENDING'))

        if order == 'ne':
            applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(applicant_status__icontains=status).order_by('-date_added')
        elif order == 'od':
            applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(applicant_status__icontains=status).order_by('date_added')

        elif order=='':
            applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(applicant_status__icontains=status)

        # no of applicants, pending and recommended
        count_applicants = len(applicants)

        context = {'applicants':applicants, 'job':job , 'count_applicants':count_applicants ,
                   'nationality':NATIONALITIES_list, 'totalApplicants':totalApplicants , 'recommended':recommended , 'pending':pending}

    except Job.DoesNotExist:
        message = "There is no applicants"
        context = {'message' : message , 'nationality':NATIONALITIES_list}


    return render(request, 'recruiter/viewApplicants.html', context)


def generate_pdf_file(request, pk):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    row_height = 20
    column_width = 50

    application = Application.objects.get(id=pk)

# application profile details:
    p.drawString(250, 800, 'Applicant ID :')
    p.drawString(350, 800, str(application.id))
    p.drawString(50 , 780 , 'Job applied : ')
    p.drawString(180, 780 , str(application.job.name))
    p.drawString(50 , 760 , 'Position applied :')
    p.drawString(180, 760 , str(application.postApplied))
    p.drawString(50 , 740 , "Fullname :")
    p.drawString(180, 740 , str(application.fullname))
    p.drawString(50 , 720 , "Date of birth :")
    p.drawString(180, 720 , str(application.profile.dob))
    p.drawString(50 , 700 , "Gender :")
    p.drawString(180, 700 , str(application.profile.gender))
    p.drawString(50 , 680 , "Place of birth :")
    p.drawString(180, 680 , str(application.profile.pob))
    p.drawString(50 , 660 , "Nationality :")
    p.drawString(180, 660 , str(application.profile.nationality))
    p.drawString(50 , 640 , "Citizenship :")
    p.drawString(180, 640 , str(application.profile.citizenship))
    p.drawString(50 , 620 , "Country of domicile :")
    p.drawString(180, 620 , str(application.profile.cod))
    p.drawString(50 , 600 , "Marital status :")
    p.drawString(180, 600 , str(application.profile.maritalStat))
    p.drawString(50 , 580 , "Religion :")
    p.drawString(180, 580 , str(application.profile.religion))
    p.drawString(50 , 560 , "Address :")
    p.drawString(180, 560 , str(application.profile.address))
    p.drawString(50 , 540 , "Phone no :")
    p.drawString(180, 540 , str(application.profile.code) + str(application.profile.phoneNo))
    p.drawString(50 , 520 , "Email :")
    p.drawString(180, 520 , str(application.user.email))
    p.drawString(50 , 500 , "IC or Password no. :")
    p.drawString(180, 500 , str(application.profile.icPass))
    p.line(30, 490, 580, 490)

# application details:
    p.drawString(50 , 470 , "Present Employment :")
    p.drawString(220, 470 , str(application.presentEmployment.get('Present_post')))
    p.drawString(50 , 450 , "Present Employer :")
    p.drawString(220, 450 , str(application.presentEmployment.get('Present_Employer')))
    p.drawString(50 , 430 , "Current Duties :")
    p.drawString(220, 430 , str(application.presentEmployment.get('Current_dutties')))
    p.drawString(50 , 410 , "Current Post Appointment :")
    p.drawString(220, 410 , str(application.presentEmployment.get('Current_post_appointment')))
    p.drawString(50 , 390 , "Basic salary :")
    p.drawString(220, 390 , str(application.presentEmployment.get('Basic_salary')))
    p.drawString(50 , 370 , "Other Emoluments Allowance :")
    p.drawString(220, 370 , str(application.presentEmployment.get('Other_Emoluments_Allowance')))
    p.drawString(50 , 350 , "Income tax deduction :")
    p.drawString(220, 350 , str(application.presentEmployment.get('Income_Tax_Deduction')))
    p.drawString(50 , 330 , "Period of notice :")
    p.drawString(220, 330 , str(application.presentEmployment.get('Period_of_Notice')))
    p.line(30, 320, 580, 320)

    #academic reco
    p.drawString(50 , 300 , "Academic Record :")
    p.drawString(180, 300 , str(application.academicRec))
    p.drawString(50 , 280 , "Membership Fellowship :")
    p.drawString(220, 280 , str(application.membershipFellowship))
    p.drawString(50 , 250 , "Employement Recommendation for Higher Education :")
    p.drawString(50, 230 , str(application.employementRec.get('Employement_Recommendation_Higher_Education')))
    p.drawString(50 , 200 , "Employement Recommendation for Industry :")
    p.drawString(50, 180 , str(application.employementRec.get('Employement_Recommendation_Industry')))
    p.drawString(50 , 160 , "Courses offering :")
    p.drawString(180, 160 , str(application.teachingSupervision.get('Courses_offering')))
    p.drawString(50 , 140 , "List of Supervision :")
    p.drawString(180, 140 , str(application.teachingSupervision.get('List_of_Supervision')))
    p.drawString(50 , 120 , "Area of interest :")
    p.drawString(180, 120 , str(application.teachingSupervision.get('Area_of_Interest')))
    p.drawString(50 , 100 , "Google H index :")
    p.drawString(180, 100 , str(application.teachingSupervision.get('Google_H_index')))
    p.drawString(50 , 80 , "Scopus H index :")
    p.drawString(180, 80 , str(application.teachingSupervision.get('Scopus_H_index')))

    p.showPage()
    p.drawString(50 , 780 , 'Malay : ')
    p.drawString(180, 780 , str(application.languages.get('Malay')))
    p.drawString(50 , 760 , 'English : ')
    p.drawString(180, 760 , str(application.languages.get('English')))
    p.drawString(50 , 740 , 'Arabic : ')
    p.drawString(180, 740 , str(application.languages.get('Arabic')))
    p.line(30, 730, 580, 730)

    p.drawString(50 , 710 , 'Children : ')
    p.drawString(180, 710 , str(application.family.get('Children')))
    p.drawString(50 , 690 , 'Spouse : ')
    p.drawString(180, 690 , str(application.family.get('Spouse')))
    p.line(30, 680, 580, 680)

    p.drawString(50 , 660 , 'Referee 1 : ')
    p.drawString(180, 660 , str(application.referees.get('Referee_1')))
    p.drawString(50 , 640 , 'Referee 2 : ')
    p.drawString(180, 640 , str(application.referees.get('Referee_2')))
    p.drawString(50 , 620 , 'Referee 3 : ')
    p.drawString(180, 620 , str(application.referees.get('Referee_3')))



    # start_y = 710
    # p.line(30, start_y, 580, start_y)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{application.id}.pdf')



def viewApplicantDet(request, pk):
    applicant = Application.objects.get(id=pk)
    context =  {'applicant':applicant}

    return render(request, 'recruiter/viewApplicantDet.html', context)

def recommendApplicant(request, pk):
    applicant = Application.objects.get(id=pk)
    applicant.applicant_status = 'RECOMMENDED'
    id = applicant.job_id
    applicant.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # return redirect('viewApplicantsJob', pk=id)


def notRecommendApplicant(request, pk):
    applicant = Application.objects.get(id=pk)
    applicant.applicant_status = 'NOT RECOMMENDED'
    id = applicant.job_id
    applicant.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    # return redirect('viewApplicantsJob', pk=id)
def pendingApplicant(request, pk):
    applicant = Application.objects.get(id=pk)
    applicant.applicant_status = 'PENDING'
    id = applicant.job_id
    applicant.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def get_excel(request , pk):
    applicants  = Application.objects.filter(job_id = pk)
    response = HttpResponse(content_type='application/ms-excel')
    job = Job.objects.get(id=pk)
    response['Content-Disposition'] = f'attachment; filename="{job.name}.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = f"Applicants for {job.name}"

    # Add headers
    headers = ["ID" ,
               "Post Applied",
                "Full name",
                "Email",
                "DOB",
                "Gender", 
                "POB",
                "Nationality",
                "Citizenhsip",
                "COD",
                "Marital Status",
                "Religion",
                "Home Address",
                "Phone No.",
                "IC / Passport No.",
                "Highest Education Qualification",
                "Years of Experience",
                "Date applied",
                "Source",
                "Present Post",
                "Present Employer",
                "Current Dutties",
                "Current Post Appointment",
                "Basic Salary",
                "Other Emoluments Allowance",
                "Income Tax Deduction",
                "Period of Notice",
                "Academic Record",
                "Membership and Fellowship",
                "Employment Recommendation Higher Education",
                "Employment Recommendation Industry",
                "Courses Offering",
                "List of Supervision",
                "Area of interest",
                "Google H index",
                "Scopus H index",
                "Malay",
                "English",
                "Arabic",
                "Others",
                "Children",
                "Spouse",
                "Referee 1",
                "Referee 2",
                "Referee 3",
                "Status",
                ]
    ws.append(headers)

    # Add data from the model
    for applicant in applicants:
        ws.append([applicant.id,
                    applicant.postApplied,
                    applicant.fullname,
                    applicant.user.email,
                    applicant.profile.dob,
                    applicant.profile.gender, 
                    applicant.profile.pob , 
                    applicant.profile.nationality , 
                    applicant.profile.citizenship , 
                    applicant.profile.cod , 
                    applicant.profile.maritalStat , 
                    applicant.profile.religion , 
                    applicant.profile.address , 
                    applicant.profile.phoneNo , 
                    applicant.profile.icPass , 
                    applicant.profile.highQual , 
                    applicant.profile.yearsExp , 
                    applicant.date_added , 
                    applicant.source , 
                    applicant.presentEmployment.get('Present_post') , 
                    applicant.presentEmployment.get('Present_Employer') , 
                    applicant.presentEmployment.get('Current_dutties') , 
                    applicant.presentEmployment.get('Current_post_appointment') , 
                    applicant.presentEmployment.get('Basic_salary') , 
                    applicant.presentEmployment.get('Other_Emoluments_Allowance') , 
                    applicant.presentEmployment.get('Income_Tax_Deduction') , 
                    applicant.presentEmployment.get('Period_of_Notice') ,
                    applicant.academicRec ,
                    applicant.membershipFellowship ,
                    applicant.employementRec.get('Employement_Recommendation_Higher_Education'), 
                    applicant.employementRec.get('Employement_Recommendation_Industry'), 
                    applicant.teachingSupervision.get('Courses_offering'), 
                    applicant.teachingSupervision.get('List_of_Supervision') , 
                    # '=HYPERLINK("{}", "{}")'.format("request.build_absolute_uri(applicant.teachingSupervision.get('Supervision_file'))", "Supervision"),
                    applicant.teachingSupervision.get('Area_of_Interest') , 
                    applicant.teachingSupervision.get('Google_H_index') , 
                    applicant.teachingSupervision.get('Scopus_H_index') , 
                    applicant.languages.get('Malay') , 
                    applicant.languages.get('English') , 
                    applicant.languages.get('Arabic') , 
                    applicant.languages.get('Others') , 
                    applicant.family.get('Children') , 
                    applicant.family.get('Spouse') , 
                    applicant.referees.get('Referee_1') , 
                    applicant.referees.get('Referee_2') , 
                    applicant.referees.get('Referee_3') , 
                    applicant.applicant_status , 
                    ])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


def downloadAllApplicantFolder(request, pk):
    job = Job.objects.get(id=pk)
    path = f'applicants/{job.name}'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    # if os.path.exists(file_path):
        # mime_type , _ = mimetypes.guess_type(file_path)
        # with open (file_path , 'r') as fh:
            # response = HttpResponse(fh.read(), content_type='application/zip')
            # response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
            # return response
        # zip_file = open(file_path , 'r')
        # response = HttpResponse(zip_file, content_type='application/force-download')
        # response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
        # return response
    
    path_to_zip = make_archive(file_path, "zip", file_path)
    response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{job.name}.zip"'
    return response

    raise Http404




def viewApplicants(request):
    category = request.user.recruiter.category
    department = request.user.recruiter.department
    NATIONALITIES_list = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']
    
    # filter applicants:
    applicants = Application.objects.filter(job__department=department).filter(job__category=category)

    totalApplicants = len(applicants)
    recommended = len(applicants.filter(applicant_status='RECOMMENDED'))
    pending = len(applicants.filter(applicant_status='PENDING'))

    search = request.GET.get('search') if request.GET.get('search') != None else ''
    nationality = request.GET.get('nationality') if request.GET.get('nationality') != None else ''
    job_name = request.GET.get('jobs') if request.GET.get('jobs') != None else ''
    order = request.GET.get('order') if request.GET.get('order') != None else ''
    status = request.GET.get('status') if request.GET.get('status') != None else ''

    if order == 'ne':
        applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(job__name__icontains=job_name).filter(applicant_status__icontains=status).order_by('-date_added')
    elif order == 'od':
        applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(job__name__icontains=job_name).filter(applicant_status__icontains=status).order_by('date_added')

    elif order=='':
        applicants = applicants.filter(fullname__icontains=search).filter(profile__nationality__icontains=nationality).filter(job__name__icontains=job_name).filter(applicant_status__icontains=status)
    
    count_applicants = len(applicants)
    jobs = Job.objects.filter(department=department, category=category)

    context = {'applicants':applicants, 'count_applicants':count_applicants ,'nationality':NATIONALITIES_list , 'jobs':jobs , 'totalApplicants':totalApplicants , 'recommended':recommended, 'pending':pending}
    return render(request, 'recruiter/viewAllApplicants.html', context )


def viewNextApplicant(request , job_id , current_applicant_id):
    job = Job.objects.get(id=job_id)
    applicants = Application.objects.filter(job=job)
    for applicant in applicants:
        if applicant.id > int(current_applicant_id):
            return redirect('viewApplicantDet' , pk=applicant.id)
    #if there is no result go to the first applicant?

    first_applicant = Application.objects.filter(job=job).first()

    return redirect ('viewApplicantDet', pk=first_applicant.id)

def viewPreviousApplicant(request, job_id, current_applicant_id):
    job = Job.objects.get(id=job_id)
    applicants = Application.objects.filter(job=job)
    for applicant in reversed(applicants):
        if applicant.id < int(current_applicant_id):
            return redirect('viewApplicantDet' , pk=applicant.id)
    #if there is no result go to the first applicant?

    last_applicant = Application.objects.filter(job=job).last()

    return redirect ('viewApplicantDet', pk=last_applicant.id)



def viewJobDet(request, pk):
    job = Job.objects.get(id=pk)
    context = {'job':job}
    return render(request, 'recruiter/viewJobDet.html', context)