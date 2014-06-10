from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Ubicacions(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    provincia = models.CharField(max_length=30)
    comarca = models.CharField(max_length=30)
    poble = models.CharField(max_length=30)
    adressa = models.TextField(max_length=100)

    def __unicode__(self):
        return self.adressa

    def get_absolute_url(self):
        return reverse('ubicacio_detail', kwargs={'pk': self.pk})


class Festes(models.Model):
    nom = models.CharField(max_length=50)
    data_inici = models.DateTimeField()
    data_fi = models.DateTimeField()
    categoria = models.CharField(max_length=30)
    descripcio = models.TextField(max_length=200)
    localitat = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('festa_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'),
        (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating(stars)', blank=False,
        default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=User.objects.get(id=1))
    date = models.DateField(default=date.today)

    class  Meta:
        abstract = True


class FestaReview(Review):
    restaurant = models.ForeignKey(Festes)


class Events(models.Model):
    nom = models.CharField(max_length=50)
    tipus = models.CharField(max_length=30)
    descripcio = models.TextField(max_length=200)
    festa = models.ForeignKey(Festes)
    ubicacio = models.ForeignKey(Ubicacions)
    data = models.DateTimeField()

    def __unicode__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})


class Usuaris(User):
    assistencia = models.ManyToManyField(Festes)

    def __unicode__(self):
        return self.username


class Organitzadors(Usuaris):
    empresa = models.CharField(max_length=30)
    festa = models.ManyToManyField(Festes, blank=True)
    event = models.ManyToManyField(Events, blank=True)

    def __unicode__(self):
        return self.username