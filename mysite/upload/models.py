from django.db import models

class Editor(models.Model):
    Editor = models.CharField(max_length = 40)
    Website = models.CharField(max_length = 40)
    Address = models.CharField(max_length=100)
    Zipcode = models.CharField(max_length=10)
    Country = models.CharField(max_length=20)
    Language = models.CharField(max_length=20)
    PhoneNumber = models.CharField(max_length=20)

    def __unicode__(self):
        return self.Editor

class Publication(models.Model):
    editor = models.ForeignKey(Editor)
    PublicationTitle = models.CharField(max_length = 40)
    sizeMax = models.CharField(max_length=40)
    typeAsk = models.CharField(max_length=40)
    Periodicity = models.CharField(max_length=20)
    PublicationDay = models.CharField(max_length=20)
    Language = models.CharField(max_length=20)
    Website = models.CharField(max_length=40)

    def __unicode__(self):
        return self.PublicationTitle


class Contact(models.Model):
    editor = models.ForeignKey(Editor)
    Title = models.CharField(max_length = 40)
    Name = models.CharField(max_length = 20)
    Surname = models.CharField(max_length = 20)
    Type = models.CharField(max_length=10)
    Language = models.CharField(max_length=20)
    Email = models.CharField(max_length = 40)
    InternationalFixPhoneNumber = models.CharField(max_length = 20)
    InternationalMobilePhoneNumber = models.CharField(max_length = 20)

    def show_name(self):
        name = self.Name + " "+self.Surname
        return name

    def __unicode__(self):
        return self.Name


