# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core import urlresolvers

from head.models import Profile, Parcel, Image, Bringer


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'date']


class InlineImage(admin.TabularInline):
    model = Image
    verbose_name = "Image"


class ParcelAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_a', 'profile_b', 'get_profiles_b',
                    'destination_a', 'destination_b', 'date_a', 'date_b',
                    'parcel_name', 'description', 'price', 'weight',
                    'is_featured',
                    'date']

    list_filter = (
        ('is_featured'),
        ('profile_a', admin.RelatedOnlyFieldListFilter),
        ('profile_b', admin.RelatedOnlyFieldListFilter),
        ('destination_a', admin.RelatedOnlyFieldListFilter),
        ('destination_b', admin.RelatedOnlyFieldListFilter),
    )

    inlines = [InlineImage]

    actions = ['make_featured', 'make_unfeatured']

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Feature selected parcels"

    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
    make_unfeatured.short_description = "UnFeature selected parcels"

    def get_profiles_b(self, obj):
        return "\n".join([p.email + ', ' for p in obj.profiles_b.all()])


class BringerAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile',
                    'destination_a', 'destination_b',
                    'flight_date',
                    'date']

    list_filter = (
        ('profile', admin.RelatedOnlyFieldListFilter),
        ('destination_a', admin.RelatedOnlyFieldListFilter),
        ('destination_b', admin.RelatedOnlyFieldListFilter),
    )

    # def link_to_profile(self, obj):
    #     link = urlresolvers.reverse("admin:head_Profile_change",
    #                             args=[obj.Profile.id])
    #     return u'<a href="%s">%s</a>' % (link,obj.B.name)
    # link_to_B.allow_tags=True


admin.site.register(Bringer, BringerAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(Profile, ProfileAdmin)
