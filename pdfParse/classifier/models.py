from django.db import models

# Create your models here.

class pdf(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='static/')