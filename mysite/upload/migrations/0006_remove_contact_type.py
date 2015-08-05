# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20150805_0743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='Type',
        ),
    ]
