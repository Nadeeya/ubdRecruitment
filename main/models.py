from django.db import models


# Create your models here.

class Job(models.Model):
    #id  =
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    uploadDate = models.DateField(auto_now_add=True)
    salary = models.IntegerField()
    minReq = models.CharField(max_length=200)
    yearsExp = models.IntegerField()
    description = models.TextField()
    contractDur = models.IntegerField()
    dateClose = models.DateField()
    jobForm = models.CharField(max_length=200)
    btnMsg = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
        








