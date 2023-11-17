from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User , Applicant
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# Create your views here.


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email , password = password)

        if user is not None:
            login(request, user)

            message = "Successfully logged in"
            
            context = {'message':message}

            if user.is_superuser:
                return redirect('adminHome')
            
            if request.user.type == 'APPLICANT':
                return redirect('home')
            
            if request.user.type == 'RECRUITER':
                return redirect('recruiterHome')
        else:
            messages.error(request, 'Email or Password does not exist')
    
        

    context = {}
    return render(request, 'user/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profilePage(request):
    id = request.user.id
    user = User.objects.get(id=id)
    profile = Applicant.objects.get(user=user)
    NATIONALITIES_list = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']
    gender_list = ['Female', 'Male']
    maritalStat_list = ['Single', 'Married', 'Others']
    context = {'user': user , 'profile':profile, 
               'nationalities': NATIONALITIES_list,
               'gender': gender_list,
               'maritalStat':maritalStat_list}
    

    if request.method == 'POST' and 'profileDetails' in request.POST:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        pob = request.POST.get('pob')
        nationality = request.POST.get('nationality')
        citizenship = request.POST.get('citizenship')
        cod = request.POST.get('cod')
        maritalStat = request.POST.get('maritalStat')
        religion = request.POST.get('religion')
        address = request.POST.get('address')
        code = request.POST.get('code')
        phoneNo = request.POST.get('phoneNo')
        icPass = request.POST.get('icPass')
        highQual = request.POST.get('highQual')
        yearsExp = request.POST.get('yearsExp')

        user.first_name = fname
        user.last_name = lname
        user.save()
        profile.dob = dob
        profile.gender = gender
        profile.pob = pob
        profile.nationality = nationality
        profile.citizenship = citizenship
        profile.cod = cod
        profile.maritalStat = maritalStat
        profile.religion = religion
        profile.address = address
        profile.code = code
        profile.phoneNo = phoneNo
        profile.icPass = icPass
        profile.highQual = highQual
        profile.yearsExp = yearsExp
        profile.save()

        message = 'Profile is successfully updated'

        context1 = {'user': user , 'profile':profile, 
               'nationalities': NATIONALITIES_list,
               'gender': gender_list,
               'maritalStat':maritalStat_list,
               'message': message}

        return render(request, 'user/profilePage.html' , context1)
    
    if request.method == 'POST' and 'uploadProfilePic' in request.POST:
        pic = request.FILES
        pic1 = pic['p']
        profile.profilePic = pic1
        profile.save()    

        return render(request, 'user/profilePage.html', context)



    return render(request, 'user/profilePage.html', context)

def signup(request):
    return render(request, 'user/signup.html')



def registration(request):
     
     if request.method == 'POST':
         fname = request.POST.get('fname')
         lname = request.POST.get('lname')
         email = request.POST.get('email')
         password = request.POST.get('password')
         password1 = request.POST.get('password1')
         dob = request.POST.get('dob')
         gender = request.POST.get('gender')
         pob = request.POST.get('pob')
         nationality = request.POST.get('nationality')
         citizenship = request.POST.get('citizenship')
         cod = request.POST.get('cod')
         maritalStat = request.POST.get('maritalStat')
         religion = request.POST.get('religion')
         address = request.POST.get('address')
         code = request.POST.get('code')
         phoneNo = request.POST.get('phoneNo')
         icPass = request.POST.get('icPass')
         highQual = request.POST.get('highQual')
         yearsExp = request.POST.get('yearsExp')
         

         check_user = User.objects.filter(email=email).first()

         if password != password1:
            context1 = {"message1" : "Password mismatch", "class1":"danger"}
            return render(request, 'user/signup.html' , context1)
         
         if check_user:
            context = {"message": "User already exist", "class": "danger"}
            return render(request, 'user/signup.html', context)
         
         user = User.objects.create_user(username= email, email=  email, password=password, first_name = fname, last_name = lname , type = 'APPLICANT')
         user.save()

         applicant_profile = Applicant.objects.create(
             user=user,
             dob=dob,
             gender = gender,
             pob = pob,
             nationality=nationality,
             citizenship = citizenship,
             cod = cod,
             maritalStat = maritalStat,
             religion = religion,
             address = address,
             code = code,
             phoneNo = phoneNo,
             icPass = icPass,
             highQual = highQual,
             yearsExp = yearsExp
                 )
         applicant_profile.save()

         context = {"message": "Successfully registrations Complete",
                    "class2":"alert1 success ",
                   }
         
         login(request, user)
         messages.success(request, 'Successfully registered.')
         return redirect('home')
     
     minReq_list = ['Olevel',
                'Alevel',
                'HND',
                'Degree',
                'Masters',
                'PHD']
     NATIONALITIES_list = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Chinese', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', 'Vietnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']
     context = {'nationalities': NATIONALITIES_list, 'minReq' : minReq_list} 

     return render(request, 'user/signup.html', context)
         



         



         









