# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_auto_20150722_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Title', models.CharField(max_length=40)),
                ('Name', models.CharField(max_length=20)),
                ('Surname', models.CharField(max_length=20)),
                ('Type', models.CharField(max_length=10)),
                ('Language', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=40)),
                ('InternationalFixPhoneNumber', models.CharField(max_length=20)),
                ('InternationalMobilePhoneNumber', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='editor',
            old_name='InternationalPhoneNumber',
            new_name='Country',
        ),
        migrations.RenameField(
            model_name='editor',
            old_name='Name',
            new_name='Language',
        ),
        migrations.RenameField(
            model_name='editor',
            old_name='Surname',
            new_name='PhoneNumber',
        ),
        migrations.RenameField(
            model_name='editor',
            old_name='Email',
            new_name='Website',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='Title',
        ),
        migrations.AddField(
            model_name='editor',
            name='Address',
            field=models.CharField(default='135 avenue de rangueil', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editor',
            name='Zipcode',
            field=models.CharField(default=31077, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='Language',
            field=models.CharField(default='English', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='Periodicity',
            field=models.CharField(default='daily', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='PublicationDay',
            field=models.CharField(default='every day', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='editor',
            field=models.ForeignKey(to='upload.Editor'),
        ),
    ]
