from django.db import models
from django.utils import timezone
from user.models import User , Applicant

# Create your models here.

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    department = models.CharField(max_length=20)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email
    
class Job(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    uploadDate = models.DateField(auto_now_add=True)
    salaryMin = models.IntegerField()
    salaryMax = models.IntegerField()
    minReq = models.CharField(max_length=200)
    yearsExp = models.IntegerField()
    description = models.TextField()
    contractDur = models.IntegerField()
    dateClose = models.DateField()
    jobForm = models.CharField(max_length=200)
    btnMsg = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "applicants/{0}/user_{1}/{2}".format(instance.applicant.job.name ,instance.applicant.user.id, filename)
    
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    profile = models.ForeignKey(Applicant , on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, default="")
    applicant_status = models.CharField(max_length=10)
    date_added = models.DateField(default=timezone.now)
    source = models.CharField(max_length=200)
    datePrev = models.DateField(null=True)
    postApplied = models.CharField(max_length=20, default="")
    presentEmployment = models.JSONField(null=True)
    academicRec =  models.JSONField(null=True)
    membershipFellowship = models.TextField(default="" , null=True)
    employementRec = models.JSONField(null=True)
    teachingSupervision = models.JSONField(null=True)
    languages = models.JSONField(null=True)
    family = models.JSONField(null=True)
    referees = models.JSONField(null=True)
    documents = models.JSONField(null=True)

    #documents = models.FileField(upload_to=user_directory_path, default="")

    def __str__(self):
        return self.user.email
    

class UserFile(models.Model):
    applicant = models.ForeignKey(Application, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to=user_directory_path, default="", max_length=1000)

    def __str__(self):
        return self.f_name



    






