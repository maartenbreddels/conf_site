# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-29 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('proposals', '0010_make_affiliation_mandatory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('official', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
            },
        ),
        migrations.CreateModel(
            name='TaggedProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals_taggedproposal_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals_taggedproposal_items', to='proposals.ProposalKeyword')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserTaggedProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals_usertaggedproposal_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals_usertaggedproposal_items', to='proposals.ProposalKeyword')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='official_keywords',
            field=taggit.managers.TaggableManager(blank=True, help_text=b'', through='proposals.TaggedProposal', to='proposals.ProposalKeyword', verbose_name=b'Official Keywords'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='user_keywords',
            field=taggit.managers.TaggableManager(blank=True, help_text=b'Please add keywords as a comma-separated list.', through='proposals.UserTaggedProposal', to='proposals.ProposalKeyword', verbose_name=b'Additional Keywords'),
        ),
    ]
