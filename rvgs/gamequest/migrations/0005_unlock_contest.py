# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0004_auto_20141111_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='unlock',
            name='contest',
            field=models.ManyToManyField(to='gamequest.Contest'),
            preserve_default=True,
        ),
    ]
