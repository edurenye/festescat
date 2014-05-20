from rest_framework.fields import *
from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentifyField
from rest_framework.serializers import HyperlinkedModelSerializer
from models import *

class UbicacioSerializer(HyperlinkedModelSerializer):
    url =  HyperlinkedIdentifyField(view_name='ubi-detail')
    latitude = FloatField()
    longitude = FloatField()
    provincia = CharField()
    comarca = CharField()
    poble = CharField()
    adressa = TextField()
    class Meta:
        model = Ubicacions
        fields('url','latitude','longitude','provincia','comarca','poble','adressa')