from django.shortcuts import render, redirect
from django.contrib import messages
#from .models import Job
from mod.models import Job , Application , UserFile
from user.models import User, Applicant
import os
from django.conf import settings
from datetime import datetime

# Create your views here.
def home(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    department = request.GET.get('department') if request.GET.get('department') != None else ''
    category = request.GET.get('category') if request.GET.get('category') != None else ''
    minReq = request.GET.get('minReq') if request.GET.get('minReq') != None else ''
    order = request.GET.get('uploadDate') if request.GET.get('uploadDate') != None else ''

    if order == 'latest':
        jobs = Job.objects.filter(name__icontains=search).filter(department__icontains=department).filter(category__icontains=category).filter(minReq__icontains=minReq).order_by('-uploadDate')
    
    elif order == 'earliest':
        jobs = Job.objects.filter(name__icontains=search).filter(department__icontains=department).filter(category__icontains=category).filter(minReq__icontains=minReq).order_by('uploadDate')
    
    else:
        jobs = Job.objects.filter(name__icontains=search).filter(department__icontains=department).filter(category__icontains=category).filter(minReq__icontains=minReq)
    
    job_count = jobs.count()
    elapsedTimeDict = {}

    for job in jobs :
        now =  datetime.now().date()
        elapsedTime = (now - job.uploadDate).days
        if elapsedTime == 0:
            days = 'Today'
        elif elapsedTime < 7:
            days = str(elapsedTime) + ' days ago'
        elif elapsedTime == 7:
            days = 'A week ago'
        elif elapsedTime > 7:
            day = elapsedTime//7
            days =  str(day) + ' weeks ago'
        elif elapsedTime == 30 | elapsedTime == 31:
            days = 'A month ago'
        elif elapsedTime > 31:
            month = elapsedTime//30
            days = str(month) + ' months ago'
        elif elapsedTime == 365:
            days = 'A year ago'
        elif elapsedTime > 365:
            years = elapsedTime//365
            days = str(years) + ' years ago'

        id = job.id
        elapsedTimeDict[id] = days


    category_list = ['Academic' , 'Non-Academic' , 'Others']
    department_list = ['Admission',
			    'Academic Offices',
                'Center For Lifelong Learning',
                'Human Resources',
                'Corporate Communications',
                'Tabung UBD Finance',
				'Office of Promotion and Events Management',
				'Student Affairs Section',
                'Academy of Brunei Studies',
                'Faculty of Arts and Social Sciences',
                'Faculty of Integrated Technologies',
                'Faculty of Science',
                'Institute of Policy Studies',
                'Sultan Hassanal Bolkiah Institute of Education',
                'School of Digital Science',
                'Pengiran Anak Puteri Rashidah Sa’adatul Bolkiah Institute of Health Sciences',
                'UBD School of Business and Economics']
    
    minReq_list = ['Olevel',
                   'Alevel',
                   'HND',
                   'Degree',
                   'Master',
                   'PHD']
    

    context = {'jobs':jobs, 'job_count':job_count , 'category':category_list , 'department':department_list ,'minReq':minReq_list , 'elapsedTime':elapsedTimeDict}
    return render(request, 'main/mainPages/home.html', context)

# directories for ubd navigation bar:

def researchFacilities(request):
    return render(request, 'main/mainPages/researchFacilities.html')

def ubdLiving(request):
    return render(request, 'main/mainPages/ubdLiving.html')

def ubdBenefit(request):
    return render(request, 'main/mainPages/ubdBenefit.html')

def ubdAbout(request):
    return render(request, 'main/mainPages/ubdAbout.html')

# job details page:

def jobDetails(request, pk):
    job = Job.objects.get(id=pk)

    context = {'job':job}

    return render(request, 'main/mainPages/jobDetails.html', context)

def jobForm(request, pk):

    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in!')
        return redirect('login')
    
    job = Job.objects.get(id=pk)
    id = request.user.id
    user = User.objects.get(id=id)
    profile = Applicant.objects.get(user=user)

    NATIONALITIES_list = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']
    gender_list = ['Female', 'Male']
    maritalStat_list = ['Single', 'Married', 'Others']

    context = {'n': range(13), 'job':job, 'user':user, 'profile':profile, 'nationalities':NATIONALITIES_list , 'gender':gender_list
               , 'maritalStat':maritalStat_list }
    
    if request.method == "POST":
        email = request.POST.get('email')
        postApplied = request.POST.get('post_applied')
        datePrev = request.POST.get('date_prev')
        source = request.POST.get('source')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        pob = request.POST.get('pob')
        cod = request.POST.get('cod')
        nationality = request.POST.get('nationality')
        citizenship = request.POST.get('citizenship')
        marital = request.POST.get('marital')
        religion = request.POST.get('religion')
        icPass = request.POST.get('ic_passport')
        address = request.POST.get('address')
        phoneNo = request.POST.get('tel')

        presentPost = request.POST.get('present_post')
        presentEmployer = request.POST.get('present_employer')
        currentDuties = request.POST.get('current_duties')
        currentPostAppt = request.POST.get('current_post_appointment')
        basicSalary = request.POST.get('basic_salary')
        otherEmolumentsAllowance = request.POST.get('other_emoluments_allowance')
        incomeTaxDeduction = request.POST.get('income_tax_deduction')
        periodOfNotice = request.POST.get('period_of_notice')
        
        academicRec = request.POST.get('academic_rec')

        membershipFellowship = request.POST.get('membership_fellowship')

        empRecHighEd = request.POST.get('employment_rec_higher_ed')
        empRecInd = request.POST.get('employment_rec_industry')

        coursesOffering = request.POST.get('courses_offering')
        listSupervision = request.POST.get('list_supervision')
        superVisionFile = request.FILES['list_supervision_file']
        areaInterest = request.POST.get('area_interest')
        publications = request.FILES['publications']
        google_h_index = request.POST.get('google_h_index')
        scopus_h_index = request.POST.get('scopus_h_index')

        malay = request.POST.get('Malay')
        english = request.POST.get('English')
        arabic = request.POST.get('Arabic')
        others = request.POST.get('Others')

        children = request.POST.get('children')
        spouse = request.POST.get('spouse')

        referee1 = request.POST.get('referee_1')
        referee2 = request.POST.get('referee_2')
        referee3 = request.POST.get('referee_3')

        icPassFile = request.FILES['passport_ic']
        cv = request.FILES['CV']
        transcript = request.FILES['transcripts']
        other_docs = request.FILES['other_docs']

        user.email = email
        user.save()
        profile.dob = dob
        profile.gender = gender
        profile.pob = pob
        profile.nationality = nationality
        profile.citizenship = citizenship
        profile.cod = cod
        profile.maritalStat = marital
        profile.religion = religion
        profile.address = address
        profile.phoneNo = phoneNo
        profile.icPass = icPass
        profile.save()

        applicant_status = 'PENDING'

        application  = Application.objects.create(
            user = user,
            job = job,
            profile = profile)
        
        file_name = "Supervision file_" + str(user.id)

        myfile = UserFile.objects.create(applicant = application ,f_name=file_name,myfiles=superVisionFile)
        myfile.save()

        publicationsFile = UserFile.objects.create(applicant = application, f_name="Publications", myfiles=publications)
        publicationsFile.save()

        icPassFile1 = UserFile.objects.create(applicant=application, f_name="IC Passport", myfiles=icPassFile)
        icPassFile1.save()
        cvFile = UserFile.objects.create(applicant=application, f_name="CV", myfiles=cv)
        cvFile.save()
        transcriptFile = UserFile.objects.create(applicant=application, f_name="Transcript", myfiles=transcript)
        transcriptFile.save()
        other_docsFile = UserFile.objects.create(applicant=application, f_name="Other Document", myfiles=other_docs)
        other_docsFile.save()
        
        presentEmployement = {
            'Present_post' : presentPost,
            'Present_Employer' : presentEmployer,
            'Current_dutties' : currentDuties,
            'Current_post_appointment' : currentPostAppt,
            'Basic_salary' : basicSalary,
            'Other_Emoluments_Allowance' : otherEmolumentsAllowance,
            'Income_Tax_Deduction' : incomeTaxDeduction,
            'Period_of_Notice' : periodOfNotice
        }

        employementRec = {
            'Employement_Recommendation_Higher_Education': empRecHighEd,
            'Employement_Recommendation_Industry': empRecInd,
        }

        teachingSupervision = {
            'Courses_offering' : coursesOffering,
            'List_of_supervision' :listSupervision,
            'Supervision_file_name' : myfile.f_name,
            'Supervision_file' : myfile.myfiles.url,
            'Area_of_interest' :areaInterest,
            'Publications_name' : publicationsFile.f_name,
            'Publications_file' : publicationsFile.myfiles.url,
            'Google_H_index' : google_h_index,
            'Scopus_H_index' : scopus_h_index,
        }

        languages = {
            'Malay': malay,
            'English' : english,
            'Arabic' : arabic,
            'Others' : others
        }

        family = {
            'Children' : children,
            'Spouse' : spouse,
        }
        referees = {
            'Referee_1' : referee1,
            'Referee_2' : referee2,
            'Referee_3' : referee3,
        }

        documents = {
            'IC_Passport_name' : icPassFile1.f_name,
            'IC_Passport_file' : icPassFile1.myfiles.url,
            'CV_name' : cvFile.f_name,
            'CV_file' : cvFile.myfiles.url,
            'Transcript_name' : transcriptFile.f_name,
            'Transcript_file' : transcriptFile.myfiles.url,
            'Other_Documents_name' : other_docsFile.f_name,
            'Other_Documents_file' : other_docsFile.myfiles.url,

        }        

        application_cont = Application.objects.get(id = application.id)

        application_cont.applicant_status = applicant_status
        application_cont.datePrev = datePrev
        application_cont.source = source
        application_cont.fullname = fullname
        application_cont.presentEmployment = presentEmployement
        application_cont.academicRec = academicRec
        application_cont.membershipFellowship = membershipFellowship
        application_cont.employementRec = employementRec
        application_cont.teachingSupervision = teachingSupervision
        application_cont.languages = languages
        application_cont.family = family
        application_cont.referees = referees
        application_cont.documents = documents
        application_cont.postApplied = postApplied

        
        application_cont.save()
        messages.success(request, 'Your application form has been submitted!.')
        return redirect('home')

        #UserFile.objects.create(applicant = application)
        
        
        """
        application  = Application.objects.create(
            user = user,
            job = job,
            profile = profile,
            applicant_status = applicant_status,
            source = source,
            presentEmployement = presentEmployement,
            academicRec = academicRec,
            membershipFellowship = membershipFellowship,
            employementRec = employementRec,
            teachingSupervision = teachingSupervision,

        )"""
    return render(request, 'main/mainPages/jobForm.html', context)


