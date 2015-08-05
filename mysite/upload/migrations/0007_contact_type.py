# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_remove_contact_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='Type',
            field=models.CharField(default='Technical', max_length=10),
            preserve_default=False,
        ),
    ]
