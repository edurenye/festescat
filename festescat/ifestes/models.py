from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ubicacions(models.Model):
        latitude = models.FloatField()
        longitude = models.FloatField()
        provincia = models.CharField(max_length=30)
        comarca = models.CharField(max_length=30)
        poble = models.CharField(max_length=30)
        adressa = models.TextField(max_length=100)
	#def __unicode__(self):

class Festes(models.Model):
	nom = models.CharField(max_length=50)
	data_inici = models.DateTimeField()
	data_fi = models.DateTimeField()
	categoria = models.CharField(max_length=30)
	descripcio = models.TextField(max_length=200)
	localitat = models.CharField(max_length=30)

class Events(models.Model):
	nom = models.CharField(max_length=50)
	tipus = models.CharField(max_length=30)
	descripcio = models.TextField(max_length=200)
	festa = models.ForeignKey(Festes)
	ubicacio = models.ForeignKey(Ubicacions)
	data = models.DateTimeField()

class Organitzadors(User):
	empresa = models.CharField(max_length=30)
	nom = models.CharField(max_length=50)
	festa = models.ManyToManyField(Festes)
	event = models.ManyToManyField(Events)

class Usuaris(User):
	assistencia = models.ManyToManyField(Events)
