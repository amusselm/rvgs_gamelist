# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0009_auto_20150422_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='achievement',
            name='name',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=2048),
            preserve_default=True,
        ),
    ]
