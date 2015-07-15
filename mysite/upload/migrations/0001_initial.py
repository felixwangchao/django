# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Editor', models.CharField(max_length=40)),
                ('PublicationTitle', models.CharField(max_length=40)),
                ('Title', models.CharField(max_length=40)),
                ('Name', models.CharField(max_length=20)),
                ('Surname', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=40)),
                ('InternationalPhoneNumber', models.CharField(max_length=20)),
            ],
        ),
    ]
