# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0007_contact_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='Website',
            field=models.CharField(default='www.baidu.com', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='editor',
            name='Address',
            field=models.CharField(max_length=100),
        ),
    ]
