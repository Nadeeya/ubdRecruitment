from django.urls import path, include
from . import views
from user.views import loginPage , logoutUser , profilePage , registration


urlpatterns = [
    path('', views.home, name="home"),
    

    #directories for ubd navigation bar:
    path('researchFacilities/', views.researchFacilities ,name="researchFacilities"),
    path('ubdLiving/', views.ubdLiving ,name="ubdLiving"),
    path('ubdBenefit/', views.ubdBenefit ,name="ubdBenefit"),
    path('ubdAbout/', views.ubdAbout ,name="ubdAbout"),

    #to connect to other web page from other apps:
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('profile-page/', profilePage , name="profilePage"),
    path('applicant-registration/', registration , name="applicant_reg"),

    #view each job details
    path('jobDetails/<str:pk>/', views.jobDetails ,name="jobDetails"),
    path('jobForm/<str:pk>/', views.jobForm ,name="jobForm"),

    
   




]