# -*- coding: utf-8 -*-
from django.contrib import admin

from head.models import Profile, Parcel, Image


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'date']


class ParcelAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_a', 'profile_b', 'get_profiles_b',
                    'destination_a', 'destination_b', 'date_a', 'date_b',
                    'parcel_name', 'description', 'price', 'weight',
                    'date']

    def get_profiles_b(self, obj):
        return "\n".join([p.profiles_b for p in obj.profiles_b.all()])

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Parcel, ParcelAdmin)
