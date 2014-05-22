from rest_framework.fields import *
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import HyperlinkedModelSerializer
from .models import *


class UbicacioSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api_ubi-detail')

    class Meta:
        model = Ubicacions
        fields = ('url', 'latitude', 'longitude', 'provincia', 'comarca',
            'poble', 'adressa')


class EventSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api_event-detail')
    festa = HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api_festa-detail')
    ubicacio = HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api_ubi-detail')

    class Meta:
        model = Events
        fields = ('nom', 'tipus', 'descripcio', 'festa', 'ubicacio', 'data')


class FestaSerializer(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name='api_festa-detail')

    class Meta:
        model = Festes
        field = ('nom', 'data_inici', 'data_fi', 'categoria', 'descripcio',
            'localitat')