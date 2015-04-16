# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0006_contest_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='upcoming',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
