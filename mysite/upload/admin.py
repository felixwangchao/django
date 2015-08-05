# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Editor, Publication, Contact

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 3

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 3


class EditorAdmin(admin.ModelAdmin):
    # this is used to change the display in the admin
    fields = ['Editor','Website','Address','Zipcode','Country','Language','PhoneNumber']
    inlines = [PublicationInline,ContactInline]

admin.site.register(Editor, EditorAdmin)

