# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Editor, Publication

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 3


class EditorAdmin(admin.ModelAdmin):
    # this is used to change the display in the admin
    fields = ['Editor','Title','Name','Surname','Email','InternationalPhoneNumber']
    inlines = [PublicationInline]

admin.site.register(Editor, EditorAdmin)

