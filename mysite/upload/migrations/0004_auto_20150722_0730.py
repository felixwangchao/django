# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_configuration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='publication',
        ),
        migrations.AddField(
            model_name='publication',
            name='sizeMax',
            field=models.CharField(default=20000000, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='typeAsk',
            field=models.CharField(default='pdf', max_length=40),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Configuration',
        ),
    ]
