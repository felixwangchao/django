# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20150715_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SizeMax', models.CharField(max_length=40)),
                ('TypeAsk', models.CharField(max_length=40)),
                ('publication', models.ForeignKey(to='upload.Publication')),
            ],
        ),
    ]
