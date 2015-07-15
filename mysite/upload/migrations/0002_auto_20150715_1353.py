# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PublicationTitle', models.CharField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='editor',
            name='PublicationTitle',
        ),
        migrations.AddField(
            model_name='publication',
            name='editor',
            field=models.ForeignKey(to='upload.Editor'),
        ),
    ]
