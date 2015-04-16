# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamequest', '0007_contest_upcoming'),
    ]

    operations = [
        migrations.AddField(
            model_name='unlock',
            name='comment',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='achievement',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='achievementlist',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contest',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
