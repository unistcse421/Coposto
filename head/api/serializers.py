from head.models import Profile, Parcel
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'password')


# class ParcelSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')