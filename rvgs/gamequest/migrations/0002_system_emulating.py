# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='emulating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='gamequest.System', null=True),
            preserve_default=True,
        ),
    ]
