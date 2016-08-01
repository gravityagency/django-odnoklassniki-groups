# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import m2m_history.fields
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('odnoklassniki_users', '0002_user_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('fetched', models.DateTimeField(db_index=True, null=True, verbose_name='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u043e', blank=True)),
                ('id', models.BigIntegerField(help_text='\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440', serialize=False, verbose_name='ID', primary_key=True)),
                ('albums_count', models.PositiveIntegerField(null=True)),
                ('discussions_count', models.PositiveIntegerField(null=True)),
                ('name', models.CharField(max_length=800)),
                ('description', models.TextField()),
                ('shortname', models.CharField(max_length=50)),
                ('members_count', models.PositiveIntegerField(null=True)),
                ('photo_id', models.BigIntegerField(null=True)),
                ('pic128x128', models.URLField()),
                ('pic50x50', models.URLField()),
                ('pic640x480', models.URLField()),
                ('premium', models.NullBooleanField()),
                ('private', models.NullBooleanField()),
                ('shop_visible_admin', models.NullBooleanField()),
                ('shop_visible_public', models.NullBooleanField()),
                ('attrs', annoying.fields.JSONField(null=True)),
                ('users', m2m_history.fields.ManyToManyHistoryField(to='odnoklassniki_users.User')),
            ],
            options={
                'verbose_name': 'Odnoklassniki group',
                'verbose_name_plural': 'Odnoklassniki groups',
            },
            bases=(models.Model,),
        ),
    ]
