from django.urls import path, include
from . import views
from user.views import loginPage , logoutUser

urlpatterns = [
    path('admin-home/', views.adminHomePage , name='adminHome'),
    path('add-recruiter/', views.addRecruiter, name='addRecruiter'),
    path('add-job/', views.addJob, name='addJob'),
    path('login/', loginPage , name="login"),
    path('logout/', logoutUser, name="logout"),
    path('manage-recuiters/', views.manageRecruiters, name="manageRecruiters"),
    path('manage-jobs/', views.manageJobs, name="manageJobs"),
    path('edit-recruiter/<str:pk>/', views.editRecruiter, name="editRecruiter"),
    path('delete-recruiter/<str:pk>/', views.deleteRecruiter, name="deleteRecruiter"),
    path('edit-job/<str:pk>/', views.editJob, name="editJob"),

]