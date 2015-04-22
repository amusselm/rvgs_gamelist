# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0008_auto_20150126_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='systemDescription',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
